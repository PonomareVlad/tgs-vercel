from http.server import BaseHTTPRequestHandler
from lottie.exporters.core import export_tgs
from lottie.importers.svg import import_svg
import cgi

svg_path = '/tmp/sticker.svg'
tgs_path = '/tmp/sticker.svg'


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        return self.send_error(405)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD": "POST",
                     "CONTENT_TYPE": self.headers['Content-Type']})

        uploaded_file = form.getvalue("file")
        if uploaded_file:
            self.send_response(200)
            self.send_header('Content-type', 'application/gzip')
            self.send_header('Content-Disposition', 'attachment; filename="sticker.tgs"')
            self.end_headers()
            open(svg_path, "wb").write(uploaded_file)
            animation = import_svg(svg_path)
            export_tgs(animation, tgs_path, True, True)
            self.wfile.write(open(tgs_path, 'rb').read())
        else:
            self.send_error(415)
        return
