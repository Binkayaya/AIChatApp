from flask import Flask, render_template, request, redirect, session, url_for
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("Gemini_API_KEY")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat(history=[])

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for using session

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            session["username"] = name
            return redirect(url_for("chatbot"))
    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chatbot():
    username = session.get("username")
    if not username:
        return redirect(url_for("index"))

    user_message = ""
    bot_response = ""

    if request.method == "POST":
        user_message = request.form["message"]
        response = chat.send_message(user_message)
        bot_response = response.text

    return render_template("chat.html", user_message=user_message, bot_response=bot_response, username=username)

if __name__ == "__main__":
    app.run(debug=True)
