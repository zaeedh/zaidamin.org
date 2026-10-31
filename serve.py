"""
Academic Development Server for zaidamin.org
Dual-Stack IPv4 & IPv6 with CORS for Antigravity IDE (Jetski Preview) & Browsers.
"""

import http.server
import socket
import socketserver
import os
from pathlib import Path

PORT = 8000
DIRECTORY = Path(__file__).resolve().parent / "dist"

class AcademicPreviewHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def end_headers(self):
        # Enable CORS and iframe embedding for Antigravity IDE webviews (Jetski / Simple Browser)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

class DualStackServer(http.server.ThreadingHTTPServer):
    address_family = socket.AF_INET6

    def server_bind(self):
        # Allow IPv4 and IPv6 on same socket
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()

def run():
    with DualStackServer(("::", PORT), AcademicPreviewHandler) as httpd:
        print("=" * 60)
        print(f" Academic Server Active (Dual-Stack IPv4 + IPv6):")
        print(f" - http://127.0.0.1:{PORT}")
        print(f" - http://localhost:{PORT}")
        print(f" Serving Root: {DIRECTORY}")
        print("=" * 60)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    run()
