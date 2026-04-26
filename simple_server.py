#!/usr/bin/env python3
"""Simple HTTP server that serves the static files"""

import http.server
import socketserver
import os

PORT = 8000

# Change to the directory containing index.html
os.chdir(os.path.dirname(os.path.abspath(__file__)))

Handler = http.server.SimpleHTTPRequestHandler

print(f"Starting server on port {PORT}...")
print(f"Serving from: {os.getcwd()}")
print(f"Open http://localhost:{PORT} in your browser")

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped")
