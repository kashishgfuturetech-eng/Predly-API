"""
Predly Backend 启动入口
"""

import os
import sys
import socket

# Bind port immediately so Render's scanner sees it
# before heavy imports (camel-ai, oasis etc.) finish loading
port = int(os.environ.get('PORT', os.environ.get('FLASK_PORT', 10000)))
_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
_sock.bind(('0.0.0.0', port))
_sock.listen(5)

# Now do the slow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.config import Config


def main():
    errors = Config.validate()
    if errors:
        print("配置错误:")
        for err in errors:
            print(f"  - {err}")
        print("\n请检查 .env 文件中的配置")
        sys.exit(1)

    app = create_app()

    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    debug = Config.DEBUG

    # Pass the already-bound socket to Flask
    app.run(host=host, port=port, debug=False, threaded=True, fd=_sock.fileno())


if __name__ == '__main__':
    main()