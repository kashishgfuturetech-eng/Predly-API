import os
port = os.environ.get("PORT", os.environ.get("FLASK_PORT", "10000"))
bind = f"0.0.0.0:{port}"
workers = 1
threads = 4
timeout = 120
worker_class = "sync"