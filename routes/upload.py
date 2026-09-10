from flask import (
    Blueprint,
    jsonify,
    request,
    current_app
)

from core.file_validator import (
    validate_file,
    validate_dataset_structure,
    FileValidationError
)

from core.content_validator import (
    validate_saved_content,
    ContentValidationError
)

from core.file_io import (
    read_dataset,
    save_dataset
)

from core.output_sanitizer import sanitize_dataframe


upload_bp = Blueprint(
    "upload",
    __name__,
    url_prefix="/api"
)


@upload_bp.post("/upload")
def upload_file():

    manager = current_app.session_manager

    session_id = None

    try:

        uploaded_file = request.files.get("file")

        if uploaded_file is None:

            raise FileValidationError(
                "Please select a file to upload."
            )

        info = validate_file(
            uploaded_file,
            current_app.config["ALLOWED_EXTENSIONS"],
            current_app.config["MAX_CONTENT_LENGTH"]
        )

        session_id = manager.create_session(
            info["extension"],
            info["filename"],
            info["size"]
        )

        session_dir = manager.get_session_path(
            session_id
        )

        if session_dir is None:

            raise RuntimeError(
                "Unable to create upload session."
            )

        original_path = (
            session_dir /
            f"original.{info['extension']}"
        )

        uploaded_file.save(original_path)

        validate_saved_content(
            original_path,
            info["extension"]
        )

        validate_dataset_structure(
            original_path,
            info["extension"]
        )

        df = read_dataset(original_path)

        safe_df = sanitize_dataframe(df)

        working_extension = info["extension"]

        current_path = (
            session_dir /
            f"current.{working_extension}"
        )

        if info["extension"] == "xls":

            working_extension = "xlsx"

            current_path = (
                session_dir /
                "current.xlsx"
            )

        save_dataset(
            safe_df,
            current_path
        )

        manager.update_meta(
            session_id,
            working_extension=working_extension
        )

        manager.touch(
            session_id
        )

        manager.cleanup_expired()

        return jsonify({

            "success": True,

            "session_id": session_id,

            "filename": info["filename"],

            "extension": info["extension"],

            "working_extension": working_extension,

            "size": info["size"]
        })

    except (
        FileValidationError,
        ContentValidationError
    ) as error:

        if session_id:
            manager.delete_session(
                session_id
            )

        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except Exception:

        if session_id:
            manager.delete_session(
                session_id
            )

        current_app.logger.exception(
            "Upload failed"
        )

        return jsonify({
            "success": False,
            "error": "Unable to process the uploaded file."
        }), 500