from flask import Flask, render_template, request
from flask_cors import CORS
from chatgpt import get_response

app = Flask(__name__)
CORS(app) # disables CORS


@app.route("/")
def home():
    return render_template("index.html")

# Define route for home page
import json
@app.route("/get", methods=["GET", "POST"])
def gpt_response():
    userText = request.args.get('msg')
    return json.dumps((get_response(userText)))

if __name__ == "__main__":
    app.run(debug=False)