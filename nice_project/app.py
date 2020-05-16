import datetime

from flask import Flask
from flask import render_template

from nice_project.utils.memory import Memory

flask_app = Flask(__name__)

memory = Memory(4)

@flask_app.route("/")
def index():
    global memory
    now = datetime.datetime.now()
    memory = memory.add(now)
    iterable = iter(memory)
    return render_template("index.html", iterable=iterable)
