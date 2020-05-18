import datetime

from flask import Flask
from flask import render_template

from nice_project.utils.memory import Memory
from nice_project.utils.stoper import Stoper

flask_app = Flask(__name__, static_folder="../nginx/static")

memory = Memory(8)


def store_with_time(value):
    return datetime.datetime.now(), value


function = store_with_time
stoper = Stoper(memory, function)


@flask_app.route("/")
def index():
    iterable = stoper.get_stored()
    return render_template("index.html", iterable=iterable)


@flask_app.route("/store/<string:text>")
def save_text(text):
    stoper.stop(text)
    iterable = stoper.get_stored()
    return render_template("index.html", iterable=iterable)
