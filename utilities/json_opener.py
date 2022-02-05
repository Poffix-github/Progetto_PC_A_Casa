from json import load


def read(path):
    with open(path, 'r') as f:
        return load(f)
