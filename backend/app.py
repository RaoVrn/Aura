from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
from dotenv import load_dotenv
from gemini_rag import ask_gemini  # fallback if not streaming
from command_handler import handle_create_command  # Import the new module

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

@app.route('/ask', methods=['POST'])
def ask():
    """API endpoint to handle user queries"""
    data = request.json
    user_query = data.get("query", "").strip()
    
    if not user_query:
        return jsonify({"error": "Query cannot be empty"}), 400

    # Check if the query is a file or folder creation command.
    if user_query.lower().startswith("create a "):
        creation_result = handle_create_command(user_query)
        if creation_result:
            return jsonify(creation_result)
        else:
            return jsonify({"response": "Creation command could not be processed."})
    
    # For non-creation queries, produce the full response at once.
    def generate():
        try:
            # If a streaming function is available, accumulate all chunks first.
            if hasattr(ask_gemini, "stream") and callable(ask_gemini.stream):
                full_response = ""
                for chunk in ask_gemini.stream(user_query):
                    full_response += chunk
                yield f"data:{full_response}\n\n"
            else:
                full_response = ask_gemini(user_query)
                yield f"data:{full_response}\n\n"
        except Exception as e:
            yield f"data:Error: {str(e)}\n\n"
    
    return Response(generate(), mimetype="text/event-stream")

@app.route("/api/create-folder", methods=["POST"])
def create_folder():
    data = request.json
    folder_name = data.get("folder_name", "").strip()
    if not folder_name:
        return jsonify({"error": "Folder name is required."}), 400

    user_home = os.path.expanduser("~")
    onedrive_desktop = os.path.join(user_home, "OneDrive", "Desktop")
    desktop_path = onedrive_desktop if os.path.exists(onedrive_desktop) else os.path.join(user_home, "Desktop")
    path = os.path.join(desktop_path, folder_name)
    
    try:
        os.makedirs(path, exist_ok=True)
        return jsonify({"message": f"Folder '{folder_name}' created successfully at {path}!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
