import sys
import cgi
import json
import gzip
import logging
import tempfile
from lottie.importers.svg import import_svg
from http.server import BaseHTTPRequestHandler
from lottie.exporters.tgs_validator import TgsValidator

class handler(BaseHTTPRequestHandler):

    def send_json_error(self, code=500, error=None, message=None):
        if error is None:
            exception = sys.exc_info()
            error = {"type": exception[0].__name__, "message": str(exception[1])}
        self.send_response(code, message)
        self.send_header('Content-type', 'text/json; charset=utf-8')
        self.end_headers()
        json_obj = json.dumps({"error": error}, indent=4)
        self.wfile.write(json_obj.encode())

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
            with tempfile.TemporaryFile("wb+") as svg:
                try:
                    svg.write(uploaded_file)
                    animation = import_svg(svg)
                    animation.tgs_sanitize()
                    validator = TgsValidator()
                    validator(animation)
                    if validator.errors:
                        details = map(str, validator.errors)
                        error = {"type": "ValidationError", "message": "Unsupported SVG content", "details": details}
                        logging.critical(error["message"])
                        return self.send_json_error(422, error)
                    lottie_dict = animation.to_dict()
                    lottie_dict["tgs"] = 1
                    tgs = gzip.compress(json.dumps(lottie_dict).encode())
                except Exception as e:
                    logging.critical(e, exc_info=True)
                    self.send_json_error(422)
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/gzip')
                    self.send_header('Content-Disposition', 'attachment; filename="sticker.tgs"')
                    self.end_headers()
                    self.wfile.write(tgs)

        else:
            logging.critical("Unsupported file")
            self.send_json_error(415, {"type": "FileError", "message": "Unsupported file"})
