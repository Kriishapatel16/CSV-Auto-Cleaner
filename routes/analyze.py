from flask import (
    Blueprint,
    jsonify,
    current_app
)

from core.file_io import (
    read_dataset
)

from core.analysis_engine import (
    analyze_dataframe
)


analyze_bp = Blueprint(
    "analyze",
    __name__,
    url_prefix="/api"
)


@analyze_bp.get(
    "/analyze/<session_id>"
)
def analyze_dataset(
    session_id
):

    manager = (
        current_app.session_manager
    )

    session_dir = (
        manager.get_session_path(
            session_id
        )
    )

    if session_dir is None:

        return jsonify({
            "success": False,
            "error":
                "Invalid or expired session."
        }), 404

    meta = (
        manager.get_meta(
            session_id
        ) or {}
    )

    extension = (
        meta.get(
            "working_extension"
        )
        or
        meta.get(
            "extension"
        )
    )

    if not extension:

        return jsonify({
            "success": False,
            "error":
                "Session metadata is invalid."
        }), 400

    current_file = (
        session_dir /
        f"current.{extension}"
    )

    if not current_file.exists():

        return jsonify({
            "success": False,
            "error":
                "Dataset not found."
        }), 404

    try:

        df = read_dataset(
            current_file
        )

        stats = analyze_dataframe(
            df
        )

        stats["file_size"] = (
            current_file.stat()
            .st_size
        )

        stats["file_type"] = (
            extension.upper()
        )

        manager.touch(
            session_id
        )

        return jsonify({

            "success":
                True,

            "session_id":
                session_id,

            "stats":
                stats
        })

    except Exception:

        current_app.logger.exception(
            "Analysis failed"
        )

        return jsonify({
            "success": False,
            "error":
                "Unable to analyze the dataset."
        }), 400