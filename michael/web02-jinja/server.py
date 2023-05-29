from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Configure Jinja environment
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(['html', 'xml'])
)

# HTTPRequestHandler class
class MyServerHandler(BaseHTTPRequestHandler):
    # Handle GET requests
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            template = env.get_template('index.html')
            self.wfile.write(template.render().encode())
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
            template = env.get_template('greeting.html')
            greeting = template.render(name=name)
            self.wfile.write(greeting.encode())
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
