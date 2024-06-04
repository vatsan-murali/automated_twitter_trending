from flask import Flask, render_template, jsonify
from twitConn import fetch_twitter_trends

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/run_script', methods=['GET'])
def run_script():
    data = fetch_twitter_trends()
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch Twitter trends"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
