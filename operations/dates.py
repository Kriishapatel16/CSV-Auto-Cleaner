import pandas as pd


def _validate_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")


def _convert_series(series):
    return pd.to_datetime(
        series,
        errors="coerce",
        format="mixed"
    )


def convert_to_datetime(df):
    _validate_dataframe(df)

    result = df.copy()
    changed = 0

    for column in result.select_dtypes(include="object").columns:
        converted = _convert_series(result[column])

        valid = (
            result[column].notna()
            & converted.notna()
        )

        changed += int(valid.sum())

        result[column] = converted

    return result, {
        "operation": "convert_to_datetime",
        "description": f"Converted {changed} values to date format.",
        "values_changed": changed
    }


def remove_invalid_dates(df):
    _validate_dataframe(df)

    result = df.copy()
    date_columns = []

    for column in result.select_dtypes(include="object").columns:
        converted = _convert_series(result[column])

        valid_count = int(
            converted.notna().sum()
        )

        if valid_count > 0:
            date_columns.append(column)

    removed = 0

    for column in date_columns:
        converted = _convert_series(result[column])

        invalid = (
            result[column].notna()
            & converted.isna()
        )

        removed += int(invalid.sum())

        result = result.loc[
            ~invalid
        ]

    result = result.reset_index(drop=True)

    return result, {
        "operation": "remove_invalid_dates",
        "description": f"Removed {removed} rows containing invalid dates.",
        "rows_removed": removed
    }


def extract_year(df):
    _validate_dataframe(df)

    result = df.copy()
    changed = 0

    for column in result.select_dtypes(
        include=["datetime", "object"]
    ).columns:

        converted = _convert_series(result[column])
        valid = converted.notna()

        if valid.any():
            result[f"{column}_year"] = converted.dt.year
            changed += int(valid.sum())

    return result, {
        "operation": "extract_year",
        "description": f"Extracted year from {changed} date values.",
        "values_changed": changed
    }


def extract_month(df):
    _validate_dataframe(df)

    result = df.copy()
    changed = 0

    for column in result.select_dtypes(
        include=["datetime", "object"]
    ).columns:

        converted = _convert_series(result[column])
        valid = converted.notna()

        if valid.any():
            result[f"{column}_month"] = converted.dt.month
            changed += int(valid.sum())

    return result, {
        "operation": "extract_month",
        "description": f"Extracted month from {changed} date values.",
        "values_changed": changed
    }


def extract_day(df):
    _validate_dataframe(df)

    result = df.copy()
    changed = 0

    for column in result.select_dtypes(
        include=["datetime", "object"]
    ).columns:

        converted = _convert_series(result[column])
        valid = converted.notna()

        if valid.any():
            result[f"{column}_day"] = converted.dt.day
            changed += int(valid.sum())

    return result, {
        "operation": "extract_day",
        "description": f"Extracted day from {changed} date values.",
        "values_changed": changed
    }