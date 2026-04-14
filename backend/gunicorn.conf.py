import os
port = os.environ.get("PORT", os.environ.get("FLASK_PORT", "10000"))
bind = f"0.0.0.0:{port}"
workers = 1
threads = 2
timeout = 600        # increase from 120 to 600 seconds
graceful_timeout = 300
worker_class = "sync"
keepalive = 5