from fastapi import FastAPI
import json

from validator import validate_json

app = FastAPI(
    title="AI Output Consistency Validator",
    version="1.0.0"
)

# Load schema once
with open("schemas/user_schema.json") as f:
    schema = json.load(f)


@app.get("/")
def home():
    return {
        "message": "AI Output Consistency Validator Running"
    }


@app.post("/validate")
def validate_response(response: dict):

    return validate_json(response, schema)