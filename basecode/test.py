import psycopg2

def print_database_table():
    conn = psycopg2.connect(
        dbname="IP",
        user="yash",
        password="yash",
        host="localhost",
        port="5433"
    )
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT 
                file_id,
                file_name,
                file_path,
                file_size,
                file_type,
                folder_id,
                summary,
                function,
                phy_effect,
                structure,
                behaviour,
                action,
                state
            FROM FILE
        """)
        records = cur.fetchall()

        # Printing the headers
        headers = [
            "file_id", "file_name", "file_path", "file_size", "file_type",
            "folder_id", "summary", "function", "phy_effect", "structure",
            "behaviour", "action", "state"
        ]
        print("|".join(headers))

        # Printing the rows
        for row in records:
            print("|".join(str(item) for item in row))

    except Exception as e:
        print(f"Database query error: {e}")
    finally:
        cur.close()
        conn.close()

print_database_table()
