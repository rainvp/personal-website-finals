from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
import uuid

app = Flask(__name__)
CORS(app)

# Supabase setup
SUPABASE_URL = "https://kbhnxlrhbxamkgwyqpjn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtiaG54bHJoYnhhbWtnd3lxcGpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg0Njc3NzEsImV4cCI6MjA1NDA0Mzc3MX0.lCXlrIXQaw3BvkzR9SBLGuxXnDAIscdkzcUpnn0KR-8"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Helper function to validate UUID
def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False
    
@app.route('/')
def home():
    return "Welcome to the Guestbook API! Use Postman to interact with it."

    
@app.route('/guestbook', methods=['GET'])
def get_guestbook_entries():
    try:
        response = supabase.from_('guestbook').select("name, message").execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/guestbook', methods=['POST'])
def add_guestbook_entry():
    data = request.json
    if not data.get("name"):
        return jsonify({"error": "Name is required"}), 400
    
    try:
        response = supabase.from_('guestbook').insert([{
            "name": data["name"],
            "email": data.get("email", ""),  
            "message": data.get("message", "")
        }]).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

