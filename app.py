import os
from http.server import BaseHTTPRequestHandler, HTTPServer

import mysql.connector

VERSION = "0.4.0"


def check_mysql():
    host = os.getenv("MYSQL_HOST")
    port = int(os.getenv("MYSQL_PORT", "3306"))
    database = os.getenv("MYSQL_DATABASE")
    username = os.getenv("MYSQL_USERNAME")
    password = os.getenv("MYSQL_PASSWORD")
    missing = [name for name, value in {
        "MYSQL_HOST": host,
        "MYSQL_DATABASE": database,
        "MYSQL_USERNAME": username,
        "MYSQL_PASSWORD": password,
    }.items() if not value]
    if missing:
        return False, "missing " + ",".join(missing)

    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password,
            connection_timeout=3,
        )
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
        finally:
            conn.close()
        return True, f"connected to {host}:{port}/{database}"
    except Exception as exc:
        return False, str(exc)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"ok\n")
            return

        ok, detail = check_mysql()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        status = "ok" if ok else "failed"
        body = (
            f"California Beans Docker test container V{VERSION}\n"
            f"mysql: {status}\n"
            f"mysql_detail: {detail}\n"
        )
        self.wfile.write(body.encode("utf-8"))

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    server = HTTPServer((host, port), Handler)
    print(f"Starting California Beans on http://{host}:{port}")
    server.serve_forever()
