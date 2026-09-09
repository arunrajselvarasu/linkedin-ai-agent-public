from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


class CallbackHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urlparse(self.path)
        query = parse_qs(parsed_url.query)

        code = query.get("code", [None])[0]
        error = query.get("error", [None])[0]

        if code:
            print("\n✅ LinkedIn authorization successful!")
            print("\nAuthorization Code:")
            print(code)

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            self.wfile.write(
                b"""
                <html>
                    <body>
                        <h1>LinkedIn Authorization Successful!</h1>
                        <p>You can close this browser window.</p>
                    </body>
                </html>
                """
            )

        elif error:
            print("\n❌ LinkedIn authorization failed:")
            print(error)

            self.send_response(400)
            self.end_headers()

        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        return


server = HTTPServer(("localhost", 8000), CallbackHandler)

print("🚀 LinkedIn OAuth callback server running...")
print("Waiting for LinkedIn authorization...")
print("Callback URL: http://localhost:8000/callback")

server.serve_forever()