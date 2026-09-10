from flask import Blueprint, jsonify, current_app

from core.file_io import read_dataset, save_dataset
from core.analysis_engine import analyze_dataframe
from core.history_manager import HistoryManager
from core.output_sanitizer import sanitize_dataframe


reset_bp = Blueprint(
    "reset",
    __name__,
    url_prefix="/api"
)


@reset_bp.post("/reset/<session_id>")
def reset_dataset(session_id):

    manager = current_app.session_manager

    session_dir = manager.get_session_path(session_id)

    if session_dir is None:
        return jsonify({
            "success": False,
            "error": "Invalid or expired session."
        }), 404

    meta = manager.get_meta(session_id) or {}

    original_extension = meta.get("extension")

    if not original_extension:
        return jsonify({
            "success": False,
            "error": "Original file format is unavailable."
        }), 400

    working_extension = (
        meta.get("working_extension")
        or original_extension
    )

    original_file = (
        session_dir /
        f"original.{original_extension}"
    )

    current_file = (
        session_dir /
        f"current.{working_extension}"
    )

    if not original_file.is_file():
        return jsonify({
            "success": False,
            "error": "Original dataset not found."
        }), 404

    try:

        original_df = read_dataset(
            original_file
        )

        safe_df = sanitize_dataframe(
            original_df
        )

        save_dataset(
            safe_df,
            current_file
        )

        HistoryManager(session_dir).clear()

        report_file = session_dir / "report.pdf"
        report_file.unlink(missing_ok=True)

        df = read_dataset(
            current_file
        )

        stats = analyze_dataframe(
            df
        )

        manager.update_meta(
            session_id,
            last_before_stats=stats,
            last_after_stats=stats,
            last_operations=[],
            last_undo=False
        )

        manager.touch(session_id)

        return jsonify({
            "success": True,
            "session_id": session_id,
            "stats": stats,
            "message": "Dataset reset to the original upload."
        })

    except Exception:

        current_app.logger.exception(
            "Failed to reset dataset"
        )

        return jsonify({
            "success": False,
            "error": "Unable to reset the dataset."
        }), 500