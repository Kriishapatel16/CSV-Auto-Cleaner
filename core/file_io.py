from pathlib import Path
import os
import tempfile

import pandas as pd


SUPPORTED_EXTENSIONS = {
    ".csv",
    ".tsv",
    ".xlsx",
    ".xls",
    ".json",
}


def read_dataset(file_path):
    path = Path(file_path).resolve()

    if not path.is_file():
        raise FileNotFoundError("Dataset file was not found.")

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file format: {extension}")

    if extension == ".csv":
        return pd.read_csv(path)

    if extension == ".tsv":
        return pd.read_csv(path, sep="\t")

    if extension == ".xlsx":
        return pd.read_excel(
            path,
            engine="openpyxl"
        )

    if extension == ".xls":
        return pd.read_excel(
            path,
            engine="xlrd"
        )

    if extension == ".json":
        return pd.read_json(path)

    raise ValueError(f"Unsupported file format: {extension}")


def save_dataset(df, file_path):
    path = Path(file_path).resolve()
    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file format: {extension}")

    if extension == ".xls":
        raise ValueError(
            "Legacy XLS files are converted to XLSX for processing and download."
        )

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            dir=path.parent,
            suffix=extension,
            delete=False
        ) as temp_file:
            temp_path = Path(temp_file.name)

        if extension == ".csv":
            df.to_csv(
                temp_path,
                index=False
            )

        elif extension == ".tsv":
            df.to_csv(
                temp_path,
                sep="\t",
                index=False
            )

        elif extension == ".xlsx":
            df.to_excel(
                temp_path,
                index=False,
                engine="openpyxl"
            )

        elif extension == ".json":
            df.to_json(
                temp_path,
                orient="records",
                indent=2,
                date_format="iso"
            )

        os.replace(
            temp_path,
            path
        )

    except Exception:
        if temp_path is not None:
            try:
                temp_path.unlink(
                    missing_ok=True
                )
            except OSError:
                pass

        raise