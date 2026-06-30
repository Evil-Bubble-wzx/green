#!/usr/bin/env python3
"""
Excel to PostgreSQL Data Importer for Green Compute System.

Reads data_import_config.yaml, imports each Excel file into the corresponding
PostgreSQL table with:
- Column renaming (Chinese -> English) per column_mapping
- Empty row removal
- Whitespace trimming
- Province name standardization
- Region value standardization
- Required field validation
- Unique key duplicate checking
- Year range validation (2016-2024)
- Probability range validation (0-1)
- Numeric field type checking
- Append mode (default) — duplicates written to validation report

Generates: data/data_validation_report.md
"""

import os
import sys
import re
import logging
from pathlib import Path
from datetime import datetime
from collections import defaultdict

import pandas as pd
import numpy as np
import yaml
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect as sa_inspect

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

def get_project_root():
    return Path(__file__).resolve().parent.parent.parent


def setup_logging():
    """Configure logging to stdout."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    return logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

def get_engine():
    """Create SQLAlchemy engine from .env DATABASE_URL."""
    project_root = get_project_root()
    dotenv_path = project_root / ".env"
    load_dotenv(dotenv_path)

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ DATABASE_URL not found in .env")
        print("   Create .env with:")
        print("   DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/green_compute")
        sys.exit(1)

    # Mask password for logging
    masked = re.sub(r"://([^:]+):([^@]+)@", r"://\1:****@", db_url)
    logger.info(f"Database URL: {masked}")

    return create_engine(db_url)


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

def load_config(config_path: Path) -> dict:
    """Load YAML import configuration."""
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    logger.info(f"Loaded config: {len(config.get('imports', []))} import definitions")
    return config


# ---------------------------------------------------------------------------
# Province / Region standardization
# ---------------------------------------------------------------------------

def build_province_standardizer(config: dict) -> dict:
    """Build province name standardization mapping."""
    mapping = config.get("province_standardization", {})
    # Add self-mapping for all known provinces
    for prov in config.get("region_mapping", {}).keys():
        if prov not in mapping:
            mapping[prov] = prov
    return mapping


def build_region_lookup(config: dict) -> dict:
    """Build province -> region lookup."""
    return config.get("region_mapping", {})


def build_hub_set(config: dict) -> set:
    """Build set of hub province names."""
    return set(config.get("hub_provinces", []))


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def check_year_range(values: pd.Series, min_year: int, max_year: int) -> list:
    """Check year values are within expected range. Returns list of out-of-range values."""
    if values.dropna().empty:
        return []
    vals = pd.to_numeric(values, errors="coerce").dropna()
    out_of_range = vals[(vals < min_year) | (vals > max_year)]
    return sorted(out_of_range.unique().tolist())


def check_probability_range(values: pd.Series) -> list:
    """Check probability values are in [0, 1]. Returns list of out-of-range values."""
    if values.dropna().empty:
        return []
    vals = pd.to_numeric(values, errors="coerce").dropna()
    out_of_range = vals[(vals < 0) | (vals > 1)]
    return sorted(out_of_range.unique().tolist())[:10]  # top 10


def check_numeric(values: pd.Series) -> int:
    """Count non-numeric values in a supposed numeric column."""
    if values.dropna().empty:
        return 0
    numeric_vals = pd.to_numeric(values, errors="coerce")
    return numeric_vals.isna().sum()


# ---------------------------------------------------------------------------
# Data dictionary enrichment
# ---------------------------------------------------------------------------

def enrich_from_dictionary(
    df: pd.DataFrame, import_def: dict, project_root: Path
) -> pd.DataFrame:
    """
    Enrich a DataFrame with fields from the data dictionary.

    Reads dictionary Excel, matches on ``match_field``, and pulls the
    configured ``fields`` into the DataFrame.  Every row in *df* must find
    a match — unmatched rows cause a ``ValueError`` listing the missing keys.

    Parameters
    ----------
    df : DataFrame
        Already-renamed data from the source Excel.
    import_def : dict
        The import definition (must contain a ``dictionary`` block).
    project_root : Path
        Project root for resolving relative dictionary paths.

    Returns
    -------
    DataFrame with additional columns merged from the dictionary.
    """
    dict_cfg = import_def.get("dictionary")
    if not dict_cfg:
        return df

    dict_path = project_root / dict_cfg["path"]
    dict_sheet = dict_cfg["sheet"]
    match_field = dict_cfg["match_field"]
    field_map = dict_cfg["fields"]  # db_field -> dict_column_name

    if not dict_path.exists():
        raise FileNotFoundError(f"Dictionary not found: {dict_path}")

    dict_df = pd.read_excel(dict_path, sheet_name=dict_sheet, header=3)
    # dict_df columns are already the header names from the dictionary

    if match_field not in df.columns:
        raise KeyError(
            f"Match field '{match_field}' not in source DataFrame. "
            f"Available columns: {list(df.columns)}"
        )

    # Build a lookup: for each match_field value, get the dict fields
    dict_cols_needed = [match_field] + list(field_map.values())
    missing_in_dict = [c for c in dict_cols_needed if c not in dict_df.columns]
    if missing_in_dict:
        raise KeyError(
            f"Columns {missing_in_dict} not found in dictionary sheet "
            f"'{dict_sheet}'. Available: {list(dict_df.columns)}"
        )

    lookup = dict_df[dict_cols_needed].drop_duplicates(subset=[match_field])
    lookup = lookup.dropna(subset=[match_field])
    # Strip whitespace for robust matching
    lookup[match_field] = lookup[match_field].astype(str).str.strip()

    # Prepare source keys
    source_keys = df[match_field].astype(str).str.strip()

    # Check for unmatched rows BEFORE merging
    lookup_values = set(lookup[match_field])
    unmatched = source_keys[~source_keys.isin(lookup_values)].unique()
    if len(unmatched) > 0:
        raise ValueError(
            f"Cannot match {len(unmatched)} indicator(s) in the data dictionary:\n"
            + "\n".join(f"  - {u}" for u in sorted(unmatched))
            + f"\n\nPlease add these indicators to {dict_path} sheet '{dict_sheet}'."
        )

    # Merge: rename dict columns to DB field names
    rename_map = {v: k for k, v in field_map.items()}
    lookup_renamed = lookup.rename(columns=rename_map)
    # Keep only the DB fields + match_field
    cols_to_merge = [match_field] + list(field_map.keys())
    lookup_renamed = lookup_renamed[cols_to_merge]

    # Merge into df
    merged = df.merge(lookup_renamed, on=match_field, how="left")

    # For any columns that exist in both (e.g., dimension, direction),
    # prefer the dictionary value when the Excel value is missing
    for col in field_map:
        if col in df.columns and col in merged.columns:
            # If Excel value is NaN, fill from dictionary
            merged[col] = merged[col + "_x"].fillna(merged[col + "_y"]) \
                if col + "_x" in merged.columns and col + "_y" in merged.columns \
                else merged[col]

    # Drop merge artifacts
    for col in list(merged.columns):
        if col.endswith("_x") or col.endswith("_y"):
            merged = merged.drop(columns=[col])

    logger.info(f"  Enriched from dictionary: {len(field_map)} fields matched on '{match_field}'")
    return merged


# ---------------------------------------------------------------------------
# Data reading and cleaning
# ---------------------------------------------------------------------------

def read_excel_sheet(file_path: Path, sheet_name: str) -> pd.DataFrame:
    """Read an Excel sheet into a DataFrame."""
    return pd.read_excel(file_path, sheet_name=sheet_name)


def clean_dataframe(df: pd.DataFrame, import_def: dict) -> pd.DataFrame:
    """Apply standard cleaning to DataFrame."""
    original_len = len(df)

    # Remove fully empty rows
    df = df.dropna(how="all").reset_index(drop=True)

    # Strip whitespace from string columns
    str_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in str_cols:
        df[col] = df[col].str.strip()

    # Remove rows where all required fields are empty
    required = import_def.get("required_fields", [])
    if required:
        # Map required db fields to Excel column names
        col_mapping = import_def.get("column_mapping", {})
        excel_required = [col_mapping.get(r, r) for r in required]
        excel_required = [e for e in excel_required if e in df.columns]
        if excel_required:
            df = df.dropna(subset=excel_required, how="all").reset_index(drop=True)

    removed = original_len - len(df)
    if removed > 0:
        logger.info(f"  Removed {removed} empty/invalid rows")

    return df


def rename_columns(df: pd.DataFrame, import_def: dict) -> pd.DataFrame:
    """Rename columns from Excel (Chinese) names to DB (English) names."""
    col_mapping = import_def.get("column_mapping", {})

    # Build reverse mapping: Excel col name -> DB field name
    # Only for columns that exist in the DataFrame
    rename_map = {}
    for db_field, excel_col in col_mapping.items():
        # excel_col may be a string (from YAML) or int (e.g., year columns)
        # df.columns may contain strings or ints. Convert both to string for
        # comparison, but also try exact match.
        if excel_col in df.columns:
            rename_map[excel_col] = db_field
        elif isinstance(excel_col, str):
            # Handle integer column names in df (e.g., 2016, 2017)
            try:
                excel_col_int = int(excel_col)
                if excel_col_int in df.columns:
                    rename_map[excel_col_int] = db_field
            except (ValueError, TypeError):
                pass
        elif isinstance(excel_col, int) and excel_col in df.columns:
            rename_map[excel_col] = db_field

    if rename_map:
        df = df.rename(columns=rename_map)
        logger.debug(f"  Renamed {len(rename_map)} columns")

    return df


def standardize_province(df: pd.DataFrame, province_map: dict) -> tuple:
    """Standardize province names. Returns (df, changes_list)."""
    changes = []
    if "province" not in df.columns:
        return df, changes

    original = df["province"].copy()
    df["province"] = df["province"].map(lambda x: province_map.get(str(x).strip(), str(x).strip()) if pd.notna(x) else x)

    changed = original != df["province"]
    for old, new in zip(original[changed], df["province"][changed]):
        changes.append(f"Province: '{old}' -> '{new}'")

    return df, changes


def standardize_region(df: pd.DataFrame, region_lookup: dict) -> list:
    """Fill missing region values based on province. Returns changes list."""
    changes = []
    if "region" not in df.columns or "province" not in df.columns:
        return changes

    for idx, row in df.iterrows():
        if pd.isna(row.get("region")) or str(row.get("region")).strip() == "":
            province = str(row["province"]).strip() if pd.notna(row.get("province")) else ""
            if province in region_lookup:
                df.at[idx, "region"] = region_lookup[province]
                changes.append(f"Row {idx}: Filled region='{region_lookup[province]}' from province='{province}'")

    # Also standardize existing region values
    valid_regions = {"东部", "中部", "西部", "东北"}
    if "region" in df.columns:
        for idx, row in df.iterrows():
            val = str(row["region"]).strip() if pd.notna(row.get("region")) else ""
            if val and val not in valid_regions:
                # Try to guess
                province = str(row.get("province", "")).strip() if pd.notna(row.get("province")) else ""
                if province in region_lookup:
                    old = df.at[idx, "region"]
                    df.at[idx, "region"] = region_lookup[province]
                    changes.append(f"Row {idx}: Corrected region '{old}' -> '{region_lookup[province]}'")

    return changes


def standardize_is_hub(df: pd.DataFrame, hub_set: set) -> list:
    """Fill is_hub boolean column based on province. Returns changes list."""
    changes = []
    if "is_hub" not in df.columns and "province" in df.columns:
        df["is_hub"] = df["province"].isin(hub_set)
        changes.append("Created is_hub column from province and hub_provinces config")
    elif "is_hub" in df.columns:
        # Normalize to boolean
        for idx, row in df.iterrows():
            val = row.get("is_hub")
            if pd.notna(val):
                if str(val).lower() in ("true", "yes", "1", "1.0"):
                    df.at[idx, "is_hub"] = True
                elif str(val).lower() in ("false", "no", "0", "0.0", ""):
                    df.at[idx, "is_hub"] = False
    return changes


# ---------------------------------------------------------------------------
# Type conversion
# ---------------------------------------------------------------------------

def convert_types(df: pd.DataFrame, import_def: dict):
    """Convert DataFrame columns to appropriate types."""
    numeric_fields = import_def.get("numeric_fields", [])
    integer_fields = import_def.get("integer_fields", [])

    for field in numeric_fields:
        if field in df.columns:
            df[field] = pd.to_numeric(df[field], errors="coerce")

    for field in integer_fields:
        if field in df.columns:
            df[field] = pd.to_numeric(df[field], errors="coerce")
            # Convert to nullable integer
            mask = df[field].notna()
            if mask.any():
                df.loc[mask, field] = df.loc[mask, field].astype("int64")

    return df


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_import(df: pd.DataFrame, import_def: dict, config: dict) -> dict:
    """Run all validation checks. Returns validation report dict."""
    report = {
        "table_name": import_def["table_name"],
        "file_path": import_def["file_path"],
        "sheet_name": import_def["sheet_name"],
        "rows_after_clean": len(df),
        "warnings": [],
        "errors": [],
    }

    # 1. Check required fields (missing column OR null value = error)
    required = import_def.get("required_fields", [])
    for field in required:
        if field not in df.columns:
            report["errors"].append(
                f"Required field '{field}' not found in data columns"
            )
        else:
            null_count = df[field].isna().sum()
            if null_count > 0:
                # List the actual rows that have nulls
                null_rows = df[df[field].isna()]
                if "indicator_name" in null_rows.columns:
                    identities = null_rows["indicator_name"].tolist()
                elif "province" in null_rows.columns:
                    identities = null_rows["province"].tolist()
                else:
                    identities = null_rows.index.tolist()
                report["errors"].append(
                    f"Required field '{field}' has {null_count} NULL value(s): "
                    f"{identities[:10]}{'...' if len(identities) > 10 else ''}"
                )

    # 2. Check unique keys
    unique_keys = import_def.get("unique_keys", [])
    if unique_keys:
        available_keys = [k for k in unique_keys if k in df.columns]
        if available_keys:
            dupes = df.duplicated(subset=available_keys, keep=False)
            if dupes.any():
                dupe_count = dupes.sum()
                dupe_rows = df[dupes][available_keys].head(10).to_dict("records")
                report["warnings"].append(
                    f"Found {dupe_count} duplicate rows on {available_keys}. "
                    f"First 10: {dupe_rows}"
                )

    # 3. Check year range
    if "year" in df.columns:
        year_range = config.get("year_range", {"min": 2016, "max": 2024})
        out_of_range = check_year_range(df["year"], year_range["min"], year_range["max"])
        if out_of_range:
            report["warnings"].append(
                f"Year values outside {year_range['min']}-{year_range['max']}: {out_of_range}"
            )

    # 4. Check probability fields
    prob_fields = ["probability", "max_posterior_probability"]
    for pf in prob_fields:
        if pf in df.columns:
            out_of_range = check_probability_range(df[pf])
            if out_of_range:
                report["warnings"].append(
                    f"Field '{pf}' has values outside [0,1]: {out_of_range}"
                )

    # 5. Check numeric fields are actually numeric
    numeric_fields = import_def.get("numeric_fields", [])
    for field in numeric_fields:
        if field in df.columns:
            non_numeric = check_numeric(df[field])
            if non_numeric > 0:
                report["warnings"].append(
                    f"Field '{field}' has {non_numeric} non-numeric values"
                )

    # 6. Check score-like fields > 0
    score_fields = ["composite_score", "score_2016", "score_2024"]
    for sf in score_fields:
        if sf in df.columns:
            vals = pd.to_numeric(df[sf], errors="coerce").dropna()
            neg_vals = (vals < 0).sum()
            if neg_vals > 0:
                report["warnings"].append(
                    f"Field '{sf}' has {neg_vals} negative values"
                )

    return report


# ---------------------------------------------------------------------------
# Database write
# ---------------------------------------------------------------------------

def table_exists(engine, table_name: str) -> bool:
    """Check if a table exists in the database."""
    inspector = sa_inspect(engine)
    return table_name in inspector.get_table_names()


def write_to_db(df: pd.DataFrame, import_def: dict, engine, mode: str = "append"):
    """Write DataFrame to PostgreSQL table.

    Supports two modes:
    - ``append``: skip rows whose unique_keys already exist in the DB.
    - ``upsert``: use INSERT … ON CONFLICT DO UPDATE for unique_keys.
    """
    table_name = import_def["table_name"]

    if not table_exists(engine, table_name):
        logger.warning(f"  ⚠️  Table '{table_name}' does not exist. Run schema.sql first.")
        return 0, f"Table '{table_name}' does not exist"

    inspector = sa_inspect(engine)
    db_columns = {col["name"] for col in inspector.get_columns(table_name)}

    available_cols = [c for c in df.columns if c in db_columns]
    skipped_cols = [c for c in df.columns if c not in db_columns and c != "id"]

    if skipped_cols:
        logger.debug(f"  Skipped columns (not in DB): {skipped_cols}")

    df_to_write = df[available_cols].copy()

    # Remove 'id' if present (auto-generated)
    if "id" in df_to_write.columns:
        df_to_write = df_to_write.drop(columns=["id"])

    if df_to_write.empty:
        return 0, "No matching columns found"

    unique_keys = import_def.get("unique_keys", [])

    # --- Upsert path ---
    if mode == "upsert" and unique_keys:
        # Build INSERT … ON CONFLICT … DO UPDATE
        columns = list(df_to_write.columns)
        col_quoted = ", ".join(f'"{c}"' for c in columns)
        conflict_cols = ", ".join(f'"{k}"' for k in unique_keys if k in columns)

        if not conflict_cols:
            return 0, "No unique_keys present in data columns for upsert"

        # Build VALUES placeholders: (:col0, :col1, …)
        placeholders = ", ".join(f":{c}" for c in columns)

        # Build SET clause: col = EXCLUDED.col for non-key columns
        update_cols = [c for c in columns if c not in unique_keys and c != "created_at"]
        set_clause = ", ".join(f'"{c}" = EXCLUDED."{c}"' for c in update_cols)

        sql = (
            f"INSERT INTO {table_name} ({col_quoted}) "
            f"VALUES ({placeholders}) "
            f"ON CONFLICT ({conflict_cols}) "
            f"DO UPDATE SET {set_clause}"
        )

        rows_written = 0
        try:
            with engine.connect() as conn:
                for _, row in df_to_write.iterrows():
                    params = {c: row[c] if pd.notna(row[c]) else None for c in columns}
                    conn.execute(text(sql), params)
                    rows_written += 1
                conn.execute(text("COMMIT"))
        except Exception as e:
            return 0, str(e)

        return rows_written, None

    # --- Append path (original) ---
    if mode == "append" and unique_keys:
        existing_keys = set()
        try:
            with engine.connect() as conn:
                key_cols = ", ".join(f'"{k}"' for k in unique_keys if k in db_columns)
                if key_cols:
                    result = conn.execute(text(f"SELECT {key_cols} FROM {table_name}"))
                    existing_keys = {tuple(row) for row in result.fetchall()}
        except Exception as e:
            logger.warning(f"  Could not read existing keys: {e}")

        if existing_keys:
            def is_new_row(row):
                key = tuple(row.get(k) for k in unique_keys if k in row.index)
                return key not in existing_keys

            mask = df_to_write.apply(is_new_row, axis=1)
            duplicates = (~mask).sum()
            if duplicates > 0:
                logger.info(f"  Skipping {duplicates} rows that already exist (unique key match)")
            df_to_write = df_to_write[mask]

    if df_to_write.empty:
        logger.info(f"  ℹ️  All {len(df)} rows already exist — nothing to import")
        return 0, None  # Not an error — just no new data

    # Standard insert
    try:
        df_to_write.to_sql(
            table_name,
            engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=100,
        )
        return len(df_to_write), None
    except Exception as e:
        return 0, str(e)


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_validation_report(
    all_reports: list,
    all_changes: dict,
    success_count: int,
    fail_count: int,
    total_rows_imported: int,
    output_path: Path,
):
    """Generate the final validation report."""
    lines = []
    lines.append("# Data Import Validation Report")
    lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Summary:** {success_count} succeeded, {fail_count} failed")
    lines.append(f"**Total rows imported:** {total_rows_imported}\n")
    lines.append("---\n")

    # Summary table
    lines.append("## Import Results\n")
    lines.append("| Table | File | Rows | Status |")
    lines.append("|-------|------|------|--------|")
    for r in all_reports:
        status = "❌ FAIL" if r.get("errors") else "✅ OK"
        if r.get("warnings"):
            status += f" ({len(r['warnings'])} warnings)"
        lines.append(
            f"| {r['table_name']} | {Path(r['file_path']).name} "
            f"| {r.get('rows_imported', r.get('rows_after_clean', 0))} | {status} |"
        )
    lines.append("")

    # Detailed issues
    lines.append("---\n")
    lines.append("## Warnings & Errors\n")
    for r in all_reports:
        if r.get("errors") or r.get("warnings"):
            lines.append(f"### {r['table_name']}\n")
            for err in r.get("errors", []):
                lines.append(f"- ❌ **Error:** {err}")
            for warn in r.get("warnings", []):
                lines.append(f"- ⚠️ **Warning:** {warn}")
            lines.append("")

    # Standardization changes
    if any(v for v in all_changes.values()):
        lines.append("---\n")
        lines.append("## Data Standardization Changes\n")
        for table, changes in all_changes.items():
            if changes:
                lines.append(f"### {table}\n")
                for c in changes[:20]:  # Limit to 20 per table
                    lines.append(f"- {c}")
                if len(changes) > 20:
                    lines.append(f"  ... and {len(changes) - 20} more changes")
                lines.append("")

    # Fields needing manual confirmation
    lines.append("---\n")
    lines.append("## Fields Needing Manual Confirmation\n")
    lines.append("The following items should be reviewed by a human:\n")
    lines.append("1. **Hub provinces** — Verify the hub_provinces list in the config")
    lines.append("   matches the actual national compute hub node designations.")
    lines.append("2. **Province names** — Check that all province name standardizations are correct.")
    lines.append("3. **Indicator codes** — The indicator_system table is now auto-populated from")
    lines.append("   data_dictionary.xlsx. Verify the 34 indicator codes are complete.")
    lines.append("4. **Region mapping** — Verify all 31 provinces are assigned to the correct region.")
    lines.append("5. **Markov state columns** — The 'Unnamed: 0' column in Markov sheets needs")
    lines.append("   verification that it maps correctly to 'from_state'.")
    lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return output_path


# ---------------------------------------------------------------------------
# Main import flow
# ---------------------------------------------------------------------------

def import_all(config: dict, engine, import_mode: str = "append"):
    """Run all imports defined in config."""
    imports = config.get("imports", [])
    all_reports = []
    all_changes = defaultdict(list)
    success_count = 0
    fail_count = 0
    total_rows = 0

    province_map = build_province_standardizer(config)
    region_lookup = build_region_lookup(config)
    hub_set = build_hub_set(config)
    project_root = get_project_root()

    for i, import_def in enumerate(imports, 1):
        table_name = import_def["table_name"]
        file_rel = import_def["file_path"]
        sheet_name = import_def["sheet_name"]
        file_path = project_root / file_rel

        # Determine import mode for this table:
        # Tables with a "dictionary" config default to upsert so re-runs are safe.
        table_mode = import_def.get("import_mode", import_mode)
        if import_def.get("dictionary") and table_mode == "append":
            table_mode = "upsert"

        logger.info(f"\n{'='*60}")
        logger.info(f"[{i}/{len(imports)}] Importing: {table_name} (mode={table_mode})")
        logger.info(f"  File: {file_rel}")
        logger.info(f"  Sheet: {sheet_name}")

        if not file_path.exists():
            logger.warning(f"  ⚠️  File not found: {file_path}. Skipping.")
            all_reports.append({
                "table_name": table_name,
                "file_path": file_rel,
                "sheet_name": sheet_name,
                "errors": [f"File not found: {file_path}"],
            })
            fail_count += 1
            continue

        try:
            # Read
            df = read_excel_sheet(file_path, sheet_name)
            logger.info(f"  Read {len(df)} rows × {len(df.columns)} columns")

            # Clean
            df = clean_dataframe(df, import_def)

            # Rename columns
            df = rename_columns(df, import_def)

            # Enrich from data dictionary (indicator_system + any future table)
            df = enrich_from_dictionary(df, import_def, project_root)

            # Standardize
            df, prov_changes = standardize_province(df, province_map)
            region_changes = standardize_region(df, region_lookup)
            hub_changes = standardize_is_hub(df, hub_set)

            all_changes[table_name].extend(prov_changes)
            all_changes[table_name].extend(region_changes)
            all_changes[table_name].extend(hub_changes)

            # Convert types
            df = convert_types(df, import_def)

            # Validate
            report = validate_import(df, import_def, config)

            if report["errors"]:
                logger.error(f"  ❌ Validation errors:")
                for err in report["errors"]:
                    logger.error(f"     {err}")
                all_reports.append(report)
                fail_count += 1
                continue

            # Write to DB
            rows_written, error = write_to_db(df, import_def, engine, table_mode)
            if error:
                report["errors"].append(error)
                logger.error(f"  ❌ Write error: {error}")
                fail_count += 1
            else:
                report["rows_imported"] = rows_written
                total_rows += rows_written
                success_count += 1
                logger.info(f"  ✅ Imported {rows_written} rows to {table_name}")

            if report.get("warnings"):
                for w in report["warnings"]:
                    logger.warning(f"  ⚠️  {w}")

            all_reports.append(report)

        except Exception as e:
            logger.error(f"  ❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            all_reports.append({
                "table_name": table_name,
                "file_path": file_rel,
                "sheet_name": sheet_name,
                "errors": [str(e)],
            })
            fail_count += 1

    return all_reports, dict(all_changes), success_count, fail_count, total_rows


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

logger = None  # Will be set in main()


def main():
    global logger
    logger = setup_logging()

    # Support --table=<name> to import a single table (for testing / re-runs)
    target_table = None
    args = sys.argv[1:]
    for arg in args:
        if arg.startswith("--table="):
            target_table = arg.split("=", 1)[1]
        elif arg == "--table" and len(args) > args.index(arg) + 1:
            target_table = args[args.index(arg) + 1]

    project_root = get_project_root()
    config_path = project_root / "backend" / "importers" / "data_import_config.yaml"
    output_path = project_root / "data" / "data_validation_report.md"

    print("=" * 60)
    print("  Green Compute System - Data Importer")
    print("=" * 60)

    # Load config
    if not config_path.exists():
        print(f"❌ Config not found: {config_path}")
        sys.exit(1)

    config = load_config(config_path)

    # Filter to single table if requested
    if target_table:
        all_imports = config.get("imports", [])
        filtered = [d for d in all_imports if d["table_name"] == target_table]
        if not filtered:
            print(f"❌ Table '{target_table}' not found in config. Available tables:")
            for d in all_imports:
                print(f"   - {d['table_name']}")
            sys.exit(1)
        config["imports"] = filtered
        logger.info(f"🔍 Filtered to single table: {target_table}")

    import_mode = config.get("import_mode", "append")

    # Connect to DB
    engine = get_engine()

    # Verify connection
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("✅ Database connection successful")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        logger.error("   Check your .env DATABASE_URL and ensure PostgreSQL is running.")
        sys.exit(1)

    # Run imports
    all_reports, all_changes, success, fail, total = import_all(config, engine, import_mode)

    # Generate report
    report_path = generate_validation_report(
        all_reports, all_changes, success, fail, total, output_path
    )

    # Final summary
    print(f"\n{'='*60}")
    print(f"  IMPORT COMPLETE")
    print(f"{'='*60}")
    print(f"  ✅ Succeeded: {success}")
    print(f"  ❌ Failed:    {fail}")
    print(f"  📊 Total rows: {total}")
    print(f"  📄 Report:    {report_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
