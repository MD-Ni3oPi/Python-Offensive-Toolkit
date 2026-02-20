#Step 1: Install the Web Library
#pip install requests --break-system-packages

from http.server import BaseHTTPRequestHandler, HTTPServer


class ExfilHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        print("\n[*] --- INCOMING HTTP EXFILTRATION ---")
        print(f"[*] Path: {self.path}")
        print(f"[*] Client: {self.client_address}")
        print("[-] Encrypted Data Received:")
        print(post_data.decode('utf-8', errors='replace'))
        print("[*] ----------------------------------")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Success")


if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8080), ExfilHandler)
    print("[*] HTTP Listener running on 127.0.0.1:8080...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
