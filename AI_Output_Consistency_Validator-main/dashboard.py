import streamlit as st
import json

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Output Validator",
    page_icon="✦",
    layout="wide"
)

# ── Custom CSS (dark professional look) ──────────────────────────────────────
st.markdown("""
<style>
/* Dark background */
.stApp { background-color: #0d0f14; color: #e2e8f0; }

/* Hide default Streamlit header/footer */
#MainMenu, footer, header { visibility: hidden; }

/* Inputs and textareas */
.stTextArea textarea {
    background-color: #131720 !important;
    color: #e2e8f0 !important;
    border: 1px solid #2d3748 !important;
    border-radius: 10px !important;
    font-family: 'Courier New', monospace !important;
    font-size: 13px !important;
}

/* Buttons */
.stButton > button {
    background-color: #6366f1 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 10px 28px !important;
    font-size: 14px !important;
    width: 100% !important;
}
.stButton > button:hover {
    background-color: #4f46e5 !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background-color: #131720;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 16px;
}
[data-testid="metric-container"] label {
    color: #64748b !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #818cf8 !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0d0f14 !important;
    border-right: 1px solid #1e293b !important;
}
[data-testid="stSidebar"] * { color: #94a3b8 !important; }

/* Select box */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #131720 !important;
    border-color: #2d3748 !important;
    color: #e2e8f0 !important;
}

/* Success / Error boxes */
.success-box {
    background: rgba(74, 222, 128, 0.08);
    border: 1px solid rgba(74, 222, 128, 0.3);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.fail-box {
    background: rgba(248, 113, 113, 0.08);
    border: 1px solid rgba(248, 113, 113, 0.3);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.field-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 13px;
    font-family: 'Courier New', monospace;
}
.dot-ok  { color: #4ade80; font-size: 10px; }
.dot-err { color: #f87171; font-size: 10px; }
.score-big {
    font-size: 48px;
    font-weight: 700;
    font-family: 'Courier New', monospace;
    text-align: center;
}
.tag-pass {
    background: #14532d;
    color: #4ade80;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    display: inline-block;
}
.tag-fail {
    background: #7f1d1d;
    color: #f87171;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    display: inline-block;
}
.panel {
    background: #131720;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 20px;
}
.panel-title {
    font-size: 13px;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 14px;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 10px;
}
.hist-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    background: #0d0f14;
    border-radius: 8px;
    margin-bottom: 6px;
    font-size: 12px;
    font-family: 'Courier New', monospace;
}
</style>
""", unsafe_allow_html=True)

# ── Schema (same as your user_schema.json) ───────────────────────────────────
SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age":  {"type": "integer"},
        "city": {"type": "string"}
    },
    "required": ["name", "age", "city"],
    "additionalProperties": False
}

SAMPLE_VALID   = '{\n  "name": "John",\n  "age": 25,\n  "city": "Mumbai"\n}'
SAMPLE_INVALID = '{\n  "name": "John",\n  "age": "Twenty Five"\n}'
SAMPLE_MISSING = '{\n  "name": "John",\n  "age": 25\n}'

# ── Session state for stats & history ────────────────────────────────────────
if "total"   not in st.session_state: st.session_state.total   = 0
if "passed"  not in st.session_state: st.session_state.passed  = 0
if "failed"  not in st.session_state: st.session_state.failed  = 0
if "scores"  not in st.session_state: st.session_state.scores  = []
if "history" not in st.session_state: st.session_state.history = []


