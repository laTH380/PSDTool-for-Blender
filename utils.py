import json

def dict2jsonstring(data):
    json_data = json.dumps(data)
    return json_data

def jsonstring2dict(data):
    return json.loads(data)

def save_json_file(data, output_path):
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)