# Initial Postgres Schema

This directory contains the TKT-019 Postgres rewrite of the legacy staging SQLite DDL exported from `../solid-sheep/lib/staging-schema-sql.js`.

## Source Count

The current source export contains 251 `CREATE TABLE` statements and 371 indexes. The migration ticket text mentions 252 tables / 3,602 lines, but the checked-in source snapshot used for this port has 251 tables / 3,589 lines. `make verify-TKT-019` validates the concrete source snapshot count to avoid inventing an extra table.

## Translation Rules

- SQLite `PRAGMA defer_foreign_keys=TRUE` and `DELETE FROM sqlite_sequence` are omitted.
- `CREATE EXTENSION IF NOT EXISTS vector` is created up front for later pgvector-backed tables. The current source snapshot has no embedding columns, so no `vector(dim)` columns are emitted yet.
- `INTEGER PRIMARY KEY AUTOINCREMENT` is translated to `BIGSERIAL PRIMARY KEY`.
- `TEXT` remains `TEXT` unless the column is timestamp-shaped or JSON-shaped.
- Timestamp-shaped `TEXT` columns, including `*_at`, `*_until`, and columns with `DEFAULT (datetime('now'))`, are translated to `TIMESTAMPTZ`; `datetime('now')` becomes `CURRENT_TIMESTAMP`.
- JSON-shaped `TEXT` columns, including `*_json`, known JSON payload fields, and `TEXT DEFAULT '[]'` / `TEXT DEFAULT '{}'`, are translated to `JSONB` with JSON defaults cast via `::jsonb`.
- SQLite `REAL` is translated to Postgres `DOUBLE PRECISION`.
- Non-primary-key `INTEGER`, checks, unique constraints, foreign keys, and indexes are preserved unless syntax required a Postgres type/default rewrite.

The schema is intentionally raw SQL only. Django model declarations and `0001_initial` migrations are handled by TKT-020 and TKT-021.
