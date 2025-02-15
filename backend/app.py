import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv  # Import dotenv

# Load .env file
load_dotenv()

# Get API Key from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)

def get_ai_response(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text if response else "Sorry, I couldn't process that."

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_query = data.get("query", "")
    response = get_ai_response(user_query)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
