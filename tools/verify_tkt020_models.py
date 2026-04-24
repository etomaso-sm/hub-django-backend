"""Verify TKT-020 inspectdb model split.

Checks the generated app model files against the TKT-019 schema and, when
provided, the raw inspectdb output captured from a live Postgres database.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA = REPO_ROOT / "migrations" / "initial" / "schema.sql"
APPS_DIR = REPO_ROOT / "apps"
EXPECTED_APPS = {
    "auth",
    "hub",
    "preferences",
    "tasks",
    "notifications",
    "agents",
    "brief",
    "crm",
    "finance",
    "reconciliation",
    "fundraise",
    "analytics",
    "lenses",
    "connectors",
    "jockey",
    "calls",
    "calendar",
    "learning",
    "audit",
    "vault",
    "spatial",
    "admin",
    "billing",
    "storefront",
    "stream",
    "governance",
    "onboarding",
    "import_",
    "pricing",
    "vectorize",
    "network",
    "qa",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inspectdb", type=Path)
    args = parser.parse_args()

    schema_tables = _schema_tables()
    model_tables = _model_tables()

    errors: list[str] = []
    if len(schema_tables) != 251:
        errors.append(f"expected 251 schema tables, found {len(schema_tables)}")
    if set(model_tables) != schema_tables:
        errors.append(
            "model db_table set does not match schema: "
            f"missing={sorted(schema_tables - set(model_tables))} "
            f"extra={sorted(set(model_tables) - schema_tables)}"
        )
    duplicates = sorted({table for table in model_tables if model_tables.count(table) > 1})
    if duplicates:
        errors.append(f"duplicate model db_table declarations: {duplicates}")

    missing_apps = sorted(EXPECTED_APPS - _model_apps())
    if missing_apps:
        errors.append(f"missing expected app model files: {missing_apps}")

    errors.extend(_tenant_manager_errors())

    if args.inspectdb:
        inspect_tables = set(_db_tables(args.inspectdb.read_text()))
        if inspect_tables != schema_tables:
            errors.append(
                "inspectdb table set does not match schema: "
                f"missing={sorted(schema_tables - inspect_tables)} "
                f"extra={sorted(inspect_tables - schema_tables)}"
            )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"TKT-020 models OK ({len(schema_tables)} tables across {len(EXPECTED_APPS)} apps)")
    return 0


def _schema_tables() -> set[str]:
    return set(re.findall(r"^CREATE TABLE ([A-Za-z_][A-Za-z0-9_]*)", SCHEMA.read_text(), re.M))


def _model_tables() -> list[str]:
    tables: list[str] = []
    for path in sorted(APPS_DIR.glob("*/models.py")):
        tables.extend(_db_tables(path.read_text()))
    return tables


def _model_apps() -> set[str]:
    return {path.parent.name for path in APPS_DIR.glob("*/models.py")}


def _db_tables(text: str) -> list[str]:
    return re.findall(r"db_table = [\"']([^\"']+)[\"']", text)


def _tenant_manager_errors() -> list[str]:
    errors: list[str] = []
    for path in sorted(APPS_DIR.glob("*/models.py")):
        text = path.read_text()
        if (
            "tenant_id = " in text
            and "from apps.common.managers import TenantScopedManager" not in text
        ):
            errors.append(f"{path.relative_to(REPO_ROOT)} uses tenant_id without manager import")
        for block in re.findall(
            r"^class\s+(\w+)\(models\.Model\):\n(?P<body>.*?)(?=^class\s+\w+\(models\.Model\):|\Z)",
            text,
            flags=re.M | re.S,
        ):
            class_name, body = block
            has_tenant = re.search(r"^\s+tenant_id\s+=", body, flags=re.M)
            has_manager = re.search(r"^\s+objects\s+=\s+TenantScopedManager\(\)", body, flags=re.M)
            if has_tenant and not has_manager:
                errors.append(
                    f"{path.relative_to(REPO_ROOT)}:{class_name} missing TenantScopedManager"
                )
    return errors


if __name__ == "__main__":
    raise SystemExit(main())
