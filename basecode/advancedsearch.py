import psycopg2
from fuzzywuzzy import fuzz

def fetch_data_and_search(conn, search_inputs):
    cur = conn.cursor()
    try:
        # Join the FILE table with the MAIN_FOLDER table on folder_id to get folder_name
        cur.execute("""
            SELECT 
                f.file_id, f.file_name, f.summary, f.function, f.phy_effect, 
                f.structure, f.behaviour, f.action, f.state, m.folder_name
            FROM FILE f
            JOIN MAIN_FOLDER m ON f.folder_id = m.folder_id
        """)
        records = cur.fetchall()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    best_matches = []

    # Evaluate each record
    for record in records:
        # Dictionary to hold the best score for each field
        best_field_scores = {field: 0 for field in ['summary', 'function', 'phy_effect', 'structure', 'behaviour', 'action', 'state']}
        
        # Iterate through each field and its corresponding input search term
        for field_index, field_name in enumerate(best_field_scores.keys(), start=2): # Start from index 2 to skip file_id and file_name
            input_term = search_inputs[field_index - 2]  # Adjust index for input terms list
            if record[field_index] and input_term:  # Ensure both the field and input are non-empty
                score = fuzz.partial_ratio(input_term.lower(), record[field_index].lower())
                best_field_scores[field_name] = max(best_field_scores[field_name], score)

        # Add the record and the highest score from any field to the best_matches list
        if any(score > 50 for score in best_field_scores.values()):  # Check if any field score is above 50
            highest_score = max(best_field_scores.values())
            best_matches.append((highest_score, record))

    # Sort by the highest scores
    best_matches.sort(reverse=True, key=lambda x: x[0])

    # Print the top result with summary, action, state, and folder name
    print("Top matching records:")
    if best_matches:
        score, match = best_matches[0]  # Take the top match
        print(f"Match Score: {score}%")
        print(f"File ID: {match[0]}, File Name: {match[1]}")
        print(f"Folder Name: {match[9]}")
        print(f"Summary: {match[2]}")
        print(f"Action: {match[7]}")
        print(f"State: {match[8]}")
    else:
        print("No matches found.")

def main():
    conn = psycopg2.connect(
        dbname="IP",
        user="yash",
        password="yash",
        host="localhost",
        port="5433"
    )
    # Collect inputs for each field
    fields = ['summary', 'function', 'phy_effect', 'structure', 'behaviour', 'action', 'state']
    search_inputs = []
    for field in fields:
        term = input(f"Enter search terms for {field} (leave empty if not applicable): ")
        search_inputs.append(term)

    fetch_data_and_search(conn, search_inputs)

    conn.close()

main()
