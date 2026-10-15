"""Verify a downloaded Risk Terminal data release.

    python verify_release.py <release-dir> [--changelog path/to/METHODOLOGY_CHANGELOG.md]

Standard library only, on purpose: this file ships INSIDE every release, so a
reviewer who downloaded a zip and has nothing installed can still check that the
bytes they hold are the bytes we published.

What it checks:

  1. Every file listed in MANIFEST.json exists, with the published byte size and
     SHA-256 (streamed in 1 MiB chunks, never read whole).
  2. Every gzipped CSV has the published row count and the published header, in
     the published order. Rows are counted by streaming the CSV reader, so a
     newline inside a quoted field cannot inflate the count.
  3. No third-party editorial column appears in any header. This is a licence
     boundary, not a schema preference. Every table is checked: a column named
     headline / title / summary / body / text / content fails unless it is on
     the first-party allowlist below, and the events table additionally may not
     carry any of its known third-party columns.
  4. No string column looks like syndicated headlines: if more than 0.5% of a
     column's non-empty values end in a " - Outlet" / " | Outlet" suffix, the
     column fails; and no JSON value may carry a headline / title / summary-
     style key at any depth.
  5. Every model version and fingerprint in MANIFEST.fingerprints appears in the
     methodology changelog, when a copy of it is available. A release ships
     standalone, so a missing changelog is a warning and a skipped check; a
     fingerprint the changelog does not document is a failure.

Exit code 0 on a clean pass, 1 on any mismatch.
"""

import argparse
import csv
import gzip
import hashlib
import json
import re
import sys
from pathlib import Path

# Column names that, anywhere in a release, usually mean someone else's prose.
EDITORIAL_COLUMN_NAMES = frozenset({"headline", "title", "summary", "body", "text", "content"})

# (file key, column) pairs that carry such a name and are first-party:
# `backtest_events.title` names an event in a corpus we wrote; `leaders.title`
# is an office title ("President"); the explainer `summary` is our own model
# reading our own structured data, labelled AI-derived in the dictionary;
# `legislation.title` is the official title of a bill from open legislative
# data and `legislation.summary` is our own short factual line about it.
# These reviewed columns are also exempt from the outlet-suffix heuristic: our
# corpus titles use " — Operation …" subtitles that look like a suffix.
FIRST_PARTY_EDITORIAL_COLUMNS = frozenset(
    {
        ("backtest_events", "title"),
        ("leaders", "title"),
        ("score_explainers", "summary"),
        ("score_explainer_history", "summary"),
        ("legislation", "title"),
        ("legislation", "summary"),
    }
)

# The events table also has third-party columns under other names.
FORBIDDEN_TABLES = frozenset({"events"})

# Kept in sync with app.core.data_exports.EVENT_FORBIDDEN_COLUMNS by
# app/tests/test_release_build.py, which asserts the two sets are identical.
# Duplicated rather than imported because this file must run inside a
# downloaded release directory, where `app` does not exist.
FORBIDDEN_COLUMNS = frozenset(
    {
        "title",
        "summary",
        "cluster_summary",
        "ai_why_it_matters",
        "ai_market_exposure",
        "ai_watch_next",
        "subject_reason",
        "source_name",
        "external_id",
    }
)

try:  # prefer the registry when running inside the repo
    from app.core.data_exports import EVENT_FORBIDDEN_COLUMNS as _REGISTRY_FORBIDDEN

    FORBIDDEN_COLUMNS = frozenset(_REGISTRY_FORBIDDEN)
except Exception:
    pass

HASH_CHUNK = 1 << 20
CSV_FIELD_LIMIT = 10 * 1024 * 1024

