"""Write hub credentials where `nethackers login` would have put them.

The CLI stores a GitHub device-flow credential at
``~/.nethackers/credentials.json``, and ``hubclient.credentials.load()``
reads exactly four keys: ``login``, ``access_token`` and optionally
``refresh_token`` / ``expires_at``. The token is enough on its own -- the CLI
refreshes silently when an expiry is present, and a token without one is
simply treated as non-expiring.

Written as a file rather than a heredoc inside the workflow's ``run: |``
block, because a heredoc nested there has to be indented to the block's level
and a mistake only shows up as a mid-job runtime failure.
"""

from __future__ import annotations

import json
import os
import pathlib
import sys


def main() -> None:
    token = os.environ.get("NETHACKERS_TOKEN", "").strip()
    login = os.environ.get("NETHACKERS_LOGIN", "").strip()
    if not token or not login:
        print("no token/login; nothing written", file=sys.stderr)
        raise SystemExit(1)

    path = pathlib.Path.home() / ".nethackers" / "credentials.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    credentials = {"login": login, "access_token": token}
    path.write_text(json.dumps(credentials, indent=2))
    # The CLI writes 600; match it, since the file holds a bearer token.
    os.chmod(path, 0o600)
    print(f"wrote {path} for {login}")


if __name__ == "__main__":
    main()
