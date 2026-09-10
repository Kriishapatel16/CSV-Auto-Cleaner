from pathlib import Path
import zipfile


MAX_ZIP_ENTRIES = 5000
MAX_UNCOMPRESSED_SIZE = 500 * 1024 * 1024
MAX_COMPRESSION_RATIO = 1000


class ContentValidationError(ValueError):
    pass


MAGIC_SIGNATURES = {
    "xlsx": b"PK\x03\x04",
    "xls": b"\xD0\xCF\x11\xE0",
}


def validate_saved_content(file_path, extension):
    path = Path(file_path).resolve()

    if not path.is_file():
        raise ContentValidationError(
            "Uploaded file could not be found."
        )

    extension = str(extension).lower().lstrip(".")

    if extension not in {
        "csv",
        "tsv",
        "json",
        "xlsx",
        "xls",
    }:
        raise ContentValidationError(
            "Unsupported file format."
        )

    try:
        with path.open("rb") as file:
            header = file.read(8)
    except OSError:
        raise ContentValidationError(
            "Unable to inspect uploaded file."
        )

    if extension == "xlsx":
        _validate_xlsx(path, header)

    elif extension == "xls":
        _validate_xls(header)

    else:
        _validate_text_file(path, header)


def _validate_xlsx(path, header):

    if not header.startswith(
        MAGIC_SIGNATURES["xlsx"]
    ):
        raise ContentValidationError(
            "The XLSX file content does not match its file type."
        )

    if not zipfile.is_zipfile(path):
        raise ContentValidationError(
            "The XLSX file is invalid or corrupted."
        )

    try:
        with zipfile.ZipFile(path, "r") as archive:

            entries = archive.infolist()

            if len(entries) > MAX_ZIP_ENTRIES:
                raise ContentValidationError(
                    "The XLSX file contains too many internal files."
                )

            total_size = 0

            for entry in entries:

                if entry.file_size < 0:
                    raise ContentValidationError(
                        "The XLSX file contains invalid data."
                    )

                total_size += entry.file_size

                if total_size > MAX_UNCOMPRESSED_SIZE:
                    raise ContentValidationError(
                        "The XLSX file expands beyond the allowed size."
                    )

                if (
                    entry.compress_size > 0
                    and entry.file_size / entry.compress_size
                    > MAX_COMPRESSION_RATIO
                ):
                    raise ContentValidationError(
                        "The XLSX file has an unsafe compression ratio."
                    )

    except zipfile.BadZipFile:
        raise ContentValidationError(
            "The XLSX file is corrupted."
        )


def _validate_xls(header):

    if not header.startswith(
        MAGIC_SIGNATURES["xls"]
    ):
        raise ContentValidationError(
            "The XLS file content does not match its file type."
        )


def _validate_text_file(path, header):

    suspicious_signatures = (
        b"\xD0\xCF\x11\xE0",
        b"PK\x03\x04",
        b"\x7FELF",
        b"MZ",
    )

    if any(
        header.startswith(signature)
        for signature in suspicious_signatures
    ):
        raise ContentValidationError(
            "The file content does not match the selected text format."
        )

    try:
        with path.open(
            "r",
            encoding="utf-8-sig"
        ) as file:
            file.read(1024 * 1024)

    except UnicodeDecodeError:
        raise ContentValidationError(
            "The text file encoding is not supported."
        )

    except OSError:
        raise ContentValidationError(
            "Unable to inspect the uploaded text file."
        )