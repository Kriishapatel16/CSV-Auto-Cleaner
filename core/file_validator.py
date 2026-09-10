from pathlib import Path

import pandas as pd
from werkzeug.utils import secure_filename


class FileValidationError(ValueError):
    pass


def get_extension(filename):
    return (
        Path(filename or "")
        .suffix
        .lower()
        .lstrip(".")
    )


def validate_file(file_storage, allowed_extensions, max_size):
    if file_storage is None:
        raise FileValidationError("No file was uploaded.")

    original_filename = (file_storage.filename or "").strip()

    if not original_filename:
        raise FileValidationError("Please select a file.")

    safe_filename = secure_filename(original_filename)

    if not safe_filename:
        raise FileValidationError("The uploaded filename is invalid.")

    extension = get_extension(safe_filename)

    allowed = {
        str(value).lower().lstrip(".")
        for value in allowed_extensions
    }

    if extension not in allowed:
        raise FileValidationError(
            "Unsupported file type. Allowed formats: CSV, XLSX, XLS, JSON, TSV."
        )

    try:
        current_position = file_storage.stream.tell()
        file_storage.stream.seek(0, 2)
        size = file_storage.stream.tell()
        file_storage.stream.seek(current_position)
    except (OSError, AttributeError):
        raise FileValidationError(
            "Unable to determine uploaded file size."
        )

    if size <= 0:
        raise FileValidationError("The uploaded file is empty.")

    if size > max_size:
        raise FileValidationError(
            "File exceeds the maximum size of 100 MB."
        )

    return {
        "filename": safe_filename,
        "extension": extension,
        "size": size
    }


def validate_dataset_structure(file_path, extension):
    file_path = Path(file_path)

    if not file_path.is_file():
        raise FileValidationError("Uploaded file could not be found.")

    extension = str(extension).lower().lstrip(".")

    try:
        if extension == "csv":
            df = pd.read_csv(
                file_path,
                nrows=1000
            )

        elif extension == "tsv":
            df = pd.read_csv(
                file_path,
                sep="\t",
                nrows=1000
            )

        elif extension == "xlsx":
            df = pd.read_excel(
                file_path,
                engine="openpyxl",
                nrows=1000
            )

        elif extension == "xls":
            df = pd.read_excel(
                file_path,
                engine="xlrd",
                nrows=1000
            )

        elif extension == "json":
            df = pd.read_json(file_path).head(1000)

        else:
            raise FileValidationError(
                "Unsupported file format."
            )

    except FileValidationError:
        raise

    except Exception:
        raise FileValidationError(
            "The uploaded file could not be read. "
            "It may be corrupted or have an invalid format."
        )

    if df.shape[1] == 0:
        raise FileValidationError(
            "The dataset does not contain any columns."
        )

    return df