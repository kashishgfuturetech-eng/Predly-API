import os
port = os.environ.get("PORT", os.environ.get("FLASK_PORT", "10000"))
bind = f"0.0.0.0:{port}"
workers = 1
threads = 2  # reduce from 4 to 2 to save RAM
timeout = 300
worker_class = "sync"