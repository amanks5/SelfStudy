from flask import Flask
import database

app = Flask(__name__, static_folder="static", static_url_path="/")

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/test")
def test():
    return "<p>Hello, {}!</p>".format(database.getCurrentDatabase())
