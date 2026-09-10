from flask import Blueprint, jsonify, current_app

from core.history_manager import HistoryManager
from core.file_io import read_dataset
from core.analysis_engine import analyze_dataframe


undo_bp = Blueprint(
    "undo",
    __name__,
    url_prefix="/api"
)


@undo_bp.post("/undo/<session_id>")
def undo_operation(session_id):

    manager = current_app.session_manager

    session_dir = manager.get_session_path(session_id)

    if session_dir is None:
        return jsonify({
            "success": False,
            "error": "Invalid or expired session."
        }), 404

    meta = manager.get_meta(session_id) or {}

    extension = (
        meta.get("working_extension")
        or meta.get("extension")
    )

    if not extension:
        return jsonify({
            "success": False,
            "error": "Session file format is unavailable."
        }), 400

    current_file = session_dir / f"current.{extension}"

    if not current_file.is_file():
        return jsonify({
            "success": False,
            "error": "Current dataset not found."
        }), 404

    history = HistoryManager(session_dir)

    try:
        restored = history.restore_latest(current_file)

        if not restored:
            return jsonify({
                "success": False,
                "error": "Nothing to undo."
            }), 400

        df = read_dataset(current_file)
        stats = analyze_dataframe(df)

        manager.update_meta(
            session_id,
            last_before_stats=stats,
            last_after_stats=stats,
            last_operations=[],
            last_undo=True
        )

        manager.touch(session_id)

        return jsonify({
            "success": True,
            "session_id": session_id,
            "stats": stats,
            "message": "Last cleaning round was undone."
        })

    except Exception:
        current_app.logger.exception(
            "Dataset undo failed"
        )

        return jsonify({
            "success": False,
            "error": "Unable to undo the last cleaning operation."
        }), 500