import pandas as pd


def _validate_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")


def remove_duplicate_rows(df, keep="first"):
    _validate_dataframe(df)

    if keep not in {"first", "last", False}:
        keep = "first"

    before = len(df)

    result = (
        df.drop_duplicates(keep=keep)
        .reset_index(drop=True)
    )

    removed = before - len(result)

    return result, {
        "operation": "remove_duplicate_rows",
        "description": f"Removed {removed} duplicate rows.",
        "rows_removed": removed
    }


def remove_duplicate_columns(df):
    _validate_dataframe(df)

    before = len(df.columns)

    result = df.loc[
        :,
        ~df.columns.duplicated()
    ]

    removed = before - len(result.columns)

    return result, {
        "operation": "remove_duplicate_columns",
        "description": f"Removed {removed} duplicate columns.",
        "columns_removed": removed
    }


def remove_all_duplicate_groups(df):
    _validate_dataframe(df)

    duplicate_mask = df.duplicated(
        keep=False
    )

    removed = int(
        duplicate_mask.sum()
    )

    result = (
        df.loc[~duplicate_mask]
        .reset_index(drop=True)
    )

    return result, {
        "operation": "remove_all_duplicate_groups",
        "description": (
            f"Removed {removed} rows belonging to duplicate groups."
        ),
        "rows_removed": removed
    }