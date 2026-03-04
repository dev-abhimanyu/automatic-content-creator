import json

def get_value(file, key):
    f = open(file)
    data = json.load(f)
    value = data[key]
    f.close()
    return value