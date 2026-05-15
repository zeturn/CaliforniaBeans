from http.server import BaseHTTPRequestHandler, HTTPServer

VERSION = "0.1.0"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"California Beans Docker test container V{VERSION}\n".encode("utf-8"))

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    server = HTTPServer((host, port), Handler)
    print(f"Starting California Beans on http://{host}:{port}")
    server.serve_forever()
