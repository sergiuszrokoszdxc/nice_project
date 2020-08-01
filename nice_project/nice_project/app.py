import random

from flask import Flask
from flask import render_template
from flask import request

flask_app = Flask(__name__)

memory = []

@flask_app.route("/show", methods=["GET"])
def show():
    try:
        random_element = random.choice(memory)
    except IndexError:
        random_element = ""
    return render_template(
        "show.html",
        random_element=random_element
        )

@flask_app.route("/submit", methods=["GET", "POST"])
def submit():
    thanks = False
    if request.method == "POST":
        compliment = request.form.get("compliment")
        memory.append(compliment)
        thanks = True
    # TODO: What if wrong form
    return render_template(
        "submit.html",
        thanks=thanks
        )

@flask_app.route("/index")
def index():
    # TODO: Add a game
    return render_template("index.html")