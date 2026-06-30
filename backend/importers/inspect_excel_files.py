#!/usr/bin/env python3
"""
Excel File Inspector for Green Compute System.

Scans all Excel files in data/raw/, outputs:
- File name
- Sheet names
- Row count
- Column names (first 15 shown in report, full list in detailed output)
- First 5 rows as sample data

Generates a report at data/excel_inspection_report.md.
Run this FIRST before adjusting data_import_config.yaml or running the import.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

import pandas as pd
import openpyxl


def get_project_root():
    """Get project root directory (parent of backend/)."""
    return Path(__file__).resolve().parent.parent.parent


def inspect_excel(file_path: Path) -> dict:
    """Inspect a single Excel file and return its structure."""
    result = {
        "file_name": file_path.name,
        "file_path": str(file_path),
        "file_size_kb": round(file_path.stat().st_size / 1024, 1),
        "sheets": [],
    }

    try:
        xl = pd.ExcelFile(file_path)
        for sheet_name in xl.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            sheet_info = {
                "sheet_name": sheet_name,
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": list(df.columns),
                "sample_rows": [],
            }
            # Get first 5 rows as samples
            for i, row in df.head(5).iterrows():
                sample = {}
                for col in df.columns[:10]:  # First 10 columns only
                    val = row[col]
                    if pd.notna(val):
                        sample[str(col)] = str(val)[:60]
                    else:
                        sample[str(col)] = "NULL"
                sheet_info["sample_rows"].append(sample)
            result["sheets"].append(sheet_info)
    except Exception as e:
        result["error"] = str(e)

    return result


def generate_markdown_report(results: list, output_path: Path):
    """Generate a Markdown inspection report."""
    lines = []
    lines.append("# Excel File Inspection Report")
    lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Directory:** `data/raw/`")
    lines.append(f"**Total files:** {len(results)}\n")
    lines.append("---\n")

    # Summary table
    lines.append("## Summary\n")
    lines.append("| # | File | Sheets | Total Rows | Size (KB) | Status |")
    lines.append("|---|------|--------|------------|-----------|--------|")
    for i, r in enumerate(results, 1):
        status = "❌ Error" if "error" in r else "✅ OK"
        sheet_count = len(r["sheets"])
        total_rows = sum(s["rows"] for s in r["sheets"]) if "sheets" in r else 0
        lines.append(
            f"| {i} | {r['file_name']} | {sheet_count} | {total_rows} | "
            f"{r['file_size_kb']} | {status} |"
        )
    lines.append("")

    # Detailed per file
    lines.append("---\n")
    lines.append("## Detailed Inspection\n")

    for i, r in enumerate(results, 1):
        lines.append(f"### {i}. {r['file_name']}\n")
        lines.append(f"- **Path:** `{r['file_path']}`")
        lines.append(f"- **Size:** {r['file_size_kb']} KB")

        if "error" in r:
            lines.append(f"- **❌ Error:** {r['error']}\n")
            continue

        lines.append(f"- **Sheets:** {len(r['sheets'])}\n")

        for sheet in r["sheets"]:
            lines.append(f"#### Sheet: `{sheet['sheet_name']}`\n")
            lines.append(f"- **Rows:** {sheet['rows']}")
            lines.append(f"- **Columns:** {sheet['columns']}")

            # Column names
            cols = sheet["column_names"]
            lines.append(f"- **Column Names:**")
            for j, col in enumerate(cols):
                lines.append(f"  {j+1}. `{col}`")

            # Sample rows
            if sheet["sample_rows"]:
                lines.append(f"\n**First {min(5, len(sheet['sample_rows']))} rows:**\n")
                lines.append("| # | " + " | ".join(list(sheet["sample_rows"][0].keys())[:8]) + " |")
                lines.append("|---|" + "|".join(["---"] * min(8, len(sheet["sample_rows"][0]))) + "|")
                for k, sample in enumerate(sheet["sample_rows"][:5], 1):
                    vals = list(sample.values())[:8]
                    lines.append(f"| {k} | " + " | ".join(vals) + " |")
            lines.append("")

    lines.append("---\n")
    lines.append("## Field Ambiguity Notes\n")
    lines.append("The following fields MAY need manual confirmation:\n")
    lines.append("1. **Province names** — Verify all province names match the standard short form")
    lines.append('   (e.g., "内蒙古" not "内蒙古自治区").')
    lines.append("2. **Year values** — Confirm all year values fall within 2016-2024 range.")
    lines.append("3. **Numeric fields** — Check for unexpected string values in numeric columns.")
    lines.append('4. **Unnamed columns** — Some sheets (e.g., Markov transition matrices) have')
    lines.append("   unnamed first columns. Column mapping in the import config must handle these.")
    lines.append("5. **Region values** — Verify region values are one of: 东部, 中部, 西部, 东北.")
    lines.append("6. **LPA types** — Verify LPA type values match the 4 defined types.")
    lines.append("")

    # Write
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return output_path


def main():
    project_root = get_project_root()
    raw_dir = project_root / "data" / "raw"
    output_path = project_root / "data" / "excel_inspection_report.md"

    if not raw_dir.exists():
        print(f"❌ Directory not found: {raw_dir}")
        sys.exit(1)

    # Find all Excel files
    excel_files = sorted([
        f for f in raw_dir.iterdir()
        if f.suffix.lower() in (".xlsx", ".xls") and not f.name.startswith("~$")
    ])

    if not excel_files:
        print(f"❌ No Excel files found in {raw_dir}")
        sys.exit(1)

    print(f"📂 Found {len(excel_files)} Excel file(s) in {raw_dir}")
    print(f"{'='*70}")

    results = []
    for f in excel_files:
        print(f"\n🔍 Inspecting: {f.name} ...")
        result = inspect_excel(f)

        if "error" in result:
            print(f"  ❌ Error: {result['error']}")
        else:
            for sheet in result["sheets"]:
                print(f"  📄 Sheet '{sheet['sheet_name']}': "
                      f"{sheet['rows']} rows × {sheet['columns']} columns")
                col_preview = ", ".join(str(c) for c in sheet["column_names"][:8])
                if len(sheet["column_names"]) > 8:
                    col_preview += f" ... (+{len(sheet['column_names']) - 8} more)"
                print(f"     Columns: {col_preview}")

        results.append(result)

    # Generate report
    report_path = generate_markdown_report(results, output_path)
    print(f"\n{'='*70}")
    print(f"✅ Inspection report saved to: {report_path}")
    print(f"\n📋 Next steps:")
    print(f"  1. Review the report at {report_path}")
    print(f"  2. Update backend/importers/data_import_config.yaml if needed")
    print(f"  3. Run: psql -U postgres -h localhost -d green_compute -f backend/db/schema.sql")
    print(f"  4. Run: python backend/importers/import_excel_to_db.py")


if __name__ == "__main__":
    main()
