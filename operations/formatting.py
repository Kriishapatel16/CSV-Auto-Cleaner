import re

import pandas as pd


def _validate_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")


def normalize_column_names(df):
    _validate_dataframe(df)

    original = list(df.columns)
    names = []
    used = set()

    for index, column in enumerate(original, 1):
        name = re.sub(
            r"[^a-zA-Z0-9]+",
            "_",
            str(column).strip()
        ).strip("_").lower()

        if not name:
            name = f"column_{index}"

        base = name
        suffix = 2

        while name in used:
            name = f"{base}_{suffix}"
            suffix += 1

        used.add(name)
        names.append(name)

    result = df.copy()
    result.columns = names

    changed = sum(
        str(a) != str(b)
        for a, b in zip(original, names)
    )

    return result, {
        "operation": "normalize_column_names",
        "description": f"Normalized {changed} column names.",
        "columns_changed": changed
    }


def standardize_missing_tokens(df):
    _validate_dataframe(df)

    tokens = {
        "",
        "na",
        "n/a",
        "null",
        "none",
        "nan",
        "nil",
        "-"
    }

    result = df.copy()
    changed = 0

    for column in result.select_dtypes(
        include="object"
    ).columns:

        def replace_token(value):
            nonlocal changed

            if (
                isinstance(value, str)
                and value.strip().lower() in tokens
            ):
                changed += 1
                return pd.NA

            return value

        result[column] = result[column].apply(
            replace_token
        )

    return result, {
        "operation": "standardize_missing_tokens",
        "description": (
            f"Standardized {changed} text tokens as missing values."
        ),
        "values_changed": changed
    }


def convert_numeric_text(df):
    _validate_dataframe(df)

    result = df.copy()
    changed = 0

    for column in result.select_dtypes(
        include="object"
    ).columns:

        cleaned = (
            result[column]
            .astype("string")
            .str.replace(",", "", regex=False)
            .str.strip()
        )

        converted = pd.to_numeric(
            cleaned,
            errors="coerce"
        )

        non_empty = (
            cleaned.notna()
            & cleaned.ne("")
        )

        if (
            int(non_empty.sum()) > 0
            and int(
                converted[non_empty].notna().sum()
            ) == int(non_empty.sum())
        ):
            result[column] = converted
            changed += 1

    return result, {
        "operation": "convert_numeric_text",
        "description": (
            f"Converted {changed} text columns to numeric where safe."
        ),
        "columns_changed": changed
    }


def remove_empty_columns(df):
    _validate_dataframe(df)

    before = len(df.columns)

    result = df.dropna(
        axis=1,
        how="all"
    )

    removed = before - len(result.columns)

    return result, {
        "operation": "remove_empty_columns",
        "description": (
            f"Removed {removed} completely empty columns."
        ),
        "columns_removed": removed
    }