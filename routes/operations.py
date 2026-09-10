from flask import (
    Blueprint,
    jsonify,
    request,
    current_app
)

from core.file_io import (
    read_dataset,
    save_dataset
)

from core.analysis_engine import (
    analyze_dataframe
)

from core.history_manager import (
    HistoryManager
)

from core.output_sanitizer import (
    sanitize_dataframe
)

from operations.registry import (
    get_operation
)


operations_bp = Blueprint(
    "operations",
    __name__,
    url_prefix="/api"
)


MAX_OPERATIONS_PER_REQUEST = 20
MAX_STATIC_VALUE_LENGTH = 200


@operations_bp.post(
    "/operations/<session_id>"
)
def process_operations(session_id):

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

    data = request.get_json(
        silent=True
    ) or {}

    selected = data.get(
        "operations"
    )

    if (
        not isinstance(selected, list)
        or not selected
    ):
        return jsonify({
            "success": False,
            "error": "No operations selected."
        }), 400

    if len(selected) > MAX_OPERATIONS_PER_REQUEST:
        return jsonify({
            "success": False,
            "error": "Too many operations selected at once."
        }), 400

    normalized = []
    seen = set()

    for item in selected:

        if not isinstance(item, dict):
            return jsonify({
                "success": False,
                "error": "Invalid operation format."
            }), 400

        operation_id = item.get(
            "id"
        )

        if not isinstance(operation_id, str):
            return jsonify({
                "success": False,
                "error": "Invalid operation ID."
            }), 400

        operation_id = operation_id.strip()

        if not operation_id:
            return jsonify({
                "success": False,
                "error": "Operation ID cannot be empty."
            }), 400

        if get_operation(operation_id) is None:
            return jsonify({
                "success": False,
                "error": (
                    f"Unsupported operation: {operation_id}"
                )
            }), 400

        if operation_id in seen:
            continue

        seen.add(
            operation_id
        )

        clean_item = {
            "id": operation_id
        }

        if operation_id == "fill_missing_static":

            value = item.get(
                "value",
                ""
            )

            if value is None:
                value = ""

            if not isinstance(
                value,
                (str, int, float, bool)
            ):
                return jsonify({
                    "success": False,
                    "error": "Invalid static fill value."
                }), 400

            value = str(value)

            if len(value) > MAX_STATIC_VALUE_LENGTH:
                return jsonify({
                    "success": False,
                    "error": "Static fill value is too long."
                }), 400

            clean_item["value"] = value

        normalized.append(
            clean_item
        )

    if not normalized:
        return jsonify({
            "success": False,
            "error": "No valid operations selected."
        }), 400

    try:

        df = read_dataset(
            current_file
        )

        before = analyze_dataframe(
            df
        )

        results = []

        for item in normalized:

            operation_id = item["id"]

            function = get_operation(
                operation_id
            )

            if operation_id == "fill_missing_static":

                df, result = function(
                    df,
                    item.get("value", "")
                )

            else:

                df, result = function(
                    df
                )

            if not hasattr(
                df,
                "columns"
            ):
                raise ValueError(
                    "Operation returned invalid dataset data."
                )

            results.append(
                result
            )

        after = analyze_dataframe(
            df
        )

        safe_df = sanitize_dataframe(
            df
        )

        history = HistoryManager(
            session_dir
        )

        history.create_snapshot(
            current_file
        )

        save_dataset(
            safe_df,
            current_file
        )

        manager.update_meta(
            session_id,
            last_before_stats=before,
            last_after_stats=after,
            last_operations=results
        )

        manager.touch(
            session_id
        )

        return jsonify({

            "success": True,

            "session_id": session_id,

            "before": before,

            "after": after,

            "operations": results

        })

    except Exception:

        current_app.logger.exception(
            "Dataset processing failed"
        )

        return jsonify({
            "success": False,
            "error": (
                "Unable to process the selected operations."
            )
        }), 500