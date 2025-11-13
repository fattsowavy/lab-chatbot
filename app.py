from flask import Flask, render_template, request, jsonify
from utils import match_category, generate_response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "").strip()
    if not user_msg:
        return jsonify({"response": "Tulis pertanyaan dulu!"})

    category = match_category(user_msg)
    bot_response = generate_response(category, user_msg)

    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)