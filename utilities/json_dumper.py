from json import dump

def write(path, data):
    with open(path, 'r+') as f:
        return dump(data, f)
