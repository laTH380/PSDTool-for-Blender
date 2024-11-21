import json

def save_json_file(data, output_path):
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)