import flask
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

SOLR_URL = 'http://localhost:8983/solr/Ayesha_collection_shard1_replica_n1/select'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()

    # If query is empty, return all documents
    if not query:
        solr_query = '*:*'  # This will fetch all records
    else:
        solr_query = f'title:{query} OR author:{query} OR id:{query}'

    params = {
        'q': solr_query,
        'wt': 'json',
        'rows': 20
    }

    response = requests.get(SOLR_URL, params=params)
    print("STATUS CODE:", response.status_code)
    print("RESPONSE TEXT:", response.text)

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        return f"Invalid JSON response: {response.text}", 500

    docs = data['response']['docs']
    return jsonify(docs)

if __name__ == '__main__':
    app.run(debug=True)
