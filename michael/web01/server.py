from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

# HTTPRequestHandler class
class MyServerHandler(BaseHTTPRequestHandler):
    # Handle GET requests
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # HTML form
            form = '''
                <html>
                <body>
                <h1>Welcome!</h1>
                <form method="post">
                    <label for="name">Enter your name:</label><br>
                    <input type="text" id="name" name="name"><br><br>
                    <input type="submit" value="Submit">
                </form>
                </body>
                </html>
            '''
            self.wfile.write(form.encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    # Handle POST requests
    def do_POST(self):
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()
            params = parse_qs(post_data)
            name = params['name'][0] if 'name' in params else 'Unknown'
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = f'<html><body><h1>Hello {name}!</h1></body></html>'
            self.wfile.write(message.encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

# Main method to start the server
def run():
    host = 'localhost'
    port = 8000
    server_address = (host, port)
    httpd = HTTPServer(server_address, MyServerHandler)
    print(f'Starting server on {host}:{port}...')
    httpd.serve_forever()

# Run the server
run()