# flask-tornado
An implementation of a Tornado server for your Flask application

This module allows the use of Tornado as the Flask server

The flask project is here:

https://github.com/pallets/flask

The tornado project is here:

https://github.com/tornadoweb/tornado

## explanation:

As you will discover during experimenting with flask, the app.run()
in flask development server is a "blocking" server -- this was an
intentional choice to allow better debugging.  And was never, ever, intended
to be used in production.  It was included as a "convenience" to
get users developing quickly without lots of extra resources.

If you need evidence, you can test this behavior by running an app on your development
environment, and then trying to access it on several different browsers
simultaneously.  One browser "wins" and grabs the connection while the
other is forced to wait... and wait... and wait.

Tornado can be used as a very fast alternate server that will function well in
as a stand-alone server or, better yet, as a proxy worker behind Apache or Nginx.

If you are looking for alternatives, you could also employ Gunicorn.
This works very well for production environments too.  But Tornado can
be "baked-in" to your app from the beginning to bring simple apps up quickly
without much mucking around with your deployment

*Disclaimer - this is not necessarily the most secure or thread-safe
way to do things but Tornado can scale, so you could theoretically use the app in a
small to medium scale production envornment as a stand-alone app.*

However, to really do things correctly, you would want to use Apache or
Nginx front end and set this up as a worker.  So test, test, test before you go
in to production!!

## usage

### used as a Class
```
from flask import Flask
from flask_tornado import TornadoServer

import datetime

app = Flask(__name__)
server = TornadoServer(app) # instantiate a server object

@app.route('/')
def index():
    return "Hello World the local server time is {}".format(datetime.datetime.now())

if __name__ == '__main__':
    server.run(port=12345)
```

### used as a function
```
from flask import Flask
import flask_tornado

import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World the local server time is {}".format(datetime.datetime.now())

if __name__ == '__main__':
    # it is required to reference the app (default port is 5000)
    flask_tornado.run(app)
```

### used with an SSL context
```
from flask import Flask
from flask_tornado import TornadoServer

import datetime

app = Flask(__name__)
server = TornadoServer(app)

@app.route('/')
def index():
    return "Hello World the local server time is {}".format(datetime.datetime.now())

if __name__ == '__main__':
    server.run(port=8443, ssl_cert='path_to_your_ssl_cert_file', ssl_key='path_to_your_ssl_key')
```

## API DOCUMENTATION

todo

## SSL context which has a port 80 redirect to 443

todo
