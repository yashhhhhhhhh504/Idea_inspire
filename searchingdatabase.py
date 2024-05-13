import psycopg2
from fuzzywuzzy import fuzz

def connect_db():
    return psycopg2.connect(
        dbname="IP",
        user="yash",
        password="yash",
        host="localhost",
        port="5433"
    )

def fuzzy_search_summary(search_query, threshold=70):
    conn = connect_db()
    cur = conn.cursor()
    # Adjust the query to include a JOIN with MAIN_FOLDER and select the folder_name
    cur.execute("""
        SELECT f.file_id, f.file_name, f.summary, m.folder_name
        FROM FILE f
        JOIN MAIN_FOLDER m ON f.folder_id = m.folder_id
        WHERE f.summary IS NOT NULL;
    """)
    results = cur.fetchall()
    matches = []
    for file_id, file_name, summary, folder_name in results:
        score = fuzz.partial_ratio(search_query.lower(), summary.lower())
        if score >= threshold:
            matches.append({
                'file_id': file_id,
                'file_name': file_name,
                'summary': summary,
                'folder_name': folder_name,  # Include the folder name in the results
                'score': score
            })
    cur.close()
    conn.close()

    # Sort matches by score in descending order and limit to the top 2
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches[:1]  # Return only the top 2 matches
