from pathlib import Path

from flask import (
    Blueprint,
    send_file,
    jsonify,
    current_app
)


download_bp = Blueprint(
    "download",
    __name__,
    url_prefix="/api"
)


MIMETYPES = {

    "csv":
        "text/csv",

    "tsv":
        "text/tab-separated-values",

    "xlsx":
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

    "json":
        "application/json",
}


@download_bp.get(
    "/download/<session_id>"
)
def download(
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

    current_file = (
        session_dir /
        f"current.{extension}"
    )

    if not current_file.exists():

        return jsonify({
            "success": False,
            "error":
                "Processed dataset not found."
        }), 404

    original = Path(
        meta.get(
            "original_filename",
            "dataset"
        )
    )

    filename = (
        f"{original.stem}"
        f"_cleaned."
        f"{extension}"
    )

    manager.touch(
        session_id
    )

    return send_file(
        current_file,
        as_attachment=True,
        download_name=filename,
        mimetype=MIMETYPES.get(
            extension
        )
    )