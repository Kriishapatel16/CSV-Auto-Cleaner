import pandas as pd


def _validate_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")


def remove_constant_columns(df):
    _validate_dataframe(df)

    columns = [
        column
        for column in df.columns
        if df[column].nunique(
            dropna=False
        ) <= 1
    ]

    result = df.drop(
        columns=columns
    )

    return result, {
        "operation": "remove_constant_columns",
        "description": (
            f"Removed {len(columns)} constant columns."
        ),
        "columns_removed": len(columns)
    }


def sort_columns(df):
    _validate_dataframe(df)

    result = df.reindex(
        sorted(
            df.columns,
            key=lambda value: str(value).lower()
        ),
        axis=1
    )

    changed = (
        list(df.columns)
        != list(result.columns)
    )

    return result, {
        "operation": "sort_columns",
        "description": "Sorted columns alphabetically.",
        "changed": changed
    }


def reset_row_index(df):
    _validate_dataframe(df)

    changed = not isinstance(
        df.index,
        pd.RangeIndex
    ) or not (
        df.index.start == 0
        and df.index.step == 1
    )

    result = df.reset_index(
        drop=True
    )

    return result, {
        "operation": "reset_row_index",
        "description": "Reset the dataset row index.",
        "changed": changed
    }