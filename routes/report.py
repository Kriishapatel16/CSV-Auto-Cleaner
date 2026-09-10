from flask import (
    Blueprint,
    jsonify,
    current_app,
    send_file
)

from core.file_io import read_dataset
from core.analysis_engine import analyze_dataframe
from reporting.pdf_generator import generate_pdf


report_bp = Blueprint(
    "report",
    __name__,
    url_prefix="/api"
)


@report_bp.get("/report/<session_id>")
def generate_report(session_id):

    manager = current_app.session_manager

    session_dir = manager.get_session_path(
        session_id
    )

    if session_dir is None:

        return jsonify({
            "success": False,
            "error": "Invalid or expired session."
        }), 404

    meta = manager.get_meta(
        session_id
    ) or {}

    extension = (
        meta.get("working_extension")
        or meta.get("extension")
    )

    if not extension:

        return jsonify({
            "success": False,
            "error": "Session file format is unavailable."
        }), 400

    current_file = (
        session_dir /
        f"current.{extension}"
    )

    if not current_file.is_file():

        return jsonify({
            "success": False,
            "error": "Current dataset not found."
        }), 404

    try:

        df = read_dataset(
            current_file
        )

        after = analyze_dataframe(
            df
        )

        before = (
            meta.get("last_before_stats")
            or after
        )

        operations = (
            meta.get("last_operations")
            or []
        )

        report_file = (
            session_dir /
            "report.pdf"
        )

        generate_pdf(
            report_file,
            meta.get(
                "original_filename",
                "dataset"
            ),
            before,
            after,
            operations
        )

        manager.touch(
            session_id
        )

        return send_file(
            report_file,
            as_attachment=True,
            download_name="csv_cleaning_report.pdf",
            mimetype="application/pdf"
        )

    except Exception:

        current_app.logger.exception(
            "Report generation failed"
        )

        return jsonify({
            "success": False,
            "error": "Unable to generate the PDF report."
        }), 500