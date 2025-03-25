from flask import Flask, request, jsonify
import database
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
import init_db
import notes
import flashcards


app = Flask(__name__, static_folder="static", static_url_path="/")

# I wasn't completely sure how we wanted to format the notes so I made a table with postgresql, located in init_db
with app.app_context():
    init_db.create_table()


app.config["JWT_SECRET_KEY"] = "supersecret"  
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

CORS(app)


hardcoded_users = {
    "ashaan@ufl.edu": bcrypt.generate_password_hash("password").decode("utf-8"),
    "test1@example.com": bcrypt.generate_password_hash("abc123").decode("utf-8"),
    "test2@example.com": bcrypt.generate_password_hash("qwerty").decode("utf-8"),
    "test3@example.com": bcrypt.generate_password_hash("secret").decode("utf-8")
}


@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file("index.html")

@app.route("/test")
def test():
    return "<p>Hello, {}!</p>".format(database.getCurrentDatabase())

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

    if email in hardcoded_users and bcrypt.check_password_hash(hardcoded_users[email], password):
        # Create JWT
        token = create_access_token(identity=email)
        return jsonify({"access_token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401



'''
I tested all of these functions using POSTMAN but they are pretty self explanatory, I don't have much experience using 
React so I returned all of them as json b/c that's what it said in the tutorials I watched, lmk what to change
'''


@app.route("/notes", methods=["POST"])
def create_note():
    data = request.json
    title = data.get("title")
    content = data.get("content")
    note_id = notes.create_note(title, content)
    return jsonify({"message": "Note created", "id": note_id})


@app.route("/notes", methods=["GET"])
def get_notes():
    all_notes = notes.fetch_all_notes()
    return jsonify(all_notes)


@app.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    note = notes.fetch_note(note_id)
    return jsonify(note)


@app.route("/notes/<int:note_id>", methods=["PUT"])
def edit_note(note_id):
    data = request.json
    title = data.get("title")
    content = data.get("content")
    notes.edit_note(note_id, title, content)
    return jsonify({"message": "Note Edited"})


@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    notes.delete_note(note_id)
    return jsonify({"message": "Note deleted"})


# flashcard section

@app.route("/flashcards", methods=["POST"])
def create_flashcard():
    data = request.json
    front_card = data.get("front_card")
    back_card = data.get("back_card")
    flashcard_id = flashcards.create_flashcard(front_card, back_card)
    return jsonify({"message": "Flashcard created", "id": flashcard_id})


@app.route("/flashcards", methods=["GET"])
def get_flashcards():
    all_flashcards = flashcards.fetch_all_flashcards()
    return jsonify(all_flashcards)


@app.route("/flashcards/<int:flashcard_id>", methods=["GET"])
def get_flashcard(flashcard_id):
    card = flashcards.fetch_flashcard(flashcard_id)
    return jsonify(card)


@app.route("/flashcards/<int:flashcard_id>", methods=["PUT"])
def edit_flashcard(flashcard_id):
    data = request.json
    front_card = data.get("front_card")
    back_card = data.get("back_card")
    flashcards.update_flashcard(flashcard_id, front_card, back_card)
    return jsonify({"message": "Flashcard updated"})


@app.route("/flashcards/<int:flashcard_id>", methods=["DELETE"])
def delete_flashcard(flashcard_id):
    flashcards.delete_flashcard(flashcard_id)
    return jsonify({"message": "Flashcard deleted"})






if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)