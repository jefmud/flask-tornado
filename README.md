# flask-tornado
An implementation of a Tornado server for your Flask application

*dependencies: Flask, Tornado*

This module allows the use of Tornado as the Flask server

The flask project is here:

https://github.com/pallets/flask

The tornado project is here:

https://github.com/tornadoweb/tornado

http://www.tornadoweb.org/en/stable/

## explanation:

As you will discover experimenting with flask, the app.run()
flask development server is a single-threaded "blocking server" -- this was an
intentional choice to allow better debugging.  Hence, it was never, ever, intended
to be used in production.  It was included as a convenience to
get users developing/testing quickly without lots of extra resources.

If you need evidence, you can test this behavior by running an app on your development
environment, and then trying to access it on several different browsers
simultaneously.  One browser "wins" and grabs the connection while the
other is forced to wait... and wait... and wait.

**Important Note: as of Flask release of 1.x version, the development server is multi-threaded so the previous discussion is no longer valid.  Tornado still is a better choice because it is fast, fast, fast!**

Enter Tornado.

Tornado is another web framework, worthy of study.  We're not going to ditch Flask, we
are interested in using Tornado's server with a Flask app. Tornado's included WSGI server
can be used quite well with Flask.  Tornado's server as a very fast and can function well
as a stand-alone server or, better yet, as a proxy worker behind Apache or Nginx.

If you are looking for alternatives, you could also employ Gunicorn.
This works very well for production environments too.  But Tornado can
be "baked-in" to your app from the beginning to bring simple apps up quickly
without much mucking around with your deployment

*Disclaimer - this is not necessarily the most secure or thread-safe
way to do things but Tornado can scale, so you could theoretically use the app in a
small to medium scale production environment as a stand-alone app.*

However, to really do things correctly, you would want to use Apache or
Nginx front end and set this up as a worker.  So test, test, test before you go
in to production!!

## usage and installation

*keep it simple*

The reason why we love Flask and Tornado is their surface API is simple and approachable.

For now... it is easy to just copy the file "flask_tornado.py" into the same directory
as your app! Thus adhering to the KISS principle-- or "Keep it Simple Stupid" paradigm.

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

At some point Armin Ronacher (creator of Flask) or Ben Darnell (creator of Tornado) will write a simple way to redirect HTTP to HTTPS equivalents.  Sure, you can do this with Apache or NGINX servers too, but since this article is about simple deployment, I offer several simple strategies that can be employed to accomplish this scenario:

1) create a no_redirect_app, that presents a message, in my example, "These are not the droids you are looking for", and gives a link to the root URL on the 443 app.

reference Flask docs http://flask.pocoo.org/docs/1.0/patterns/errorpages/

```python
from flask import Flask
from flask_tornado import TornadoServer
app = Flask(__name__)
server = TornadoServer(app)

@app.errorhandler(404)
def page_not_found(e):
"""returns a explicit redirect to your site"""
    return 'These are not the droids you are looking for... <a href="https://yoursite.com">try checking here</a>'

if __name__ == '__main__':
    server.run(port=80)
```

2) A slightly fancier approach, create a redirect_app that listens to requests on port 80 and then 301 redirects to the actual app listening on port 443.  If you've read this far in the docs, I assume you know what you are doing here.

http://flask.pocoo.org/docs/1.0/api/?highlight=redirect#flask.redirect

3) run a second instance of the app on port 80... but rewrite the LOGIN method to drive them to the 443 url.  This way users can consume unencrypted (public) data as they require but when they login or use a form that requires encryption, we redirect.  This unfortunately adds complexity to your project, but achieves the desired effect of SSL.

reference Flask documentation: http://flask.pocoo.org/docs/1.0/reqcontext/?highlight=before_request
