from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
import database
import uuid
import os

import notes
import flashcards

app = Flask(__name__, static_folder="static", static_url_path="/")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABSE_URI")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app) # TODO: REMOVE/RESTRICT CORS AFTER DEVELOPMENT (security risk)
database.init(app)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    """
    Simple signup route:
    Expects JSON: { "email": "...", "password": "..." }
    Returns JWT token if successful
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")

    uuid = database.signup(app, bcrypt, email, password)
    if uuid is not None:
        # Create JWT
        token = create_access_token(identity=uuid)
        return jsonify({"access_token": token}), 200
    else:
        return jsonify({"error": "Failed to signup"}), 401

@app.route("/login", methods=["POST"])
def login():
    """
    Simple login route:
    Expects JSON: { "email": "...", "password": "..." }
    Returns JWT token if successful
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")

    uuid = database.login(app, bcrypt, email, password)
    if uuid is not None:
        # Create JWT
        token = create_access_token(identity=uuid)
        return jsonify({"access_token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


'''
I tested all of these functions using POSTMAN but they are pretty self explanatory, I don't have much experience using 
React so I returned all of them as json b/c that's what it said in the tutorials I watched, lmk what to change
'''
### TODO: authenticate requests
### TODO: api url prefix

@app.route("/notes", methods=["POST"])
def create_note():
    data = request.json
    owner = uuid.uuid4() # TODO: get note owner from session (just setting owner to random id to random rn)
    title = data.get("title")
    content = data.get("content")
    note_id = notes.create_note(app, owner, title, content)
    return jsonify({"message": "Note created", "id": note_id})


@app.route("/notes", methods=["GET"])
def get_notes():
    all_notes = notes.fetch_all_notes(app)
    return jsonify(all_notes)


@app.route("/notes/<note_id>", methods=["GET"])
def get_note(note_id):
    note = notes.fetch_note(app, note_id)
    return jsonify(note)


@app.route("/notes/<note_id>", methods=["PUT"])
def edit_note(note_id):
    data = request.json
    title = data.get("title")
    content = data.get("content")
    notes.edit_note(app, note_id, title, content)
    return jsonify({"message": "Note Edited"})


@app.route("/notes/<note_id>", methods=["DELETE"])
def delete_note(note_id): 
    return jsonify({"message": "Note deleted" if notes.delete_note(app, note_id) else "Failed to delete note"})


# flashcard section

@app.route("/flashcards", methods=["POST"])
def create_flashcard():
    data = request.json
    owner = uuid.uuid4() # TODO: get note owner from session (just setting owner to random id to random rn)
    front_card = data.get("front_card")
    back_card = data.get("back_card")
    flashcard_id = flashcards.create_flashcard(app, owner, front_card, back_card)
    return jsonify({"message": "Flashcard created", "id": flashcard_id})


@app.route("/flashcards", methods=["GET"])
def get_flashcards():
    all_flashcards = flashcards.fetch_all_flashcards(app)
    return jsonify(all_flashcards)


@app.route("/flashcards/<flashcard_id>", methods=["GET"])
def get_flashcard(flashcard_id):
    card = flashcards.fetch_flashcard(app, flashcard_id)
    return jsonify(card)


@app.route("/flashcards/<flashcard_id>", methods=["PUT"])
def edit_flashcard(flashcard_id):
    data = request.json
    front_card = data.get("front_card")
    back_card = data.get("back_card")
    flashcards.update_flashcard(app, flashcard_id, front_card, back_card)
    return jsonify({"message": "Flashcard updated"})


@app.route("/flashcards/<flashcard_id>", methods=["DELETE"])
def delete_flashcard(flashcard_id): 
    return jsonify({"message": "Flashcard deleted" if flashcards.delete_flashcard(app, flashcard_id) else "Failed to delete flashcard"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
