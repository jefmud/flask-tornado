"""
This module allows the use of tornado as the Flask server

explanation:

As you will discover during experimenting with flask, the app.run()
in flask development server is a "blocking" server -- this was an
intentional choice to allow better debugging.  And was never, ever, intended
to be used in production.  It was included as a "convenience" to
get users developing quickly without lots of extra resources.

If you need evidence, you can test this behavior by running an app on your development
environment, and then trying to access it on several different browsers
simultaneously.  One browser "wins" abd grabs the connection while the
other is forced to wait... and wait... and wait.

Tornado can be used as an alternate server that will function well in
as a stand-alone server or, better yet, as a proxy worker behind Apache or Nginx.

If you are looking for alternatives, you could also employ Gunicorn.
This works very well for production environments too.  But Tornado can
be "baked-in" to your app from the beginning to bring simple apps up quickly
without much mucking around with your deployment

Disclaimer - this is not necessarily a secure or thread-safe way to do things
but Tornado can scale, so you could theoretically use the app in a
small to medium scale production envornment as a stand-alone app.

However, to really do things correctly, you would want to use Apache or
Nginx front end and set this up as a worker.  So test, test, test before you go
in to production!!
"""
from __future__ import print_function
import errno, os
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

class TornadoServer():
    def __init__(self, app, port=5000, certfile=None, keyfile=None):
        #self.http_server = HTTPServer(WSGIContainer(app))
        self.app = app
        self.port = port
        self.set_certificate(certfile, keyfile)

    def set_certificate(self, certfile=None, keyfile=None):
        """set the certificate, die if specified file doesn't exist"""
        
        self.certfile = certfile
        self.keyfile = keyfile

        if certfile:
            if not os.path.isfile(certfile):
                print("ERROR: Certificate NOT FOUND!")
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), certfile)

        if keyfile:
            if not os.path.isfile(keyfile):
                print("ERROR: Keyfile NOT FOUND!")
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), keyfile)

    
    def run(self, port=None, host=None, certfile=None, keyfile=None):
        """run the server as class method, can override the port and host"""
        server_port = self.port
        # user override of the port
        if isinstance(port, int):
            server_port = port

        self.set_certificate(certfile, keyfile)

        if self.certfile and self.keyfile:
            # add an SSL certificate if you want to use HTTPS
            ssl_options = {"certfile": self.certfile, "keyfile": self.keyfile}
            http_server = HTTPServer(WSGIContainer(self.app, ssl_options=ssl_options))
        else:
            http_server = HTTPServer(WSGIContainer(self.app))
        
        http_server.listen(server_port)
        print("Tornado server started on port %s" % server_port)
        IOLoop.instance().start()

def run(app, port=5000, certfile=None, keyfile=None):
    """run the server, functional calling style
    app - the WSGI app, required
    port - the server port
    certfile - an SSL certificate file
    keyfile - an SSL keyfile
    """
    server = TornadoServer(app, port=port, certfile=certfile, keyfile=keyfile)
    server.run()