# ── Validator logic ───────────────────────────────────────────────────────────
def validate_json(data, schema):
    errors = []
    field_checks = {}

    # Step 1: check types for all present fields FIRST
    for k, v in data.items():
        if schema.get("additionalProperties") is False and k not in schema["properties"]:
            errors.append(f"Additional property '{k}' is not allowed")
            field_checks[k] = {"ok": False, "note": "NOT ALLOWED"}
        elif k in schema["properties"]:
            expected = schema["properties"][k]["type"]
            if expected == "integer":
                ok = isinstance(v, int) and not isinstance(v, bool)
            elif expected == "string":
                ok = isinstance(v, str)
            else:
                ok = True
            actual = type(v).__name__
            field_checks[k] = {"ok": ok, "note": expected if ok else f"expected {expected}, got {actual}"}
            if not ok:
                errors.append(f"'{k}' should be of type {expected}, got {actual}")

    # Step 2: check required fields are present
    for req in schema["required"]:
        if req not in data:
            errors.append(f"'{req}' is a required property")
            field_checks[req] = {"ok": False, "note": "MISSING"}

    # Step 3: fill in required fields that are present but not yet checked
    for req in schema["required"]:
        if req not in field_checks:
            field_checks[req] = {"ok": True, "note": schema["properties"][req]["type"]}

    score = 100 if not errors else max(0, 100 - len(errors) * 25)
    return {
        "status": "PASS" if not errors else "FAIL",
        "error": errors[0] if errors else None,
        "all_errors": errors,
        "consistency_score": score,
        "field_checks": field_checks
    }


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding: 10px 0 24px;'>
  <div style='display:flex; align-items:center; gap:12px; margin-bottom:6px;'>
    <div style='background:linear-gradient(135deg,#6366f1,#8b5cf6);width:34px;height:34px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:16px;'>✦</div>
    <span style='font-size:24px;font-weight:700;color:#f1f5f9;letter-spacing:-0.5px;'>ValidAI</span>
    <span style='background:#0d1f0d;color:#4ade80;border:1px solid #166534;font-size:11px;padding:3px 10px;border-radius:20px;margin-left:8px;'>● API Running</span>
  </div>
  <p style='color:#64748b;font-size:14px;margin-left:46px;'>AI Output Consistency Validator — validate JSON against your schema in real-time.</p>
