import logging
import os

from flask import Flask, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import Config
from core.session_manager import SessionManager

from routes.upload import upload_bp
from routes.analyze import analyze_bp
from routes.operations import operations_bp
from routes.undo import undo_bp
from routes.download import download_bp
from routes.reset import reset_bp
from routes.report import report_bp

from workers.cleanup_scheduler import start_cleanup_scheduler


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.getenv("COOKIE_SECURE", "0") == "1",
        MAX_CONTENT_LENGTH=Config.MAX_CONTENT_LENGTH
    )

    logging.basicConfig(level=logging.INFO)

    Config.SESSION_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    app.session_manager = SessionManager(
        Config.SESSION_DIR,
        Config.SESSION_TTL_SECONDS
    )

    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=[
            "200 per day",
            "50 per hour"
        ],
        storage_uri=os.getenv(
            "RATELIMIT_STORAGE_URI",
            "memory://"
        ),
        headers_enabled=True
    )

    app.limiter = limiter

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = (
            "strict-origin-when-cross-origin"
        )
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: blob:; "
            "connect-src 'self'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "frame-ancestors 'none'; "
            "form-action 'self'"
        )

        if request_path_is_api(response):
            response.headers["Cache-Control"] = "no-store"

        return response

    @app.get("/")
    def index():
        return render_template("index.html")

    app.register_blueprint(upload_bp)
    app.register_blueprint(analyze_bp)
    app.register_blueprint(operations_bp)
    app.register_blueprint(undo_bp)
    app.register_blueprint(download_bp)
    app.register_blueprint(reset_bp)
    app.register_blueprint(report_bp)

    @app.errorhandler(413)
    def request_entity_too_large(_error):
        return jsonify({
            "success": False,
            "error": "File exceeds the maximum size of 100 MB."
        }), 413

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({
            "success": False,
            "error": "Resource not found."
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return jsonify({
            "success": False,
            "error": "HTTP method not allowed."
        }), 405

    @app.errorhandler(429)
    def rate_limit_exceeded(_error):
        return jsonify({
            "success": False,
            "error": "Too many requests. Please try again later."
        }), 429

    @app.errorhandler(500)
    def internal_error(_error):
        app.logger.exception("Internal server error")
        return jsonify({
            "success": False,
            "error": "An unexpected server error occurred."
        }), 500

    try:
        app.session_manager.cleanup_expired()
    except Exception as e:
        app.logger.warning(f"Initial cleanup check skipped: {e}")

    debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
    reloader_process = os.getenv("WERKZEUG_RUN_MAIN") == "true"

    if (
        os.getenv("DISABLE_CLEANUP_SCHEDULER", "0") != "1"
        and (not debug_mode or reloader_process)
    ):
        try:
            app.cleanup_scheduler = start_cleanup_scheduler(app)
        except Exception as e:
            app.logger.warning(f"Could not start background cleanup scheduler: {e}")

    return app


def request_path_is_api(response):
    content_type = response.headers.get("Content-Type", "")
    return "application/json" in content_type


app = create_app()


if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG", "0") == "1"
    )