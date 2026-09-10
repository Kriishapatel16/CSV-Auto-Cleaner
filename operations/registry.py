from operations.missing_values import (
    remove_missing_rows,
    remove_missing_columns,
    fill_missing_mean,
    fill_missing_median,
    fill_missing_mode,
    fill_missing_static,
    forward_fill,
    backward_fill
)

from operations.duplicates import (
    remove_duplicate_rows,
    remove_duplicate_columns,
    remove_all_duplicate_groups
)

from operations.text_cleaning import (
    trim_spaces,
    remove_extra_spaces,
    lowercase,
    uppercase,
    title_case
)

from operations.dates import (
    convert_to_datetime,
    remove_invalid_dates,
    extract_year,
    extract_month,
    extract_day
)

from operations.formatting import (
    normalize_column_names,
    standardize_missing_tokens,
    convert_numeric_text,
    remove_empty_columns
)

from operations.validation import (
    remove_invalid_email_rows,
    remove_invalid_date_rows
)

from operations.transformation import (
    remove_constant_columns,
    sort_columns,
    reset_row_index
)


OPERATION_REGISTRY = {
    "remove_missing_rows": remove_missing_rows,
    "remove_missing_columns": remove_missing_columns,
    "fill_missing_mean": fill_missing_mean,
    "fill_missing_median": fill_missing_median,
    "fill_missing_mode": fill_missing_mode,
    "fill_missing_static": fill_missing_static,
    "forward_fill": forward_fill,
    "backward_fill": backward_fill,

    "remove_duplicate_rows": remove_duplicate_rows,
    "remove_duplicate_columns": remove_duplicate_columns,
    "remove_all_duplicate_groups": remove_all_duplicate_groups,

    "trim_spaces": trim_spaces,
    "remove_extra_spaces": remove_extra_spaces,
    "lowercase": lowercase,
    "uppercase": uppercase,
    "title_case": title_case,

    "convert_to_datetime": convert_to_datetime,
    "remove_invalid_dates": remove_invalid_dates,
    "extract_year": extract_year,
    "extract_month": extract_month,
    "extract_day": extract_day,

    "normalize_column_names": normalize_column_names,
    "standardize_missing_tokens": standardize_missing_tokens,
    "convert_numeric_text": convert_numeric_text,
    "remove_empty_columns": remove_empty_columns,

    "remove_invalid_email_rows": remove_invalid_email_rows,
    "remove_invalid_date_rows": remove_invalid_date_rows,

    "remove_constant_columns": remove_constant_columns,
    "sort_columns": sort_columns,
    "reset_row_index": reset_row_index
}


def get_operation(name):
    if not isinstance(name, str):
        return None

    return OPERATION_REGISTRY.get(
        name.strip()
    )


def get_operation_names():
    return sorted(
        OPERATION_REGISTRY.keys()
    )