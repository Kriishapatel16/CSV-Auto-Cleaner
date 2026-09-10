import re

import pandas as pd


EMAIL_RE = re.compile(
    r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
)


def _validate_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")


def _candidate_email_columns(df):
    return [
        column
        for column in df.columns
        if (
            "email" in str(column).lower()
            or "e-mail" in str(column).lower()
        )
    ]


def remove_invalid_email_rows(df):
    _validate_dataframe(df)

    columns = _candidate_email_columns(df)

    if not columns:
        return df.copy(), {
            "operation": "remove_invalid_email_rows",
            "description": (
                "No email-like columns were detected; no rows removed."
            ),
            "rows_removed": 0
        }

    mask = pd.Series(
        True,
        index=df.index
    )

    for column in columns:
        values = df[column]

        valid = values.isna()

        non_missing = values.notna()

        valid.loc[non_missing] = (
            values.loc[non_missing]
            .astype(str)
            .str.strip()
            .map(
                lambda value: bool(
                    EMAIL_RE.fullmatch(value)
                )
            )
        )

        mask &= valid

    removed = int(
        (~mask).sum()
    )

    result = (
        df.loc[mask]
        .reset_index(drop=True)
    )

    return result, {
        "operation": "remove_invalid_email_rows",
        "description": (
            f"Removed {removed} rows with invalid email values."
        ),
        "rows_removed": removed
    }


def remove_invalid_date_rows(df):
    _validate_dataframe(df)

    candidates = [
        column
        for column in df.columns
        if any(
            token in str(column).lower()
            for token in (
                "date",
                "time",
                "dob",
                "created",
                "updated"
            )
        )
    ]

    if not candidates:
        return df.copy(), {
            "operation": "remove_invalid_date_rows",
            "description": (
                "No date-like columns were detected; no rows removed."
            ),
            "rows_removed": 0
        }

    mask = pd.Series(
        True,
        index=df.index
    )

    for column in candidates:
        parsed = pd.to_datetime(
            df[column],
            errors="coerce",
            format="mixed"
        )

        valid = (
            df[column].isna()
            | parsed.notna()
        )

        mask &= valid

    removed = int(
        (~mask).sum()
    )

    result = (
        df.loc[mask]
        .reset_index(drop=True)
    )

    return result, {
        "operation": "remove_invalid_date_rows",
        "description": (
            f"Removed {removed} rows with invalid date values."
        ),
        "rows_removed": removed
    }