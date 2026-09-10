import pandas as pd


DANGEROUS_PREFIXES = (
    "=",
    "+",
    "-",
    "@"
)


def sanitize_dataframe(df):

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")

    result = df.copy()

    for column in result.columns:

        result[column] = result[column].map(
            _sanitize_value
        )

    return result


def _sanitize_value(value):

    if not isinstance(value, str):
        return value

    stripped = value.lstrip()

    if stripped.startswith(DANGEROUS_PREFIXES):
        leading_spaces = value[:len(value) - len(stripped)]
        return leading_spaces + "'" + stripped

    return value