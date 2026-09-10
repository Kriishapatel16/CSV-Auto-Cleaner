from pathlib import Path
import tempfile
import zipfile

from core.content_validator import (
    validate_saved_content,
    ContentValidationError
)


with tempfile.TemporaryDirectory() as temp:

    temp = Path(temp)

    csv_file = temp / "test.csv"
    csv_file.write_text(
        "Name,Age\nA,20\nB,21\n",
        encoding="utf-8"
    )

    validate_saved_content(
        csv_file,
        "csv"
    )

    print("CSV validation: OK")

    xlsx_file = temp / "test.xlsx"

    with zipfile.ZipFile(
        xlsx_file,
        "w"
    ) as archive:
        archive.writestr(
            "test.txt",
            "hello"
        )

    validate_saved_content(
        xlsx_file,
        "xlsx"
    )

    print("XLSX validation: OK")

    fake_xlsx = temp / "fake.xlsx"
    fake_xlsx.write_bytes(
        b"This is not an Excel file."
    )

    try:
        validate_saved_content(
            fake_xlsx,
            "xlsx"
        )

        print("Fake XLSX test: FAILED")

    except ContentValidationError:
        print("Fake XLSX test: BLOCKED")

    fake_csv = temp / "fake.csv"
    fake_csv.write_bytes(
        b"MZ\x90\x00\x03\x00\x00\x00"
    )

    try:
        validate_saved_content(
            fake_csv,
            "csv"
        )

        print("Fake CSV test: FAILED")

    except ContentValidationError:
        print("Fake CSV test: BLOCKED")