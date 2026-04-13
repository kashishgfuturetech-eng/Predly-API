"""
Predly Backend - Flask Application Factory
"""
"""
Predly Backend - Flask Application Factory
"""

import os
import warnings
warnings.filterwarnings("ignore", message=".*resource_tracker.*")

from flask import Flask, request, make_response
from .config import Config
from .utils.logger import setup_logger, get_logger


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ── CORS ──────────────────────────────────────────────
    @app.after_request
    def apply_cors(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        return response

    @app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
    @app.route('/<path:path>', methods=['OPTIONS'])
    def options_handler(path):
        response = make_response('')
        response.status_code = 204
        return response
    # ──────────────────────────────────────────────────────

    if hasattr(app, 'json') and hasattr(app.json, 'ensure_ascii'):
        app.json.ensure_ascii = False

    logger = setup_logger('predly')

    is_reloader_process = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    debug_mode = app.config.get('DEBUG', False)
    should_log_startup = not debug_mode or is_reloader_process

    if should_log_startup:
        logger.info("=" * 50)
        logger.info("Predly Backend starting...")
        logger.info("=" * 50)

    from .services.simulation_runner import SimulationRunner
    SimulationRunner.register_cleanup()

    @app.before_request
    def log_request():
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

    from .api import graph_bp, simulation_bp, report_bp
    app.register_blueprint(graph_bp, url_prefix='/api/graph')
    app.register_blueprint(simulation_bp, url_prefix='/api/simulation')
    app.register_blueprint(report_bp, url_prefix='/api/report')

    @app.route('/')
    def health():
        return {'status': 'ok', 'service': 'Predly Backend'}

    if should_log_startup:
        logger.info("Predly Backend started successfully")

    return app