import psycopg2
import os
import re

def extract_section(content, section_name):
    # Use regex to extract content safely, assuming dollar signs are used to mark the content
    pattern = rf"{section_name}\s*\$\s*(.+?)\s*\$"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None  # Return None if no content found, better for checking absence

def update_database(conn, file_id, summary, function, phy_effect, structure, behaviour, action, state):
    cur = conn.cursor()
    try:
        # Update the database with all sections
        cur.execute("""
            UPDATE FILE SET 
            summary = %s, 
            function = %s,
            phy_effect = %s,
            structure = %s,
            behaviour = %s,
            action = %s,
            state = %s 
            WHERE file_id = %s;
        """, (summary, function, phy_effect, structure, behaviour, action, state, file_id))
        conn.commit()
        print(f"Successfully updated File ID: {file_id}")
    except psycopg2.DatabaseError as e:
        print(f"Database error while updating file ID {file_id}: {e}")
    finally:
        cur.close()

def fetch_and_display_text_files():
    conn = psycopg2.connect(
        dbname="IP",
        user="yash",
        password="yash",
        host="localhost",
        port="5433"
    )
    cur = conn.cursor()
    try:
        # Ensure all necessary columns exist
        cur.execute("ALTER TABLE FILE ADD COLUMN IF NOT EXISTS summary TEXT;")
        cur.execute("ALTER TABLE FILE ADD COLUMN IF NOT EXISTS function TEXT;")
        cur.execute("ALTER TABLE FILE ADD COLUMN IF NOT EXISTS phy_effect TEXT;")
        cur.execute("ALTER TABLE FILE ADD COLUMN IF NOT EXISTS structure TEXT;")
        cur.execute("ALTER TABLE FILE ADD COLUMN IF NOT EXISTS behaviour TEXT;")
        cur.execute("ALTER TABLE FILE ADD COLUMN IF NOT EXISTS action TEXT;")
        cur.execute("ALTER TABLE FILE ADD COLUMN IF NOT EXISTS state TEXT;")
        conn.commit()

        cur.execute("SELECT file_id, file_name, file_path FROM FILE WHERE file_type = 'txt'")
        records = cur.fetchall()

        for record in records:
            file_id, file_name, file_path = record
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        sections = {
                            'summary': extract_section(content, "SUMMARY"),
                            'function': extract_section(content, "FUNCTION"),
                            'phy_effect': extract_section(content, "PHYEFFECT"),
                            'structure': extract_section(content, "STRUCTURE"),
                            'behaviour': extract_section(content, "BEHAVIOUR"),
                            'action': extract_section(content, "ACTION"),
                            'state': extract_section(content, "STATE")
                        }
                        if any(value is not None for value in sections.values()):
                            update_database(conn, file_id, **sections)
                        else:
                            print(f"Missing content in {file_name} (ID: {file_id})")
                except Exception as e:
                    print(f"Error reading file {file_name} (ID: {file_id}): {e}")
            else:
                print(f"File not found at path: {file_path}")

    except Exception as e:
        print(f"Database or file operation error: {e}")
    finally:
        cur.close()
        conn.close()

fetch_and_display_text_files()
