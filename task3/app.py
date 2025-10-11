from flask import Flask, jsonify
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_analysis import run_analysis


app = Flask(__name__)

@app.route('/')
def home():
	return jsonify({"message": " Nutritional Insights API is running!"})

@app.route('/analyze', methods=['GET'])
def analyze():
	summary = run_analysis()
	return jsonify(summary)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
