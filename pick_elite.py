"""Print the `repo@commit` of the top hub elite for one identity.

Kept as a file rather than a multi-line ``python -c "..."`` inside a workflow's
``run: |`` block: the double-quoted multi-line string terminates the YAML
scalar early and breaks the file, which has happened repeatedly in this project.

Usage: pick_elite.py elite.json <identity>
"""

from __future__ import annotations

import json
import sys


def main() -> None:
    rows = json.load(open(sys.argv[1]))
    identity = sys.argv[2]
    matching = [r for r in rows if r.get("identity") == identity]
    if not matching:
        available = sorted({r.get("identity") for r in rows if r.get("identity")})
        print(
            f"no elite row for {identity}; available: {available[:5]}",
            file=sys.stderr,
        )
        raise SystemExit(1)
    reference = matching[0].get("reference") or {}
    repo, commit = reference.get("repo"), reference.get("commit")
    if not repo or not commit:
        print(f"elite row has no pinned commit: {reference}", file=sys.stderr)
        raise SystemExit(1)
    print(f"{repo}@{commit}")


if __name__ == "__main__":
    main()
