import re

import pandas as pd


def _validate_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")


def trim_spaces(df):
    _validate_dataframe(df)

    result = df.copy()
    changed = 0

    for column in result.select_dtypes(include="object").columns:
        original = result[column].copy()

        result[column] = result[column].apply(
            lambda value: value.strip()
            if isinstance(value, str)
            else value
        )

        changed += int(
            (original != result[column]).sum()
        )

    return result, {
        "operation": "trim_spaces",
        "description": (
            f"Trimmed unnecessary spaces from {changed} values."
        ),
        "values_changed": changed
    }


def remove_extra_spaces(df):
    _validate_dataframe(df)

    result = df.copy()
    changed = 0

    for column in result.select_dtypes(include="object").columns:
        original = result[column].copy()

        result[column] = result[column].apply(
            lambda value: re.sub(r"\s+", " ", value).strip()
            if isinstance(value, str)
            else value
        )

        changed += int(
            (original != result[column]).sum()
        )

    return result, {
        "operation": "remove_extra_spaces",
        "description": (
            f"Removed extra spaces from {changed} values."
        ),
        "values_changed": changed
    }


def lowercase(df):
    _validate_dataframe(df)

    result = df.copy()
    changed = 0

    for column in result.select_dtypes(include="object").columns:
        original = result[column].copy()

        result[column] = result[column].apply(
            lambda value: value.lower()
            if isinstance(value, str)
            else value
        )

        changed += int(
            (original != result[column]).sum()
        )

    return result, {
        "operation": "lowercase",
        "description": (
            f"Converted {changed} text values to lowercase."
        ),
        "values_changed": changed
    }


def uppercase(df):
    _validate_dataframe(df)

    result = df.copy()
    changed = 0

    for column in result.select_dtypes(include="object").columns:
        original = result[column].copy()

        result[column] = result[column].apply(
            lambda value: value.upper()
            if isinstance(value, str)
            else value
        )

        changed += int(
            (original != result[column]).sum()
        )

    return result, {
        "operation": "uppercase",
        "description": (
            f"Converted {changed} text values to uppercase."
        ),
        "values_changed": changed
    }


def title_case(df):
    _validate_dataframe(df)

    result = df.copy()
    changed = 0

    for column in result.select_dtypes(include="object").columns:
        original = result[column].copy()

        result[column] = result[column].apply(
            lambda value: value.title()
            if isinstance(value, str)
            else value
        )

        changed += int(
            (original != result[column]).sum()
        )

    return result, {
        "operation": "title_case",
        "description": (
            f"Converted {changed} text values to title case."
        ),
        "values_changed": changed
    }