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

# Fetch user ID from guestbook
def get_user_id(email):
    response = supabase.from_("guestbook").select("id").eq("email", email).execute()
    
    if response.get("error"):
        return None  # Handle error properly
    
    data = response.get("data", [])
    if data and isinstance(data, list) and data:
        return data[0]["id"]
    return None

@app.route('/toggle_reaction', methods=['POST'])
def toggle_reaction():
    data = request.json
    comment_id = data.get("comment_id")
    reaction_type = data.get("reaction_type")
    user_email = data.get("user_email")

    if not comment_id or not reaction_type or not user_email:
        return jsonify({"error": "Missing data"}), 400

    # Check if user exists in guestbook
    response = supabase.from_("guestbook").select("*").eq("email", user_email).execute()
    if response.get("error") or not response.get("data"):
        return jsonify({"error": "User not found"}), 404

    # Check if the user already reacted
    existing_reaction = supabase.from_("comment_reactions").select("*")\
        .eq("comment_id", comment_id).eq("user_email", user_email).execute()

    if existing_reaction.get("data"):
        # Remove reaction if it exists
        supabase.from_("comment_reactions").delete()\
            .eq("comment_id", comment_id).eq("user_email", user_email).execute()
        return jsonify({"message": "Reaction removed", "reaction_type": reaction_type})

    else:
        # Add new reaction
        supabase.from_("comment_reactions").insert({
            "comment_id": comment_id,
            "reaction_type": reaction_type,
            "user_email": user_email
        }).execute()
        return jsonify({"message": "Reaction added", "reaction_type": reaction_type})

@app.route('/get_reactions', methods=['GET'])
def get_reactions():
    comment_id = request.args.get("comment_id")
    if not comment_id or not is_valid_uuid(comment_id):
        return jsonify({"error": "Invalid or missing comment_id"}), 400

    response = supabase.from_("comment_reactions").select("*").eq("comment_id", comment_id).execute()
    
    if response.get("error"):
        return jsonify({"error": "Database error"}), 500

    reactions = {"laughs": 0, "loves": 0, "dislikes": 0}
    for reaction in response.get("data", []):
        if reaction["reaction_type"] in reactions:
            reactions[reaction["reaction_type"]] += 1

    return jsonify({"reactions": reactions})

if __name__ == '__main__':
    app.run()