# Kept identical to app.core.data_exports.OUTLET_SUFFIX_PATTERN by
# app/tests/test_release_build.py (duplicated: this file runs standalone).
OUTLET_SUFFIX_PATTERN = (
    r"\s[-\u2013\u2014|]\s"
    r"(?:[A-Z0-9][\w&'\u2019.]*|[a-z0-9-]+\.[a-z]{2,6})"
    r"(?:\s(?:[A-Z0-9&][\w&'\u2019.-]*|of|the|de|and|for|el|la|al|du|des|news|online|daily|times))"
    r"{0,5}\.?\s*$"
)
OUTLET_SUFFIX_RE = re.compile(OUTLET_SUFFIX_PATTERN)
OUTLET_SUFFIX_MAX_SHARE = 0.005


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            chunk = fh.read(HASH_CHUNK)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def read_csv_gz(
    path: Path, string_columns: frozenset[str] = frozenset()
) -> tuple[list[str], int, dict[str, tuple[int, int, int]]]:
    """Stream a gzipped CSV. Never loads it all.

    Returns (header, data row count, {column: (non-empty values, values ending
    in an outlet suffix, JSON values carrying an editorial key)}) for the named
    string columns.
    """
    csv.field_size_limit(CSV_FIELD_LIMIT)
    with gzip.open(path, "rt", newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        try:
            header = next(reader)
        except StopIteration:
            return [], 0, {}
        watch = [(i, c) for i, c in enumerate(header) if c in string_columns]
        seen = {c: 0 for _, c in watch}
        hits = {c: 0 for _, c in watch}
        nested = {c: 0 for _, c in watch}
        rows = 0
        for row in reader:
            rows += 1
            for i, col in watch:
                value = row[i] if i < len(row) else ""
                if value:
                    seen[col] += 1
                    if OUTLET_SUFFIX_RE.search(value):
                        hits[col] += 1
                    if value[0] in "[{" and _json_has_editorial_key(value):
                        nested[col] += 1
    return header, rows, {c: (seen[c], hits[c], nested[c]) for c in seen}


def _json_has_editorial_key(value: str) -> bool:
    """True when a JSON value carries a headline-like key at any depth (e.g. a
    contributor's `title` inside a score's `components`)."""
    try:
        stack = [json.loads(value)]
    except ValueError:
        return False
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            if any(str(k).lower() in EDITORIAL_COLUMN_NAMES for k in item):
                return True
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
    return False


def editorial_columns(key: str, table: str, columns: list[str]) -> list[str]:
    """Columns in this file that look like third-party prose and are not allow-listed."""
    leaked = {
        c for c in columns
        if c.lower() in EDITORIAL_COLUMN_NAMES and (key, c) not in FIRST_PARTY_EDITORIAL_COLUMNS
    }
    if table in FORBIDDEN_TABLES:
        leaked |= set(columns) & FORBIDDEN_COLUMNS
    return sorted(leaked)


def find_changelog(release_dir: Path, explicit: str | None) -> Path | None:
    if explicit:
        path = Path(explicit).expanduser()
        return path if path.is_file() else None
    candidates = [
        release_dir / "METHODOLOGY_CHANGELOG.md",
        release_dir.parent / "METHODOLOGY_CHANGELOG.md",
        release_dir.parent.parent / "audits" / "METHODOLOGY_CHANGELOG.md",
        Path(__file__).resolve().parent.parent.parent / "audits" / "METHODOLOGY_CHANGELOG.md",
    ]
    return next((c for c in candidates if c.is_file()), None)


def verify(release_dir: Path, changelog_arg: str | None) -> int:
    manifest_path = release_dir / "MANIFEST.json"
    if not manifest_path.is_file():
        print(f"FAIL  no MANIFEST.json in {release_dir}")
        return 1
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    results: list[tuple[str, str, str]] = []  # (status, subject, detail)
    failures = 0

    for entry in manifest.get("files", []):
        name = entry["path"]
        path = release_dir / name
        if not path.is_file():
            results.append(("FAIL", name, "missing from the release directory"))
            failures += 1
            continue

        problems: list[str] = []
        size = path.stat().st_size
        if size != entry["bytes"]:
            problems.append(f"size {size} != manifest {entry['bytes']}")
        digest = sha256_file(path)
        if digest != entry["sha256"]:
            problems.append(f"sha256 {digest[:16]}… != manifest {entry['sha256'][:16]}…")

        if name.endswith(".csv.gz"):
            strings = frozenset(
                c for c, t in (entry.get("dtypes") or {}).items()
                if t == "string" and (entry.get("key"), c) not in FIRST_PARTY_EDITORIAL_COLUMNS
            )
            try:
                header, rows, suffix_stats = read_csv_gz(path, strings)
            except (OSError, EOFError, gzip.BadGzipFile, UnicodeDecodeError) as exc:
                problems.append(f"unreadable: {type(exc).__name__}")
                header, rows, suffix_stats = [], -1, {}
            if header and header != entry["columns"]:
                problems.append(f"header {header} != manifest {entry['columns']}")
            if rows >= 0 and rows != entry["rows"]:
                problems.append(f"rows {rows} != manifest {entry['rows']}")
            for col, (seen, hits, nested) in sorted(suffix_stats.items()):
                if seen and hits / seen > OUTLET_SUFFIX_MAX_SHARE:
                    problems.append(
                        f"{col}: {hits:,} of {seen:,} values ({hits / seen:.2%}) end in an "
                        "outlet suffix; these read as syndicated headlines"
                    )
                if nested:
                    problems.append(
                        f"{col}: {nested:,} JSON values carry a headline/title/summary-style key"
                    )

        leaked = editorial_columns(entry.get("key", ""), entry.get("table", ""), entry["columns"])
        if leaked:
            problems.append(f"third-party editorial columns present: {leaked}")

        if problems:
            results.append(("FAIL", name, "; ".join(problems)))
            failures += 1
        else:
            results.append(("PASS", name, f"{entry['rows']:,} rows, {size:,} bytes"))

    for doc in ("README.md", "DATA_DICTIONARY.md", "LICENSE", "CHANGELOG.md"):
        exists = (release_dir / doc).is_file()
        results.append(("PASS" if exists else "FAIL", doc, "present" if exists else "missing"))
        failures += 0 if exists else 1

    fingerprints = manifest.get("fingerprints", {})
    wanted = sorted({v for values in fingerprints.values() for v in values})
    changelog = find_changelog(release_dir, changelog_arg)
    if not wanted:
        results.append(("PASS", "fingerprints", "no versioned score rows in this cut"))
    elif changelog is None:
        results.append(("WARN", "fingerprints", "no methodology changelog available — check skipped"))
    else:
        text = changelog.read_text(encoding="utf-8", errors="replace")
        missing = [v for v in wanted if v not in text]
        if missing:
            results.append(
                (
                    "FAIL",
                    "fingerprints",
                    f"not documented in {changelog.name}: {', '.join(missing)} — a release "
                    "may not ship a version or fingerprint the methodology changelog "
                    "does not describe",
                )
            )
            failures += 1
        else:
            results.append(("PASS", "fingerprints", f"{len(wanted)} documented in {changelog.name}"))

    width = max(len(r[1]) for r in results) if results else 10
    print(f"{'STATUS':<6}  {'SUBJECT':<{width}}  DETAIL")
    for status, subject, detail in results:
        print(f"{status:<6}  {subject:<{width}}  {detail}")

    release = manifest.get("release", release_dir.name)
    if failures:
        print(f"\nFAIL  {release}: {failures} problem(s)")
        return 1
    print(f"\nPASS  {release}: {len(manifest.get('files', []))} files verified")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="verify_release", description="Verify a Risk Terminal data release."
    )
    parser.add_argument("release_dir", help="the release directory (contains MANIFEST.json)")
    parser.add_argument("--changelog", default=None, help="path to METHODOLOGY_CHANGELOG.md")
    args = parser.parse_args(argv)
    return verify(Path(args.release_dir).expanduser().resolve(), args.changelog)


if __name__ == "__main__":
    raise SystemExit(main())
