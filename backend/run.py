"""
Predly Backend 启动入口
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.config import Config

def validate():
    errors = Config.validate()
    if errors:
        print("配置错误:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    print("Config validated OK", flush=True)

validate()

# Gunicorn entry point
application = create_app()