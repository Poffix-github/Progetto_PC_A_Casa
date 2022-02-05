from utilities.json_opener import read

def full_name(filepath, model, topic):
    data = read(filepath)
    for i, key in enumerate(data):
        if topic == i:
            return data[key] + model
