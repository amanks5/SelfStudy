from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
import database
import os

app = Flask(__name__, static_folder="static", static_url_path="/")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABSE_URI")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)
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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
