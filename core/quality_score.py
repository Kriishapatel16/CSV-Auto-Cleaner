def calculate_quality_score(stats):
    missing_percentage = float(
        stats.get("missing_percentage", 0)
    )

    duplicate_percentage = float(
        stats.get("duplicate_percentage", 0)
    )

    missing_percentage = max(
        0,
        min(missing_percentage, 100)
    )

    duplicate_percentage = max(
        0,
        min(duplicate_percentage, 100)
    )

    missing_score = 100 - missing_percentage
    duplicate_score = 100 - duplicate_percentage

    score = (
        missing_score * 0.60
        + duplicate_score * 0.40
    )

    return int(round(
        max(0, min(score, 100))
    ))