import json
import psycopg2

def generate_abbreviation(folder_name):
    words = folder_name.split()
    abbreviation = ''
    for word in words:
        abbreviation += word[0].upper()
        if len(abbreviation) >= 4:
            break
    if len(abbreviation) < 4:
        abbreviation += folder_name[:4 - len(abbreviation)].upper()
    return abbreviation

conn = psycopg2.connect(
    dbname="IP",
    user="yash",
    password="yash",
    host="localhost",
    port="5433"
)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS MAIN_FOLDER (
        folder_id SERIAL PRIMARY KEY,
        folder_name VARCHAR(255) NOT NULL,
        abbreviation VARCHAR(10)  -- Added abbreviation column
    )
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS FILE (
        file_id SERIAL PRIMARY KEY,
        file_name VARCHAR(255) NOT NULL,
        file_path TEXT NOT NULL,
        file_size INTEGER,
        file_type VARCHAR(100),
        folder_id INTEGER REFERENCES MAIN_FOLDER(folder_id) ON DELETE CASCADE
    )
""")

conn.commit()

with open("file_structure.json", "r") as f:
    data = json.load(f)

for main_folder, subfolders_data in data.items():
    abbreviation = generate_abbreviation(main_folder)
    cur.execute("INSERT INTO MAIN_FOLDER (folder_name, abbreviation) VALUES (%s, %s) RETURNING folder_id", (main_folder, abbreviation))
    main_folder_id = cur.fetchone()[0]
    print(f"Inserted main folder: {main_folder} (ID: {main_folder_id})")
    
    for subfolder, content in subfolders_data.items():
        # Check if content is a dictionary and has the 'files' key
        if isinstance(content, dict) and 'files' in content:
            files = content['files']
            for file_data in files:
                file_name = file_data["file_name"]
                file_path = file_data["file_path"]
                file_size = file_data["file_size"]
                file_type = file_path.split(".")[-1]
                cur.execute("INSERT INTO FILE (file_name, file_path, file_size, file_type, folder_id) VALUES (%s, %s, %s, %s, %s)",
                            (file_name, file_path, file_size, file_type, main_folder_id))
                print(f"Inserted file: {file_name} in main folder: {main_folder}")
        else:
            print(f"Skipping invalid data format in subfolder: {subfolder}")

conn.commit()
cur.close()
conn.close()
