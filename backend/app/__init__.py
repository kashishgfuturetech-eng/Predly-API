"""
Predly Backend - Flask Application Factory
"""

import os
import warnings
from flask import send_from_directory

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
    from .api import graph_bp, simulation_bp, report_bp
    app.register_blueprint(graph_bp, url_prefix='/api/graph')
    app.register_blueprint(simulation_bp, url_prefix='/api/simulation')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    
    # Health check endpoint
    @app.route('/')
    def health():
        return {'status': 'ok', 'service': 'Predly Backend'}

    # Serve Vue frontend static build (production)
    import os as _os
    from flask import send_from_directory as _sfd
    _dist = _os.path.join(_os.path.dirname(__file__), '../../frontend/dist')

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        full = _os.path.join(_dist, path)
        if path and _os.path.exists(full) and not _os.path.isdir(full):
            return _sfd(_dist, path)
        return _sfd(_dist, 'index.html')
    
    return app