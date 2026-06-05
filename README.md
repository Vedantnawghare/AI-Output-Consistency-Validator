
# 🤖 AI Output Consistency Validator

A modern AI Reliability and Validation system designed to verify whether AI-generated JSON responses follow predefined schemas consistently and accurately.

This project focuses on improving the reliability of AI outputs by detecting:
- Missing fields
- Incorrect data types
- Malformed JSON structures
- Schema inconsistencies

The system provides:
- ⚡ FastAPI backend for validation APIs
- 🎨 Streamlit dashboard with modern analytics UI
- 📊 Consistency scoring & validation tracking
- 📁 Validation history monitoring

---

# 🚀 Project Overview

AI systems often generate outputs that are:
- structurally inconsistent,
- missing important fields,
- incorrectly formatted,
- or difficult to process automatically.

This project solves that problem by implementing a schema-based validation pipeline that ensures AI-generated responses are reliable and machine-readable.

---

# ✨ Features

## ✅ AI Output Validation
Validate AI-generated JSON outputs against predefined schemas.

## ✅ Schema Enforcement
Ensures responses strictly follow required structures.

## ✅ JSON Verification
Detects malformed or invalid JSON outputs.

## ✅ Missing Field Detection
Identifies absent required properties.

## ✅ Data Type Validation
Checks whether values match expected types.

## ✅ Consistency Scoring
Generates a reliability score for every validation.

## ✅ FastAPI Backend
REST API endpoint for real-time validation.

## ✅ Interactive Streamlit Dashboard
Modern SaaS-style dashboard with:
- analytics cards,
- validation tracking,
- consistency metrics,
- validation history.

## ✅ Validation History Tracking
Tracks:
- Total validations
- Passed validations
- Failed validations

---

# 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core Programming Language |
| FastAPI | Backend API Framework |
| Streamlit | Dashboard UI |
| JSONSchema | Schema Validation |
| Pandas | Validation History Table |
| Uvicorn | ASGI Server |

---

# 📂 Project Structure

```bash
AI_Output_Consistency_Validator/
│
├── api.py
├── dashboard.py
├── validator.py
├── json_parser.py
├── requirements.txt
├── README.md
│
├── schemas/
│   └── user_schema.json
│
├── sample_outputs/
│   ├── valid.json
│   └── invalid.json
│
└── venv/
```

---

# ⚙️ How It Works

```text
AI Generated JSON
        ↓
JSON Parsing
        ↓
Schema Validation
        ↓
Consistency Checking
        ↓
Validation Report
        ↓
PASS / FAIL + Score
```

---

# 📌 Validation Rules

The validator checks for:

- Required fields
- Correct JSON structure
- Correct data types
- Additional unwanted properties
- Malformed JSON responses

---

# 📊 Example Schema

```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "age": {
      "type": "integer"
    },
    "city": {
      "type": "string"
    }
  },
  "required": ["name", "age", "city"],
  "additionalProperties": false
}
```

---

# ✅ Example Valid Input

```json
{
  "name": "John",
  "age": 25,
  "city": "Mumbai"
}
```

### Output

```json
{
  "status": "PASS",
  "error": null,
  "consistency_score": 100
}
```

---

# ❌ Example Invalid Input

```json
{
  "name": "John",
  "age": "Twenty Five"
}
```

### Output

```json
{
  "status": "FAIL",
  "error": "'Twenty Five' is not of type 'integer'",
  "consistency_score": 50
}
```

---

# ▶️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI_Output_Consistency_Validator.git
```

---

## 2️⃣ Navigate to Project

```bash
cd AI_Output_Consistency_Validator
```

---

## 3️⃣ Create Virtual Environment

```bash
python -m venv venv
```

---

## 4️⃣ Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 5️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🚀 Running the Project

## Run FastAPI Backend

```bash
uvicorn api:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger API Docs:

```text
http://127.0.0.1:8000/docs
```

---

## Run Streamlit Dashboard

```bash
streamlit run dashboard.py
```

---

# 🎨 Dashboard Features

The Streamlit dashboard includes:

- Modern SaaS-inspired UI
- Validation analytics cards
- Total / Passed / Failed tracking
- JSON validation panel
- Consistency score display
- Validation history table
- Malformed JSON alerts

=> Images: 
<img width="1919" height="988" alt="Screenshot 2026-06-04 153150" src="https://github.com/user-attachments/assets/75cedaca-dc27-48c9-863a-6b889e3dde23" />
<img width="1919" height="949" alt="Screenshot 2026-06-04 153108" src="https://github.com/user-attachments/assets/d34f1593-8357-4c75-8b38-1553cdc0c4d7" />

---

# 🧪 Test Cases

| Test Case | Expected Result |
|-----------|----------------|
| Valid JSON | PASS |
| Missing Field | FAIL |
| Wrong Data Type | FAIL |
| Extra Field | FAIL |
| Malformed JSON | ERROR |

---

# 📈 Future Improvements

- Multiple Schema Support
- AI Response Comparison
- Export Validation Reports (PDF/CSV)
- User Authentication
- Database Integration
- Real-time Monitoring Dashboard
- Validation Trend Charts

---

# 🎯 Use Cases

- AI Response Validation
- LLM Reliability Testing
- API Response Verification
- Data Quality Monitoring
- Structured Output Enforcement
- AI Testing Pipelines

---

# 📌 Author

### Shravani Sadawarte
### Vedant Nawghare

Python Developer | AI/ML 

---
