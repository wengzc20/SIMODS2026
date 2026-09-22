"""Student-facing DBLP download -> conversion -> diagnosis runner."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "code"
VERSION = "2026-07-01"
DTD_VERSION = "2023-06-28"


def run(arguments: list[str]) -> None:
    subprocess.run([sys.executable, *arguments], check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["plan", "download", "convert", "diagnose"])
    parser.add_argument("--data-dir", type=Path, default=ROOT / "external_data" / "dblp")
    parser.add_argument("--year-min", type=int, default=2023)
    parser.add_argument("--year-max", type=int, default=2025)
    parser.add_argument("--max-records", type=int)
    args = parser.parse_args()

    xml = args.data_dir / f"dblp-{VERSION}.xml.gz"
    dtd = args.data_dir / f"dblp-{DTD_VERSION}.dtd"
    edges = args.data_dir / "dblp_edges.csv"
    authors = args.data_dir / "dblp_authors.csv"
    metadata = args.data_dir / "dblp_metadata.json"
    result = args.data_dir / "dblp_q2.json"

    if args.stage == "plan":
        run([
            str(CODE / "download_dblp_snapshot.py"), "--version", VERSION,
            "--destination", str(args.data_dir), "--dry-run",
        ])
    elif args.stage == "download":
        run([
            str(CODE / "download_dblp_snapshot.py"), "--version", VERSION,
            "--destination", str(args.data_dir),
        ])
    elif args.stage == "convert":
        command = [
            str(CODE / "convert_dblp_xml.py"), "--xml", str(xml), "--dtd", str(dtd),
            "--edges-output", str(edges), "--authors-output", str(authors),
            "--metadata-output", str(metadata), "--year-min", str(args.year_min),
            "--year-max", str(args.year_max), "--record-types", "article,inproceedings",
            "--min-authors", "3",
        ]
        if args.max_records is not None:
            command.extend(["--max-records", str(args.max_records)])
        run(command)
    else:
        run([
            str(CODE / "generic_affiliation_diagnostic.py"), "--edges", str(edges),
            "--entity-column", "author_id", "--context-column", "publication_id",
            "--universe", str(authors), "--universe-id-column", "author_id",
            "--q", "2", "--output", str(result),
        ])


if __name__ == "__main__":
    main()

