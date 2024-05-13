from flask import Flask, request, jsonify
import searchingdatabase 
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', default='', type=str)
    threshold = request.args.get('threshold', default=70, type=int)
    results = searchingdatabase.fuzzy_search_summary(query, threshold)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
