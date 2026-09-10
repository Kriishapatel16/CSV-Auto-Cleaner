import pandas as pd


def _validate_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")


def remove_missing_rows(df):
    _validate_dataframe(df)

    before = len(df)

    result = (
        df.dropna()
        .reset_index(drop=True)
    )

    removed = before - len(result)

    return result, {
        "operation": "remove_missing_rows",
        "description": f"Removed {removed} rows containing missing values.",
        "rows_removed": removed
    }


def remove_missing_columns(df):
    _validate_dataframe(df)

    before = len(df.columns)

    result = df.dropna(axis=1)

    removed = before - len(result.columns)

    return result, {
        "operation": "remove_missing_columns",
        "description": f"Removed {removed} columns containing missing values.",
        "columns_removed": removed
    }


def fill_missing_mean(df):
    _validate_dataframe(df)

    result = df.copy()
    changed = 0

    for column in result.select_dtypes(
        include="number"
    ).columns:

        count = int(result[column].isna().sum())

        if count == 0:
            continue

        mean = result[column].mean()

        if pd.notna(mean):
            result[column] = result[column].fillna(mean)
            changed += count

    return result, {
        "operation": "fill_missing_mean",
        "description": f"Filled {changed} missing numeric values using mean.",
        "values_filled": changed
    }


def fill_missing_median(df):
    _validate_dataframe(df)

    result = df.copy()
    changed = 0

    for column in result.select_dtypes(
        include="number"
    ).columns:

        count = int(result[column].isna().sum())

        if count == 0:
            continue

        median = result[column].median()

        if pd.notna(median):
            result[column] = result[column].fillna(median)
            changed += count

    return result, {
        "operation": "fill_missing_median",
        "description": f"Filled {changed} missing numeric values using median.",
        "values_filled": changed
    }


def fill_missing_mode(df):
    _validate_dataframe(df)

    result = df.copy()
    changed = 0

    for column in result.columns:

        missing = int(result[column].isna().sum())

        if missing == 0:
            continue

        mode = result[column].mode(dropna=True)

        if not mode.empty:
            result[column] = result[column].fillna(mode.iloc[0])
            changed += missing

    return result, {
        "operation": "fill_missing_mode",
        "description": f"Filled {changed} missing values using the mode.",
        "values_filled": changed
    }


def fill_missing_static(df, value=""):
    _validate_dataframe(df)

    result = df.copy()

    before = int(
        result.isna().sum().sum()
    )

    result = result.fillna(value)

    after = int(
        result.isna().sum().sum()
    )

    changed = before - after

    return result, {
        "operation": "fill_missing_static",
        "description": f"Filled {changed} missing values.",
        "values_filled": changed
    }


def forward_fill(df):
    _validate_dataframe(df)

    result = df.copy()

    before = int(
        result.isna().sum().sum()
    )

    result = result.ffill()

    after = int(
        result.isna().sum().sum()
    )

    changed = before - after

    return result, {
        "operation": "forward_fill",
        "description": f"Filled {changed} values using forward fill.",
        "values_filled": changed
    }


def backward_fill(df):
    _validate_dataframe(df)

    result = df.copy()

    before = int(
        result.isna().sum().sum()
    )

    result = result.bfill()

    after = int(
        result.isna().sum().sum()
    )

    changed = before - after

    return result, {
        "operation": "backward_fill",
        "description": f"Filled {changed} values using backward fill.",
        "values_filled": changed
    }