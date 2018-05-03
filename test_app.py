from flask import Flask
import flask_tornado

import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World the local server time is {}".format(datetime.datetime.now())

if __name__ == '__main__':
    flask_tornado.run(app, port=12345)
