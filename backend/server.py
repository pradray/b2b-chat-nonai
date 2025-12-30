from flask import Flask, request, jsonify
from lambda_function import lambda_handler
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enable CORS so Vite (Port 5173) can talk to Flask (Port 5000)

@app.route('/chat', methods=['POST'])
def chat():
    event = {'body': request.json}
    lambda_response = lambda_handler(event, None)
    return lambda_response['body'], lambda_response['statusCode']

if __name__ == '__main__':
    print("Running Local Python Server on Port 5000...")
    app.run(port=5000)