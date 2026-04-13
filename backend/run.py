"""
Predly Backend 启动入口
"""

import os
import sys

# Bind port IMMEDIATELY before any other imports
# This is critical for Render's port scan
import socket
port = int(os.environ.get('PORT', 10000))
_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
_sock.bind(('0.0.0.0', port))
_sock.listen(5)
print(f"Port {port} bound successfully", flush=True)

# Now do slow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.config import Config


class CORSMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def cors_start_response(status, headers, exc_info=None):
            headers = list(headers)
            header_keys = [h[0].lower() for h in headers]
            if 'access-control-allow-origin' not in header_keys:
                headers.append(('Access-Control-Allow-Origin', '*'))
                headers.append(('Access-Control-Allow-Headers', 'Content-Type, Authorization'))
                headers.append(('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'))
            return start_response(status, headers, exc_info)

        if environ.get('REQUEST_METHOD') == 'OPTIONS':
            cors_start_response('204 No Content', [
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Headers', 'Content-Type, Authorization'),
                ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'),
                ('Content-Length', '0'),
            ])
            return [b'']

        return self.app(environ, cors_start_response)


def main():
    errors = Config.validate()
    if errors:
        print("配置错误:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    app = create_app()
    app.wsgi_app = CORSMiddleware(app.wsgi_app)

    host = os.environ.get('FLASK_HOST', '0.0.0.0')

    from werkzeug.serving import make_server
    server = make_server(host, port, app, threaded=True, fd=_sock.fileno())
    print(f"Predly Backend running on {host}:{port}", flush=True)
    server.serve_forever()


if __name__ == '__main__':
    main()