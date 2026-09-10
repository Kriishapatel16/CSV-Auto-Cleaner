from datetime import datetime
from html import escape
from pathlib import Path
import os
import tempfile

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import mm

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def _safe_text(value):
    return escape(str(value))


def _change_text(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return "0"

    if value > 0:
        return f"+{value}"

    return str(value)


def generate_pdf(
    report_path,
    filename,
    before,
    after,
    operations
):

    report_path = Path(report_path).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)

    before = before or {}
    after = after or {}
    operations = operations or []

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="SmallGray",
            parent=styles["BodyText"],
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#64748B")
        )
    )

    styles.add(
        ParagraphStyle(
            name="ReportSubtitle",
            parent=styles["Heading2"],
            fontSize=15,
            leading=20,
            textColor=colors.HexColor("#334155"),
            spaceAfter=5
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading3"],
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#0F172A"),
            spaceBefore=4,
            spaceAfter=5
        )
    )

    styles.add(
        ParagraphStyle(
            name="OperationText",
            parent=styles["BodyText"],
            fontSize=9.5,
            leading=14,
            textColor=colors.HexColor("#334155")
        )
    )

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            dir=report_path.parent,
            suffix=".pdf",
            delete=False
        ) as temp_file:
            temp_path = Path(temp_file.name)

        doc = SimpleDocTemplate(
            str(temp_path),
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm
        )

        generated_at = datetime.now().strftime(
            "%d %B %Y, %I:%M %p"
        )

        before_rows = int(before.get("rows", 0))
        after_rows = int(after.get("rows", 0))

        before_columns = int(before.get("columns", 0))
        after_columns = int(after.get("columns", 0))

        before_missing = int(before.get("missing", 0))
        after_missing = int(after.get("missing", 0))

        before_duplicates = int(before.get("duplicates", 0))
        after_duplicates = int(after.get("duplicates", 0))

        before_quality = int(before.get("quality_score", 0))
        after_quality = int(after.get("quality_score", 0))

        story = [

            Paragraph(
                "CSV Auto Cleaner",
                styles["Title"]
            ),

            Paragraph(
                "Dataset Cleaning Report",
                styles["ReportSubtitle"]
            ),

            Paragraph(
                f"File: {_safe_text(filename or 'dataset')}",
                styles["SmallGray"]
            ),

            Paragraph(
                f"Generated: {generated_at}",
                styles["SmallGray"]
            ),

            Spacer(1, 8 * mm),

            Paragraph(
                "Cleaning Summary",
                styles["SectionHeading"]
            )
        ]

        data = [

            [
                "Metric",
                "Before",
                "After",
                "Change"
            ],

            [
                "Rows",
                before_rows,
                after_rows,
                _change_text(after_rows - before_rows)
            ],

            [
                "Columns",
                before_columns,
                after_columns,
                _change_text(
                    after_columns - before_columns
                )
            ],

            [
                "Missing values",
                before_missing,
                after_missing,
                _change_text(
                    after_missing - before_missing
                )
            ],

            [
                "Duplicate rows",
                before_duplicates,
                after_duplicates,
                _change_text(
                    after_duplicates - before_duplicates
                )
            ],

            [
                "Quality score",
                before_quality,
                after_quality,
                _change_text(
                    after_quality - before_quality
                )
            ]
        ]

        table = Table(
            data,
            colWidths=[
                55 * mm,
                35 * mm,
                35 * mm,
                35 * mm
            ],
            repeatRows=1
        )

        table.setStyle(
            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#EFF6FF")
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#0F172A")
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#CBD5E1")
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),

                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "CENTER"
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F8FAFC")
                    ]
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ])
        )

        story.extend([
            table,
            Spacer(1, 8 * mm),
            Paragraph(
                "Operations Applied",
                styles["SectionHeading"]
            )
        ])

        if operations:

            for item in operations:

                if not isinstance(item, dict):
                    continue

                description = (
                    item.get("description")
                    or item.get("operation")
                    or "Operation completed"
                )

                story.append(
                    Paragraph(
                        f"• {_safe_text(description)}",
                        styles["OperationText"]
                    )
                )

                story.append(
                    Spacer(1, 2 * mm)
                )

        else:

            story.append(
                Paragraph(
                    "No cleaning operations were recorded for this round.",
                    styles["OperationText"]
                )
            )

        story.extend([

            Spacer(1, 8 * mm),

            Paragraph(
                "Report Information",
                styles["SectionHeading"]
            ),

            Paragraph(
                "The report contains summary statistics and cleaning "
                "operations only. Dataset contents are not embedded "
                "in the PDF.",
                styles["SmallGray"]
            ),

            Spacer(1, 4 * mm),

            Paragraph(
                "The dataset was processed inside a temporary session.",
                styles["SmallGray"]
            )
        ])

        doc.build(story)

        os.replace(temp_path, report_path)

        return report_path

    except Exception:

        if temp_path is not None:

            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass

        raise