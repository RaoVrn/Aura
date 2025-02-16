from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from gemini_rag import ask_gemini

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

@app.route('/ask', methods=['POST'])
def ask():
    """API endpoint to handle user queries"""
    data = request.json
    user_query = data.get("query", "")
    
    if not user_query:
        return jsonify({"error": "Query cannot be empty"}), 400

    response = ask_gemini(user_query)
    return jsonify({"response": response})

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
