from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client

app = Flask(__name__)
CORS(app)

# Supabase setup
SUPABASE_URL = "https://kbhnxlrhbxamkgwyqpjn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtiaG54bHJoYnhhbWtnd3lxcGpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg0Njc3NzEsImV4cCI6MjA1NDA0Mzc3MX0.lCXlrIXQaw3BvkzR9SBLGuxXnDAIscdkzcUpnn0KR-8"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch user ID from guestbook
def get_user_id(email):
    response = supabase.from_("guestbook").select("id").eq("email", email).execute()
    if response.data and isinstance(response.data, list) and len(response.data) > 0:
        return response.data[0]["id"]
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
    if not response.data or len(response.data) == 0:
        return jsonify({"error": "User not found"}), 404

    # Check if the user already reacted
    existing_reaction = supabase.from_("comment_reactions").select("*")\
        .eq("comment_id", comment_id).eq("user_email", user_email).execute()

    if existing_reaction.data and len(existing_reaction.data) > 0:
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


import uuid

@app.route('/get_reactions', methods=['GET'])
def get_reactions():
    comment_id = request.args.get("comment_id")
    if not comment_id:
        return jsonify({"error": "Missing comment_id"}), 400

    try:
        # Convert comment_id to a valid UUID format
        comment_id = str(uuid.UUID(comment_id))
    except ValueError:
        return jsonify({"error": "Invalid comment_id format"}), 400

    response = supabase.from_("comment_reactions").select("*").eq("comment_id", comment_id).execute()
    
    reactions = {"laughs": 0, "loves": 0, "dislikes": 0}
    for reaction in response.data:
        if reaction["reaction_type"] in reactions:
            reactions[reaction["reaction_type"]] += 1

    return jsonify({"reactions": reactions})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)


