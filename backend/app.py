from flask import Flask, request, jsonify
import database
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt


app = Flask(__name__, static_folder="static", static_url_path="/")


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




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)