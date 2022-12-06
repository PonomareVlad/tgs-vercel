from http.server import BaseHTTPRequestHandler
from lottie.exporters.core import export_lottie
from lottie.importers.svg import import_svg

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Hello, world!'.encode('utf-8'))

        animation = import_svg()

        export_lottie(animation, "open_save.json")

        return
