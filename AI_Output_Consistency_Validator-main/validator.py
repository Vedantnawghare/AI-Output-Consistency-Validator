from jsonschema import validate
from jsonschema.exceptions import ValidationError


def validate_json(data, schema):

    report = {
        "status": "PASS",
        "error": None,
        "consistency_score": 100
    }

    try:
        validate(instance=data, schema=schema)

    except ValidationError as e:

        report["status"] = "FAIL"
        report["error"] = e.message
        report["consistency_score"] = 50

    return report