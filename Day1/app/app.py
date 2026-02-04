from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import os

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        hostname = socket.gethostname()
        message = f"""
        Hello from container!
        
        Hostname: {hostname}
        Environment: {os.getenv("ENV", "not-set")}
        """

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(message.encode())

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), SimpleHandler)
    print("Starting server on port 8080")
    server.serve_forever()