</div>
<hr style='border:none;border-top:1px solid #1e293b;margin-bottom:28px;'>
""", unsafe_allow_html=True)

# ── STATS ROW ────────────────────────────────────────────────────────────────
avg_score = round(sum(st.session_state.scores) / len(st.session_state.scores)) if st.session_state.scores else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Validated", st.session_state.total)
col2.metric("✅  Passed",       st.session_state.passed)
col3.metric("❌  Failed",       st.session_state.failed)
col4.metric("📊  Avg Score",    f"{avg_score}%" if st.session_state.scores else "—")

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✦ ValidAI")
    st.markdown("---")
    st.markdown("**Load Sample**")
    sample = st.selectbox("Choose a sample", ["— select —", "Valid JSON", "Invalid (wrong type)", "Invalid (missing field)"])
    st.markdown("---")
    st.markdown("**Active Schema**")
    st.code(json.dumps(SCHEMA, indent=2), language="json")
    st.markdown("---")
    if st.button("🗑️  Clear History"):
        st.session_state.history = []
        st.session_state.total   = 0
        st.session_state.passed  = 0
        st.session_state.failed  = 0
        st.session_state.scores  = []
        st.rerun()

# ── MAIN: Input + Result ──────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="panel-title">📝 Input JSON</div>', unsafe_allow_html=True)

    # Load sample into text area
    default_text = ""
    if sample == "Valid JSON":
        default_text = SAMPLE_VALID
    elif sample == "Invalid (wrong type)":
        default_text = SAMPLE_INVALID
    elif sample == "Invalid (missing field)":
        default_text = SAMPLE_MISSING

    user_input = st.text_area(
        label="Paste your AI output JSON here",
        value=default_text,
        height=260,
        placeholder='{\n  "name": "John",\n  "age": 25,\n  "city": "Mumbai"\n}',
        label_visibility="collapsed"
    )

    validate_btn = st.button("✦ Validate JSON", use_container_width=True)

with right:
    st.markdown('<div class="panel-title">📊 Validation Result</div>', unsafe_allow_html=True)

    if validate_btn:
        if not user_input.strip():
            st.error("⚠️ Input is empty. Paste a JSON object first.")
        else:
            try:
                parsed = json.loads(user_input)
                result = validate_json(parsed, SCHEMA)

                # ── update stats
                st.session_state.total += 1
                st.session_state.scores.append(result["consistency_score"])
                if result["status"] == "PASS":
                    st.session_state.passed += 1
                else:
                    st.session_state.failed += 1

                # ── update history
                preview = user_input.replace("\n", " ").strip()[:50] + "…"
                st.session_state.history.insert(0, {
                    "status": result["status"],
                    "preview": preview,
                    "score": result["consistency_score"]
                })
                if len(st.session_state.history) > 8:
                    st.session_state.history.pop()

                # ── show result card
                box_class = "success-box" if result["status"] == "PASS" else "fail-box"
                tag_class  = "tag-pass"    if result["status"] == "PASS" else "tag-fail"
                score_color = "#4ade80" if result["consistency_score"] == 100 else "#f87171"
                message = "All checks passed ✅" if result["status"] == "PASS" else "Validation failed ❌"

                st.markdown(f"""
                <div class="{box_class}">
                  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
                    <div>
                      <span class="{tag_class}">{result['status']}</span>
                      <p style="color:#94a3b8;margin-top:8px;font-size:14px;">{message}</p>
                    </div>
                    <div class="score-big" style="color:{score_color}">{result['consistency_score']}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # ── field checks
                st.markdown("**Field Checks**")
                for field, info in result["field_checks"].items():
                    dot = '<span class="dot-ok">●</span>' if info["ok"] else '<span class="dot-err">●</span>'
                    status_color = "#94a3b8" if info["ok"] else "#f87171"
                    st.markdown(f"""
                    <div class="field-row">
                      {dot}
                      <span style="color:#e2e8f0;flex:1">{field}</span>
                      <span style="color:{status_color}">{info['note']}</span>
                    </div>""", unsafe_allow_html=True)

                # ── errors beyond first
                if result["all_errors"]:
                    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                    for err in result["all_errors"]:
                        st.error(f"· {err}")

                # ── raw JSON output
                st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                st.code(json.dumps({
                    "status": result["status"],
                    "error": result["error"],
                    "consistency_score": result["consistency_score"]
                }, indent=2), language="json")

            except json.JSONDecodeError as e:
                st.session_state.total += 1
                st.session_state.failed += 1
                st.session_state.scores.append(0)
                st.error(f"❌ Malformed JSON: {e}")
    else:
        st.markdown("""
        <div style='display:flex;flex-direction:column;align-items:center;justify-content:center;
                    min-height:260px;color:#334155;'>
          <div style='font-size:40px;margin-bottom:12px;'>🔍</div>
          <div style='font-size:14px;'>Paste JSON on the left and click Validate</div>
        </div>""", unsafe_allow_html=True)

# ── HISTORY ───────────────────────────────────────────────────────────────────
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
st.markdown(f'<div class="panel-title">🕘 Validation History ({len(st.session_state.history)})</div>', unsafe_allow_html=True)

if not st.session_state.history:
    st.markdown("<p style='color:#334155;text-align:center;padding:20px;'>No validations yet — run your first check above.</p>", unsafe_allow_html=True)
else:
    for h in st.session_state.history:
        tag = f'<span class="tag-pass">PASS</span>' if h["status"] == "PASS" else f'<span class="tag-fail">FAIL</span>'
        score_color = "#4ade80" if h["score"] == 100 else "#f87171"
        st.markdown(f"""
        <div class="hist-row">
          {tag}
          <span style="color:#64748b;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{h['preview']}</span>
          <span style="color:{score_color};font-weight:700;">Score: {h['score']}</span>
        </div>""", unsafe_allow_html=True)