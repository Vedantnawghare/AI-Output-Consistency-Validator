from json_parser import parse_json

response = '{name:"John"}'

parsed = parse_json(response)

if parsed is None:
    print("Malformed JSON detected")
else:
    print(parsed)