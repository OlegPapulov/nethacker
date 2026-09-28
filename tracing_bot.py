"""A tracing wrapper around any bot, for E2's death classification.

Why a wrapper rather than a patch
---------------------------------
The question E2 asks is *what was the bot doing when it died*, and that must be
answered **without changing what the bot does**. Patching `autoascend/agent.py`
risks altering behaviour, and then every measurement afterwards is confounded by
the instrumentation. This wrapper therefore sits outside: it holds the real bot,
observes every observation handed to it, and records what it returns -- the real
`act` is still the one that decides.

What it records per turn
------------------------
* whether any hostile monster glyph is orthogonally adjacent to the player
* whether the returned action is a movement or a non-movement (attack/spell/use)
* HP, max HP, depth and hunger from ``blstats``

At episode end it writes one JSON line to ``$NETHACK_TRACE_DIR/<seed>.json``
containing the whole tail, so the classifier can ask questions like "in the last
400 turns, how many were adjacent and how many attacked".

Only the tail is kept. A 30,000-turn episode at one record per turn would be
megabytes; the question is always about the end of the run, and the counters are
kept in full.

This is a *diagnostic* bot, not a submission: it writes files, so it is not
deterministic and must never be registered. The arena gives every episode its
own process and a private ``/tmp``, which is exactly the lifetime this needs.
"""

from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

# Same cache-root trick the packaged bot uses, set before the heavy imports.
_cache_root = Path(tempfile.gettempdir()) / "nethack_arena_submission_cache"
_cache_root.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("XDG_CACHE_HOME", str(_cache_root / "xdg"))
os.environ.setdefault("NUMBA_CACHE_DIR", str(_cache_root / "numba"))

from arena_adapter import AutoAscendDriver  # noqa: E402

# blstats indices, verified against the pinned image.
BL_HP, BL_MAXHP, BL_DEPTH, BL_HUNGER, BL_XP = 11, 10, 12, 13, 18

#: Turns of history to keep. Long enough to see a fight develop.
TAIL_TURNS = 400

#: Monster glyphs are 0..380; pets 381+; items 1906+; the map (cmap) 2359+.
_MONSTER_MAX = 381
_PLAYER = 340

#: Movement and harmless actions, as indices into nle.nethack.ACTIONS.
_MOVEMENT = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 16, 17, 18, 107})


def _adjacent_monsters(glyphs) -> int:
    """Hostile monster glyphs orthogonally adjacent to the player.

    Deliberately counts only the four orthogonal neighbours, not diagonals: a
    diagonal contact is a corner, and treating it as contact would call every
    corridor squeeze a fight.
    """
    if glyphs is None:
        return 0
    try:
        height, width = glyphs.shape
        ys, xs = _player_position(glyphs)
    except Exception:  # noqa: BLE001 - instrumentation must never break a run
        return 0
    if ys is None:
        return 0
    found = 0
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        y, x = ys + dy, xs + dx
        if 0 <= y < height and 0 <= x < width:
            g = int(glyphs[y][x])
            if 0 < g < _MONSTER_MAX and g != _PLAYER:
                found += 1
    return found


def _player_position(glyphs):
    """Locate the player glyph. Returns (row, col) or (None, None)."""
    try:
        import numpy as np

        where = np.argwhere(glyphs == _PLAYER)
        if where.size == 0:
            return None, None
        return int(where[0][0]), int(where[0][1])
    except Exception:  # noqa: BLE001
        return None, None


class TracingBot:
    """Wraps a real bot and records what happened, changing nothing."""

    def __init__(self, inner: Any) -> None:
        self._inner = inner
        self._tail: list[dict] = []
        self._total = 0
        self._adjacent_turns = 0
        self._attacking_turns = 0
        self._seed: int | None = None

    def reset(self, initial_observation: Mapping[str, Any]) -> None:
        self._tail = []
        self._total = 0
        self._adjacent_turns = 0
        self._attacking_turns = 0
        try:
            blstats = initial_observation["blstats"]
            self._seed = int(blstats[0])  # x, unused; seed comes from the runner
        except Exception:  # noqa: BLE001
            self._seed = None
        self._inner.reset(initial_observation)

    def act(self, observation: Mapping[str, Any]) -> int:
        adjacent = _adjacent_monsters(observation.get("glyphs"))
        try:
            blstats = observation["blstats"]
            hp = int(blstats[BL_HP])
            maxhp = int(blstats[BL_MAXHP])
            depth = int(blstats[BL_DEPTH])
            hunger = int(blstats[BL_HUNGER])
        except Exception:  # noqa: BLE001
            hp = maxhp = depth = hunger = -1

        action = self._inner.act(observation)

        self._total += 1
        if adjacent:
            self._adjacent_turns += 1
        if action not in _MOVEMENT:
            self._attacking_turns += 1

        self._tail.append(
            {
                "t": self._total,
                "adj": adjacent,
                "act": int(action),
                "hp": hp,
                "maxhp": maxhp,
                "depth": depth,
                "hunger": hunger,
            }
        )
        if len(self._tail) > TAIL_TURNS * 2:
            del self._tail[: TAIL_TURNS]
        return action

    def close(self) -> None:
        try:
            self._inner.close()
        except Exception:  # noqa: BLE001
            pass
        self._flush()

    def _flush(self) -> None:
        directory = os.environ.get("NETHACK_TRACE_DIR")
        if not directory:
            return
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            name = f"trace-{self._seed if self._seed is not None else 0:04d}.json"
            with open(Path(directory) / name, "w") as handle:
                json.dump(
                    {
                        "total_turns": self._total,
                        "adjacent_turns": self._adjacent_turns,
                        "attacking_turns": self._attacking_turns,
                        "tail": self._tail[-TAIL_TURNS:],
                    },
                    handle,
                )
        except Exception:  # noqa: BLE001 - tracing must never break a run
            pass


def make_agent() -> TracingBot:
    """A tracing wrapper around the packaged AutoAscend bot."""
    return TracingBot(_AutoAscendBot())


class _AutoAscendBot:
    """The packaged bot, unchanged."""

    def __init__(self) -> None:
        self._driver = AutoAscendDriver()

    def reset(self, initial_observation: Mapping[str, Any]) -> None:
        self._driver.reset(initial_observation)

    def act(self, observation: Mapping[str, Any]) -> int:
        return self._driver.act(observation)

    def close(self) -> None:
        self._driver.close()
