import json


def parse_json(ai_output):

    try:
        return json.loads(ai_output)

    except json.JSONDecodeError:

        return None