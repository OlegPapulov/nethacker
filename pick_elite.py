"""Print the `repo@commit` of the top hub elite for one identity.

`nethackers elites --scope <identity>` returns every elite for that identity,
ranked, each with a `reference` block. Rank 1 is the parent the loop should
start from, because the project's own cold-start reads the *global top elite
per identity* rather than the overall board leader.

Kept as a file rather than a heredoc in the workflow: a heredoc inside a YAML
`run: |` block has to be indented to the block's level, and getting that wrong
produces a runtime failure that only shows up mid-job.
"""

from __future__ import annotations

import json
import sys


def main() -> None:
    identity = sys.argv[1]
    rows = json.load(open("elite.json"))
    matching = [r for r in rows if r.get("identity") == identity]
    if not matching:
        # A role or facet scope returns rows for several identities; fall back
        # to the best row for the requested identity, else the best available.
        print(
            f"no elite row for {identity}; "
            f"available: {sorted({r.get('identity') for r in rows})[:5]}",
            file=sys.stderr,
        )
        raise SystemExit(1)
    reference = matching[0].get("reference") or {}
    repo, commit = reference.get("repo"), reference.get("commit")
    if not repo or not commit:
        print(f"elite row for {identity} has no pinned commit: {reference}", file=sys.stderr)
        raise SystemExit(1)
    print(f"{repo}@{commit}")


if __name__ == "__main__":
    main()
