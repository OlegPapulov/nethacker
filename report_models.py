"""Summarise an operator's model catalogue, flagging the keyless tier.

`nethackers models --operator <name>` runs the operator CLI inside a probe
container and returns the catalogue the sandbox will actually accept. Two
things matter for a free run:

* whether the catalogue parsed at all -- an empty list means the operator is
  unusable, and the docs are explicit that "a model whose catalog could not be
  read ... is an ordinary failure and takes three tries";
* which models need no credential. The `opencode/*` ids are the zen free tier,
  served by the image's bundled CLI, so they need no API key. Anything under a
  relay provider (e.g. `omniroute/*`) advertises a host-local proxy and will
  not resolve from inside a container.

Prints `OPERATOR_FAIL` on the first line when the catalogue is unusable, which
the workflow greps for.

Usage: report_models.py <models.json>
"""

from __future__ import annotations

import json
import sys


def main() -> None:
    try:
        models = json.load(open(sys.argv[1]))
    except Exception as exc:  # noqa: BLE001 - report, never raise
        print(f"OPERATOR_FAIL unreadable catalogue: {exc}")
        return
    if not isinstance(models, list) or not models:
        print("OPERATOR_FAIL empty catalogue")
        return

    ids = [m.get("id", "") for m in models if isinstance(m, dict)]
    keyless = sorted(i for i in ids if i.startswith("opencode/"))
    relay = sorted({i.split("/")[0] for i in ids if "/" in i and not i.startswith("opencode/")})

    print(f"MODELS {len(ids)}")
    print(f"KEYLESS_ZEN {len(keyless)}")
    for model_id in keyless:
        print(f"  zen {model_id}")
    if relay:
        print(f"RELAY_PROVIDERS {len(relay)} {', '.join(relay)}")
        print("  (these need a reachable upstream and are not expected in a sandbox)")
    if not keyless and not relay:
        print("OPERATOR_FAIL no usable model ids")


if __name__ == "__main__":
    main()
