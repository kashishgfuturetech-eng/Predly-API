"""
Predly Backend - Flask Application Factory
"""

import os
import warnings

# Suppress multiprocessing resource_tracker warnings (from third-party libs like transformers)
# Must be set before all other imports
warnings.filterwarnings("ignore", message=".*resource_tracker.*")

from flask import Flask, request
from flask_cors import CORS

from .config import Config
from .utils.logger import setup_logger, get_logger


def create_app(config_class=Config):
    """Flask application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Single CORS initialization — covers all routes including error responses
    CORS(app, resources={r"/*": {"origins": "*"}})

    # JSON encoding: ensure Chinese characters are rendered directly (not as \uXXXX)
    # Flask >= 2.3 uses app.json.ensure_ascii; older versions use JSON_AS_ASCII config
    if hasattr(app, 'json') and hasattr(app.json, 'ensure_ascii'):
        app.json.ensure_ascii = False
    
    # Set up logging
    logger = setup_logger('predly')
    
    # Only log startup info in the reloader child process (avoids double-printing in debug mode)
    is_reloader_process = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    debug_mode = app.config.get('DEBUG', False)
    should_log_startup = not debug_mode or is_reloader_process
    
    if should_log_startup:
        logger.info("=" * 50)
        logger.info("Predly Backend starting...")
        logger.info("=" * 50)
    
    # Register simulation process cleanup (ensures all simulation processes are terminated on server shutdown)
    from .services.simulation_runner import SimulationRunner
    SimulationRunner.register_cleanup()
    if should_log_startup:
        logger.info("Simulation process cleanup handler registered")
    
    # Update last_session for any authenticated request (throttled: once per 5 min per user)
    @app.before_request
    def track_session_activity():
        if request.method == 'OPTIONS':
            return
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return
        from .api.auth import verify_token
        from .services.user_store import _connect
        payload = verify_token(auth_header[7:])
        if not payload or not payload.get('email'):
            return
        email = payload['email'].strip().lower()
        import datetime
        now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        conn = _connect()
        try:
            conn.execute(
                """UPDATE users SET last_session = ?
                   WHERE email = ?
                   AND (last_session IS NULL OR last_session < datetime('now', '-5 minutes'))""",
                (now, email),
            )
            conn.commit()
        finally:
            conn.close()

    # Request logging middleware
    @app.before_request
    def log_request():
        # Skip OPTIONS preflight requests — let Flask-CORS handle them unimpeded
        if request.method == 'OPTIONS':
            return
        logger = get_logger('predly.request')
        logger.debug(f"Request: {request.method} {request.path}")
        if request.content_type and 'json' in request.content_type:
            logger.debug(f"Request body: {request.get_json(silent=True)}")
    
    @app.after_request
    def log_response(response):
        logger = get_logger('predly.request')
        logger.debug(f"Response: {response.status_code}")
        return response
    
    # Register blueprints
    from .api import graph_bp, simulation_bp, report_bp, auth_bp
    from .api.admin import admin_bp
    app.register_blueprint(graph_bp, url_prefix='/api/graph')
    app.register_blueprint(simulation_bp, url_prefix='/api/simulation')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # Health check
    @app.route('/')
    def health():
        return {'status': 'ok', 'service': 'Predly Backend'}
    
    if should_log_startup:
        logger.info("Predly Backend started successfully")
    
    return app