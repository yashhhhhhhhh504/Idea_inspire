import json
import re

def extract_section(text, section_name):
    # Adjust the regex to look for the section name followed by any characters until it finds $, then capture everything until the next $
    pattern = rf"{section_name}\s*\n\$\s*(.*?)\s*\$"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return f"No {section_name.lower()} found."

def process_files(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    for category_data in data['SPECIAL'].values():
        for file_info in category_data['files']:
            file_path = file_info['file_path']
            if file_info['file_name'].endswith('.txt'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        summary = extract_section(content, "SUMMARY")
                        function = extract_section(content, "FUNCTION")
                        phy_effect = extract_section(content, "PHYEFFECT")
                        structure = extract_section(content, "STRUCTURE")
                        behaviour = extract_section(content, "BEHAVIOUR")
                        action = extract_section(content, "ACTION")
                        state = extract_section(content, "STATE")  # Extract the STATE section
                        print(f"File ID: {file_info['file_name']}")
                        print("FUNCTION CONTENT:")
                        print(function)
                        print("\nSUMMARY CONTENT:")
                        print(summary)
                        print("\nPHYEFFECT CONTENT:")
                        print(phy_effect)
                        print("\nSTRUCTURE CONTENT:")
                        print(structure)
                        print("\nBEHAVIOUR CONTENT:")
                        print(behaviour)
                        print("\nACTION CONTENT:")
                        print(action)
                        print("\nSTATE CONTENT:")  # Print the STATE content
                        print(state)
                        print("\n" + "="*50 + "\n")
                except FileNotFoundError:
                    print(f"File not found: {file_path}")
                except UnicodeDecodeError:
                    # If UTF-8 fails, try reading with Latin-1 encoding
                    with open(file_path, 'r', encoding='latin-1') as file:
                        content = file.read()
                        summary = extract_section(content, "SUMMARY")
                        function = extract_section(content, "FUNCTION")
                        phy_effect = extract_section(content, "PHYEFFECT")
                        structure = extract_section(content, "STRUCTURE")
                        behaviour = extract_section(content, "BEHAVIOUR")
                        action = extract_section(content, "ACTION")
                        state = extract_section(content, "STATE")  # Re-attempt to extract STATE
                        print(f"File ID: {file_info['file_name']}")
                        print("FUNCTION CONTENT:")
                        print(function)
                        print("\nSUMMARY CONTENT:")
                        print(summary)
                        print("\nPHYEFFECT CONTENT:")
                        print(phy_effect)
                        print("\nSTRUCTURE CONTENT:")
                        print(structure)
                        print("\nBEHAVIOUR CONTENT:")
                        print(behaviour)
                        print("\nACTION CONTENT:")
                        print(action)
                        print("\nSTATE CONTENT:")
                        print(state)
                        print("\n" + "="*50 + "\n")

# Call the function with the path to your JSON configuration file
process_files('/Users/nvgenomics/Desktop/hostingdata/file_structure.json')
