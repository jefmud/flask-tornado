import os.path
import mimetypes
import sys

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

class FileHandler(tornado.web.RequestHandler):
    def get(self, path):
        if not path:
            path = 'index.html'

        if not os.path.exists(path):
            raise tornado.web.HTTPError(404)

        mime_type = mimetypes.guess_type(path)
        self.set_header("Content-Type", mime_type[0] or 'text/plain')

        outfile = open(path)
        for line in outfile:
            self.write(line)
        self.finish()

def simple_http_server(port=8080):
    tornado.options.enable_pretty_logging()
    application = tornado.web.Application([
        (r"/(.*)", FileHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

def usage():
    print("python simpleHTTPserver --port <int:port>")
    print("note: server does not check if existing server is running on that port")
    sys.exit(0)
    
if __name__ == "__main__":
    if '--port' in sys.argv:
        try:
            port = int(sys.argv[sys.argv.index('--port')+1])
            simple_http_server(port)
        except:
            print("port must be an integer value")
            usage()
            
    simple_http_server()
