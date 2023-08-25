import random

from flask import Flask

app=Flask(__name__)


@app.route('/')
def index():
    return 'random: <strong>' +str(random.random())+'</strong>'

app.run()