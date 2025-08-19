import json


def read_json_file(file: str):
    with open(file + '.json', 'r') as json_file:
        data = json.load(json_file)

    return data
