import pandas as pd

from core.output_sanitizer import sanitize_dataframe


df = pd.DataFrame({
    "Name": [
        "Alice",
        "=HYPERLINK(\"http://example.com\")",
        "+12345",
        "-12345",
        "@SUM(A1:A2)",
        "Normal text"
    ]
})


cleaned = sanitize_dataframe(df)

print(cleaned.to_string(index=False))

assert cleaned.iloc[0, 0] == "Alice"
assert cleaned.iloc[1, 0].startswith("'=")
assert cleaned.iloc[2, 0].startswith("'+")
assert cleaned.iloc[3, 0].startswith("'-")
assert cleaned.iloc[4, 0].startswith("'@")
assert cleaned.iloc[5, 0] == "Normal text"

print("Formula injection protection: OK")