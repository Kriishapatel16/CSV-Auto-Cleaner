import pandas as pd

from core.quality_score import calculate_quality_score


def _column_type(series):
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "date"

    return "text"


def analyze_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")

    rows = int(len(df))
    columns = int(len(df.columns))
    total_cells = rows * columns

    missing = int(df.isna().sum().sum())

    duplicate_rows = (
        int(df.duplicated().sum())
        if rows
        else 0
    )

    type_counts = {
        "numeric": 0,
        "text": 0,
        "date": 0
    }

    missing_by_column = []

    for column in df.columns:
        kind = _column_type(df[column])
        type_counts[kind] += 1

        missing_by_column.append({
            "column": str(column),
            "missing": int(df[column].isna().sum())
        })

    missing_percentage = (
        (missing / total_cells) * 100
        if total_cells
        else 0
    )

    duplicate_percentage = (
        (duplicate_rows / rows) * 100
        if rows
        else 0
    )

    stats = {
        "rows": rows,
        "columns": columns,
        "total_cells": total_cells,
        "missing": missing,
        "missing_percentage": round(missing_percentage, 2),
        "duplicates": duplicate_rows,
        "duplicate_percentage": round(duplicate_percentage, 2),
        "numeric_columns": type_counts["numeric"],
        "text_columns": type_counts["text"],
        "date_columns": type_counts["date"],
        "column_type_counts": type_counts,
        "missing_by_column": missing_by_column,
        "memory_bytes": int(
            df.memory_usage(deep=True).sum()
        ),
        "estimated_processing_seconds": max(
            1,
            round(max(rows, 1) / 5000)
        )
    }

    stats["quality_score"] = calculate_quality_score(stats)

    return stats