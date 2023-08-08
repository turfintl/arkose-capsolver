from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
import capsolver

# 填入CapSolver API key // Enter your CapSolver API key here
API_KEY = ''

def get_token():
    capsolver.api_key = API_KEY
    solution = capsolver.solve({
        'type': 'FunCaptchaTaskProxyLess',
        'websitePublicKey': '35536E1E-65B4-4D96-9D97-6ADB7EFF8147',
        'websiteURL': 'https://chat.openai.com',
    })
    return solution


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if self.path != '/token':
            self.send_response(502)
            self.end_headers()
            return

        token = get_token()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(token).encode())
        return


if __name__ == '__main__':
    # 避免服务器暴露于公网 // Avoid binding to public ip address
    server = HTTPServer(('127.0.0.1', 8999), RequestHandler)
    print('Server started.\nGet your arkose token via http://127.0.0.1:8999/token')
    server.serve_forever()
