import os
import json
def get_file_info(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
            except OSError:
                file_size = 0
            file_info = {
                "file_name": file,
                "file_path": file_path,
                "file_size": file_size
            }
            file_list.append(file_info)
    return file_list
def structure_files(file_list, base_path):
    file_structure = {}
    for file_info in file_list:
        path_parts = file_info['file_path'].replace(base_path, '').strip(os.sep).split(os.sep)
        cursor = file_structure
        for part in path_parts[:-1]:  
            if part not in cursor:
                cursor[part] = {} 
            cursor = cursor[part]
        if 'files' not in cursor:
            cursor['files'] = [] 
        cursor['files'].append({
            "file_name": file_info['file_name'],
            "file_path": file_info['file_path'],
            "file_size": file_info['file_size']
        })
    return file_structure
base_directory = "/Users/nvgenomics/Desktop/hostingdata/Database"
file_infos = get_file_info(base_directory)
structured_data = structure_files(file_infos, base_directory)
with open('file_structure.json', 'w') as json_file:
    json.dump(structured_data, json_file, indent=4)
print("JSON file created successfully!")
