from flask import Flask, request, jsonify, redirect
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies, get_jwt
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from spaced_rep import update_flashcard_review
from database import *

from datetime import timedelta, datetime, timezone
import database
import uuid
import os

import notes
import flashcards

app = Flask(__name__, static_folder="static", static_url_path="/")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
app.config["JWT_COOKIE_SECURE"] = False # TODO: SET TO TRUE IN PROD
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)
bcrypt = Bcrypt(app)
# TODO: REMOVE/RESTRICT CORS AFTER DEVELOPMENT (security risk)
#CORS(app, resources={r"/api/*": {"origins": ["http://localhost:8000", "http://0.0.0.0:8000", "http://127.0.0.1:8000"]}})
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

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
        access_token = create_access_token(identity=uuid)

        response = jsonify({"access_token": access_token})
        set_access_cookies(response, access_token)
        return response
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
        access_token = create_access_token(identity=uuid)
        response = jsonify({"access_token": access_token})
        set_access_cookies(response, access_token)
        return response
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/logout")
def logout():
    response = redirect("/")
    unset_jwt_cookies(response)
    return response

# Using an `after_request` callback, we refresh any token that is within 30
# minutes of expiring. Change the timedeltas to match the needs of your application.
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response

"""
API routes below
"""

@app.route("/api/me", methods=["GET"])
@jwt_required()
def me():
    uuid = get_jwt_identity()
    return jsonify({"uuid": uuid, "email": database.get_user_email(app, uuid)})

# notes section

@app.route("/api/notes", methods=["POST"])
@jwt_required()
def create_note():
    data = request.json
    owner = get_jwt_identity()
    title = data.get("title")
    content = data.get("content")
    note_id = notes.create_note(app, owner, title, content)
    return jsonify({"message": "Note created", "id": note_id})

@app.route("/api/notes", methods=["GET"])
@jwt_required()
def get_notes():
    return jsonify(notes.fetch_all_notes(app, get_jwt_identity()))

@app.route("/api/notes/<note_id>", methods=["GET"])
@jwt_required()
def get_note(note_id):
    return jsonify(notes.fetch_note(app, note_id, get_jwt_identity()))

@app.route("/api/notes/<note_id>", methods=["PUT"])
@jwt_required()
def edit_note(note_id):
    data = request.json
    title = data.get("title")
    content = data.get("content")
    return jsonify({"message": "Note edited" if notes.edit_note(app, note_id, get_jwt_identity(), title, content) else "Failed to edit note"})

@app.route("/api/notes/<note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id): 
    return jsonify({"message": "Note deleted" if notes.delete_note(app, note_id, get_jwt_identity()) else "Failed to delete note"})

# flashcard section

@app.route("/api/flashcards", methods=["POST"])
@jwt_required()
def create_flashcard():
    data = request.json
    owner =  get_jwt_identity()
    front_card = data.get("front_card")
    back_card = data.get("back_card")
    flashcard_id = flashcards.create_flashcard(app, owner, front_card, back_card)
    return jsonify({"message": "Flashcard created", "id": flashcard_id})


@app.route("/api/flashcards", methods=["GET"])
@jwt_required()
def get_flashcards():
    return jsonify(flashcards.fetch_all_flashcards(app, get_jwt_identity()))


@app.route("/api/flashcards/<flashcard_id>", methods=["GET"])
@jwt_required()
def get_flashcard(flashcard_id):
    return jsonify(flashcards.fetch_flashcard(app, flashcard_id, get_jwt_identity()))


@app.route("/api/flashcards/<flashcard_id>", methods=["PUT"])
@jwt_required()
def edit_flashcard(flashcard_id):
    data = request.json
    front_card = data.get("front_card")
    back_card = data.get("back_card")
    flashcards.update_flashcard(app, flashcard_id, get_jwt_identity(), front_card, back_card)
    return jsonify({"message": "Flashcard updated"})


@app.route("/api/flashcards/<flashcard_id>", methods=["DELETE"])
@jwt_required()
def delete_flashcard(flashcard_id): 
    return jsonify({"message": "Flashcard deleted" if flashcards.delete_flashcard(app, flashcard_id, get_jwt_identity()) else "Failed to delete flashcard"})


@app.route("/api/quiz", methods=["GET"])
@jwt_required()
def get_due_flashcards():
    user_id = get_jwt_identity()
    now = datetime.now()
    cards = db.session.execute(
        db.select(UserFlashCard)
        .where(UserFlashCard.owner == user_id, UserFlashCard.due_date <= now)
        .order_by(UserFlashCard.due_date)
    ).scalars()
    return jsonify([
        {'id': card.uuid, 'front_card': card.front, 'back_card': card.back}
        for card in cards
    ])

@app.route("/api/quiz/<flashcard_id>", methods=["POST"])
@jwt_required()
def review_flashcard(flashcard_id):
    """
    Accepts a quality score (i.e 0-5) and updates spaced rep stats
    """
    user_id = get_jwt_identity()
    data = request.json
    quality = int(data.get("quality", 0))

    card = db.session.execute(
        db.select(UserFlashCard)
        .where(UserFlashCard.uuid == flashcard_id, UserFlashCard.owner == user_id)
    ).scalar_one_or_none()
    if not card:
        return jsonify({"error": "Flashcard not found"}), 404

    card = update_flashcard_review(card, quality)
    db.session.commit()
    return jsonify({"message": "Review updated"})