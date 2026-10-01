"""Run the bot mutator for one identity.

Each iteration copies the current bot, drops the mutator's three markdown
files on top, and asks `nethackers evolve` for one OpenCode edit. The notes
files are kept in this process and copied back onto the next iteration.
They are gitignored inside the seed, and this script never writes them back
into the repo's `mutator/` directory. A new run starts from the blank
templates.

ponytail: one `evolve --iterations 1` per step. The notes survive a rejected
edit only because we copy them out ourselves; a crash between the edit and
that copy loses the iteration's notes. Upgrade path is a side directory the
operator writes to directly.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MUTATOR = Path(__file__).resolve().parent
DEFAULT_IDENTITY = "wiz-hum-cha-mal"
MODEL = "opencode/big-pickle"
OPERATOR = "opencode2"
RUN_NOTES = ("experience.md", "experiments.md")
NOTES = ("GAME_RULES.md", *RUN_NOTES)
BOT_NAMES = ("bot.py", "arena_adapter.py", "autoascend", "nethackers.solution.json", "LICENSE")


def ensure_notes(dest: Path) -> None:
    """Create experience.md and experiments.md when this run does not have them.

    A new run has neither file. That is the state before iteration 1.
    Later iterations already harvested whatever the agent wrote, so those
    files are left as they are.
    """
    dest.mkdir(parents=True, exist_ok=True)
    for name in RUN_NOTES:
        path = dest / name
        if not path.is_file():
            shutil.copyfile(MUTATOR / name, path)


def _game_rules(identity: str) -> str:
    body = (MUTATOR / "GAME_RULES.md").read_text()
    header = (
        f"# This gameplay\n\n"
        f"Identity: `{identity}`\n\n"
        "Play and score this identity only. "
        "`experience.md` and `experiments.md` are already filled from this bot's "
        "latest games. Implement the single change in `experiments.md`. "
        "When you stop, rewrite both files from what you observed. "
        "Leaving them unchanged discards the edit as a note-less change.\n\n"
    )
    return header + body


def prepare_seed(bot: Path, notes: Path, seed: Path, identity: str) -> None:
    """Bot code plus this run's notes. Notes are gitignored so a publish of
    the seed cannot carry them into the next run."""
    if seed.exists():
        shutil.rmtree(seed)
    seed.mkdir(parents=True)
    for name in BOT_NAMES:
        src = bot / name
        dst = seed / name
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copyfile(src, dst)
    (seed / "GAME_RULES.md").write_text(_game_rules(identity))
    for name in RUN_NOTES:
        src = notes / name
        if src.is_file():
            shutil.copyfile(src, seed / name)
    (seed / ".gitignore").write_text("".join(f"{name}\n" for name in NOTES))


def _latest_iter(workdir: Path) -> Path | None:
    runs = sorted((workdir / "runs").glob("*/iter-0"))
    return runs[-1] if runs else None


def _harvest(workdir: Path, notes: Path) -> None:
    tree = _latest_iter(workdir)
    if tree is None:
        return
    for name in ("experience.md", "experiments.md"):
        src = tree / name
        if src.is_file() and src.read_text().strip():
            shutil.copyfile(src, notes / name)


def _metrics(workdir: Path) -> dict:
    rows = []
    for path in sorted((workdir / "runs").glob("*/metrics.jsonl")):
        for line in path.read_text().splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows[-1] if rows else {}


def _apply_code(tree: Path, bot: Path) -> None:
    for name in BOT_NAMES:
        src = tree / name
        dst = bot / name
        if not src.exists():
            continue
        if dst.is_dir():
            shutil.rmtree(dst)
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copyfile(src, dst)


def _parse_evidence(stdout: str) -> dict:
    start = stdout.find("{")
    if start < 0:
        raise RuntimeError("eval printed no JSON")
    return json.loads(stdout[start:])


def eval_identity(bot: Path, identity: str) -> dict:
    proc = subprocess.run(
        ["nethackers", "eval", str(bot), "--objective", identity],
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "eval failed").strip()
        raise RuntimeError(detail[-2000:])
    return _parse_evidence(proc.stdout)


def _cause(row: dict) -> str:
    return row.get("cause_of_death") or row.get("milestone") or row.get("status") or "unknown"


def _hypothesis(cause: str, shallow: int, total: int) -> str:
    text = cause.lower()
    if any(word in text for word in ("starv", "hunger", "faint")):
        return (
            "Eat before exploring. Hunger is ending the game while the wizard "
            "is still on the early floors. Change food handling in autoascend "
            "so this character eats when hungry instead of walking on."
        )
    if "poison" in text:
        return (
            "Treat poison as a reason to leave, not a hit to trade. A wizard "
            "dies to it with no hit points in reserve. Change one combat or "
            "eating decision in autoascend so this character avoids a poisoned "
            "corpse or a poison attack it cannot survive."
        )
    if total and shallow * 2 >= total:
        return (
            f"Most games end at depth 1, usually {cause}. A chaotic human wizard "
            "loses a melee. Change one fight-or-run decision in autoascend so "
            "this character uses a corridor or a ranged attack instead of "
            "standing and trading hits."
        )
    return (
        f"The usual stop is {cause}. Change one strategy in autoascend so "
        "this character survives that more often. Do not branch on the seed."
    )


def write_notes_from_evidence(notes: Path, evidence: dict, identity: str) -> None:
    """Fill both note files from one public-batch eval. The agent implements
    the experiment; it does not have to invent the playthrough."""
    notes.mkdir(parents=True, exist_ok=True)
    results = list(evidence.get("results") or [])
    counts: dict[str, int] = {}
    for row in results:
        cause = _cause(row)
        counts[cause] = counts.get(cause, 0) + 1
    if counts:
        cause = max(counts, key=lambda name: (counts[name], name))
    else:
        cause = "no finished games"
    mean = evidence.get("mean_progress")
    mean_text = f"{mean:.3f}" if isinstance(mean, (int, float)) else "unknown"
    shallow = sum(1 for row in results if (row.get("max_depth") or 0) <= 1)
    lines = [
        f"| seed | progress | turns | stop |",
        f"| --- | --- | --- | --- |",
    ]
    for row in sorted(results, key=lambda item: item.get("trajectory_id", 0)):
        lines.append(
            f"| {row.get('trajectory_id', '')} | {row.get('progress', '')} | "
            f"{row.get('turns', '')} | {_cause(row)} |"
        )
    table = "\n".join(lines)
    hypothesis = _hypothesis(cause, shallow, len(results))
    (notes / "experience.md").write_text(
        f"# Playthrough\n\n"
        f"Identity: `{identity}`\n\n"
        f"## Why it stopped\n\n"
        f"{counts.get(cause, 0)} of {len(results)} games stopped at {cause}. "
        f"Mean progress {mean_text}.\n\n"
        f"{table}\n\n"
        f"## What is the problem\n\n"
        f"The score is the mean of these games. {shallow} of {len(results)} "
        f"end at depth 1. A change that does not move the usual stop, {cause}, "
        f"does not change the mean.\n\n"
        f"## What might solve it\n\n"
        f"See `experiments.md`.\n"
    )
    (notes / "experiments.md").write_text(
        f"# Next experiment\n\n"
        f"## Why it stopped\n\n"
        f"{cause} ({counts.get(cause, 0)} of {len(results)}).\n\n"
        f"## What is the problem\n\n"
        f"Mean progress is {mean_text}. The bot is kept only if the next mean "
        f"is strictly higher on `{identity}`.\n\n"
        f"## What might solve it\n\n"
        f"{hypothesis}\n"
    )


def _note_text(notes: Path) -> str:
    parts = []
    for name in RUN_NOTES:
        path = notes / name
        parts.append(path.read_text() if path.is_file() else "")
    return "\n".join(parts)


def agent_rewrote(before: str, after: str) -> bool:
    return bool(after.strip()) and after != before and "This file is empty at the start of a run" not in after


def evolve_command(seed: Path, workdir: Path, identity: str) -> list[str]:
    return [
        "nethackers", "evolve", identity,
        "--seed", str(seed),
        "--from-seed",
        "--operator", OPERATOR,
        "--model", MODEL,
        "--iterations", "1",
        "--workdir", str(workdir),
    ]


def evolve_once(seed: Path, workdir: Path, identity: str) -> subprocess.CompletedProcess[str]:
    workdir.mkdir(parents=True, exist_ok=True)
    return subprocess.run(evolve_command(seed, workdir, identity), text=True)


def run(iterations: int, bot: Path, state: Path, identity: str) -> list[dict]:
    """Mutate `bot` in place when an iteration improves it. Always leave the
    scored tree under `state/publish/<n>` so the caller can register it.
    Notes stay in `state/notes` and are not copied back to `mutator/`."""
    state.mkdir(parents=True, exist_ok=True)
    notes = state / "notes"
    results = []
    use_agent_notes = False
    for i in range(1, iterations + 1):
        if not use_agent_notes:
            evidence = eval_identity(bot, identity)
            (state / f"parent-eval-{i}.json").write_text(json.dumps(evidence))
            write_notes_from_evidence(notes, evidence, identity)
        before_files = {name: (notes / name).read_text() for name in RUN_NOTES}
        before = _note_text(notes)
        seed = state / f"seed-{i}"
        workdir = state / f"work-{i}"
        prepare_seed(bot, notes, seed, identity)
        proc = evolve_once(seed, workdir, identity)
        _harvest(workdir, notes)
        use_agent_notes = agent_rewrote(before, _note_text(notes))
        if not use_agent_notes:
            for name, text in before_files.items():
                (notes / name).write_text(text)
            (notes / "experience.md").write_text(
                before_files["experience.md"].rstrip()
                + "\n\nThe agent left these notes unchanged.\n"
            )
        metric = _metrics(workdir)
        tree = _latest_iter(workdir)
        scored = metric.get("dev_fitness") is not None
        improved = metric.get("reason") == "registered"
        if scored and tree is not None:
            dest = state / "publish" / str(i)
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(tree, dest, ignore=shutil.ignore_patterns(*NOTES, ".gitignore"))
        if improved and tree is not None:
            _apply_code(tree, bot)
        results.append({
            "identity": identity,
            "iteration": i,
            "exit_code": proc.returncode,
            "scored": scored,
            "improved": improved,
            "dev_fitness": metric.get("dev_fitness"),
            "reason": metric.get("reason"),
            "hub_reason": metric.get("hub_reason"),
            "notes_ignored": not use_agent_notes,
        })
        if proc.returncode != 0 and not scored:
            break
    (state / "results.json").write_text(json.dumps(results, indent=2))
    return results


def record_local(results: list[dict], notes: Path) -> None:
    """Append this run to the repo's experience.md and leave an unapproved
    proposal in experiments.md. Does not touch `mutator/`."""
    play = (notes / "experience.md").read_text() if (notes / "experience.md").is_file() else ""
    nxt = (notes / "experiments.md").read_text() if (notes / "experiments.md").is_file() else ""
    who = results[0].get("identity", DEFAULT_IDENTITY) if results else DEFAULT_IDENTITY
    lines = ["", f"## Run {who} ({len(results)} iteration(s))"]
    for row in results:
        lines.append(
            f"- iteration {row['iteration']}: reason={row['reason']} "
            f"dev_fitness={row['dev_fitness']} improved={row['improved']} "
            f"notes_ignored={row.get('notes_ignored')}"
        )
    lines += [
        "",
        "### Why it stopped",
        results[-1]["reason"] if results else "no iteration",
        "",
        "### What is the problem",
        play.strip() or "(the mutator wrote no playthrough notes)",
        "",
        "### What might solve it",
        "See the proposal in experiments.md. Do not edit mutator/ until a human approves it.",
        "",
    ]
    (ROOT / "experience.md").write_text((ROOT / "experience.md").read_text().rstrip() + "\n" + "\n".join(lines) + "\n")
    proposal = [
        "",
        "## Proposal (not approved)",
        "Source: the last mutator iteration. Applying this means editing `mutator/`, which needs a human yes.",
        "",
        nxt.strip(),
        "",
    ]
    (ROOT / "experiments.md").write_text((ROOT / "experiments.md").read_text().rstrip() + "\n" + "\n".join(proposal) + "\n")


def self_check() -> None:
    import tempfile
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        bot = root / "bot"
        bot.mkdir()
        (bot / "bot.py").write_text("def make_agent():\n    return None\n")
        (bot / "arena_adapter.py").write_text("# adapter\n")
        (bot / "nethackers.solution.json").write_text("{}\n")
        (bot / "LICENSE").write_text("mit\n")
        (bot / "autoascend").mkdir()
        (bot / "autoascend" / "agent.py").write_text("# agent\n")
        notes = root / "notes"
        assert not (notes / "experience.md").exists()
        ensure_notes(notes)
        assert (notes / "experience.md").read_text().startswith("# Playthrough")
        assert (notes / "experiments.md").is_file()
        (notes / "experience.md").write_text("# Playthrough\n\nkept\n")
        ensure_notes(notes)
        assert "kept" in (notes / "experience.md").read_text()
        seed = root / "seed"
        prepare_seed(bot, notes, seed, DEFAULT_IDENTITY)
        game = (seed / "GAME_RULES.md").read_text()
        assert f"Identity: `{DEFAULT_IDENTITY}`" in game
        assert "Elemental Planes" in game
        assert "Competition" not in game
        assert (seed / "experience.md").is_file()
        assert DEFAULT_IDENTITY in evolve_command(seed, root / "work", DEFAULT_IDENTITY)
        bare = root / "bare-notes"
        bare.mkdir()
        seed_bare = root / "seed-bare"
        prepare_seed(bot, bare, seed_bare, "val-dwa-law-fem")
        assert not (seed_bare / "experience.md").exists()
        assert not (seed_bare / "experiments.md").exists()
        assert "Identity: `val-dwa-law-fem`" in (seed_bare / "GAME_RULES.md").read_text()
        filled = root / "filled"
        write_notes_from_evidence(filled, {
            "mean_progress": 0.062,
            "results": [
                {"trajectory_id": 0, "progress": 0.037, "turns": 100, "max_depth": 1,
                 "cause_of_death": "killed by a jackal"},
                {"trajectory_id": 1, "progress": 0.179, "turns": 400, "max_depth": 7,
                 "cause_of_death": "killed by a jackal"},
            ],
        }, DEFAULT_IDENTITY)
        text = (filled / "experiments.md").read_text()
        assert "corridor" in text
        assert "killed by a jackal" in (filled / "experience.md").read_text()
        assert agent_rewrote("same", "same") is False
        assert agent_rewrote("same", "rewritten playthrough") is True
        assert agent_rewrote("same", "This file is empty at the start of a run") is False
    print("self-check ok")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--identity", default=DEFAULT_IDENTITY)
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--state", type=Path, default=None)
    args = parser.parse_args(argv)
    if args.self_check:
        self_check()
        return 0
    state = args.state or (ROOT / ".mutator-run")
    if state.exists():
        shutil.rmtree(state)
    results = run(args.iterations, ROOT, state, args.identity)
    record_local(results, state / "notes")
    print(json.dumps(results, indent=2))
    if not results or any(row.get("hub_reason") for row in results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
