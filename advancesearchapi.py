from flask import Flask, request, jsonify
import psycopg2
from fuzzywuzzy import fuzz
import logging
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_data_and_search(conn, search_inputs):
    cur = conn.cursor()
    results = []
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

        best_matches = []
        # Evaluate each record
        for record in records:
            best_field_scores = {field: 0 for field in ['summary', 'function', 'phy_effect', 'structure', 'behaviour', 'action', 'state']}
            for field_index, field_name in enumerate(best_field_scores.keys(), start=2): # Start from index 2 to skip file_id and file_name
                input_term = search_inputs[field_index - 2]
                if record[field_index] and input_term:
                    score = fuzz.partial_ratio(input_term.lower(), record[field_index].lower())
                    best_field_scores[field_name] = max(best_field_scores[field_name], score)

            if any(score > 50 for score in best_field_scores.values()):
                highest_score = max(best_field_scores.values())
                best_matches.append((highest_score, record))

        # Sort by the highest scores and take the top two matches
        best_matches.sort(reverse=True, key=lambda x: x[0])
        results = best_matches[:2]

    except Exception as e:
        logging.error(f"Error fetching data: {e}")
    finally:
        cur.close()

    return results

@app.route('/search', methods=['GET'])
def search():
    logging.info("Received search request with parameters: %s", request.args)
    # Collect inputs for each field
    fields = ['summary', 'function', 'phy_effect', 'structure', 'behaviour', 'action', 'state']
    search_inputs = [request.args.get(field, '') for field in fields]

    # Database connection setup
    conn = psycopg2.connect(
        dbname="IP",
        user="yash",
        password="yash",
        host="localhost",
        port="5433"
    )

    # Fetch and process the search
    matches = fetch_data_and_search(conn, search_inputs)
    conn.close()

    # Prepare and return the results
    result_data = [{
        "score": match[0],
        "file_id": match[1][0],
        "file_name": match[1][1],
        "summary": match[1][2],
        "action": match[1][7],
        "state": match[1][8],
        "folder_name": match[1][9]
    } for match in matches]

    logging.info("Returning results: %s", result_data)
    return jsonify(result_data)

if __name__ == '__main__':
    app.run(debug=True)
