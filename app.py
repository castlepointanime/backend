from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from create_contract import create_contract

app = Flask(__name__)
CORS(app)

@app.route('/')
def main():
    return jsonify(datetime.now())

@app.route('/contract', methods=['POST'])
def create_contract_route():
    return create_contract(request)