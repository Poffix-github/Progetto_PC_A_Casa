import json


def read(path):
    with open(path, 'r') as f:
        return json.load(f)
