import json

def load_json(path):
    with open(path, "r") as read_file:
        return json.load(read_file)