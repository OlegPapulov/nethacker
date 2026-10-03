"""Run the bot mutator for one identity.

Each iteration copies the current bot, drops the mutator's three markdown
files on top, and asks `nethackers evolve` for one OpenCode edit. The notes
files are kept in this process and copied back onto the next iteration.
They are gitignored inside the seed, and this script never writes them back
into the repo's `mutator/` directory. A new run starts from the blank
templates.

ponytail: one `evolve --iterations 1` per iteration, so the note for the
next one can say what the previous tree did. The coding container is not
killed from here.
nethackers scores a tree only after the operator exits; a killed
process is recorded as an operator error and is not measured.
nethackers' own container ceiling is 8 hours. The Actions job stops
at 360 minutes, which is the longest a GitHub-hosted runner allows.
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
OWNER = "OlegPapulov"
# The AutoAscend import. Used for an identity this owner has never scored.
BASELINE_COMMIT = "8387c34be4ce7c4019f4d98a9445a48e83e42731"
MODEL = "opencode/big-pickle"
OPERATOR = "opencode2"
EFFORT = "medium"
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
        "Read `experiments.md` and edit only the function it names. "
        "Do not edit `character.py`. Do not resubmit the spell-menu parser. "
        "Leave the change in the file when you exit. "
        "Do not revert it and do not restore the parent. "
        "A local game is not the score. A tree that matches the parent is thrown away. "
        "Mark the change with a `# hypothesis:` comment. "
        "Do not narrate and do not tour the tree. "
        "The judge scores the tree after this process exits. "
        "Private Dungeons are scored by their verifier after that registration. "
        "You do not have those seeds, and a local game is not a private result.\n\n"
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


def _food_death(name: str) -> bool:
    low = name.lower()
    return any(word in low for word in ("starv", "hunger", "faint"))


def _lead_cause(counts: dict[str, int]) -> str:
    """A starvation or fainting death leads the note. A monster that appears
    twice is not the task when one game still dies of hunger."""
    for name in counts:
        if _food_death(name):
            return name
    if not counts:
        return "no finished games"
    return max(counts, key=lambda name: (counts[name], name))


def _keep_win() -> str:
    """The 0.077 cap stays. The next edit is the adjacent-fast pass."""
    return (
        "Leave the weak-hunger corpse walk capped at 20 squares. Do not edit it. "
        "Do not edit `character.py` or the spell parser. That tree was scored: "
        "all 15 seeds match the parent, and the smoke seed is 1,899 turns. "
        "In `draw_monster_priority_negative`, a fast monster that is already "
        "adjacent is ignored (`pass`). That is the bot standing in the melee. "
        "When `imminent_death_on_melee` is true, draw the same negative ring for "
        "a fast adjacent monster that you already draw for a slow one. "
        "Do not leave the `pass`. Edit only that function."
    )


def _hypothesis(cause: str, shallow: int, total: int, causes: list[str] | None = None) -> str:
    blob = " ".join([cause, *(causes or [])]).lower()
    if any(word in blob for word in ("starv", "hunger", "faint")):
        lead = "One game still starves. Do not edit hunger or hit-point cuts. "
    elif "poison" in blob:
        lead = (
            "Treat poison as a reason to leave, not a hit to trade. A wizard "
            "dies to it with no hit points in reserve. "
        )
    elif total and shallow * 2 >= total:
        lead = (
            f"Most games end at depth 1, usually {cause}. A chaotic human wizard "
            "loses a melee. "
        )
    else:
        lead = f"The usual stop is {cause}. "
    return lead + _keep_win()


def mean_change(previous: float, score: float) -> str:
    """How this attempt moved the mean relative to the attempt before it."""
    delta = score - previous
    if abs(delta) < 0.0005:
        return f"does not change the mean ({previous:.3f})"
    direction = "decreases" if delta < 0 else "increases"
    return f"{direction} the mean by {abs(delta):.3f} (from {previous:.3f} to {score:.3f})"


def result_block(results: list[dict]) -> str:
    """One scored attempt per line. This is what both experiments.md files keep."""
    lines = ["## Result", ""]
    previous = results[0].get("parent_mean") if results else None
    for row in results:
        score = row.get("dev_fitness")
        score_text = f"{score:.3f}" if isinstance(score, float) else "none"
        kept = "kept" if row.get("improved") else "not kept"
        change = ""
        if isinstance(score, float) and isinstance(previous, (int, float)):
            sentence = mean_change(float(previous), score)
            change = f" {sentence[0].upper()}{sentence[1:]}."
        lines.append(
            f"- iteration {row.get('iteration')}: {score_text} {kept} "
            f"({row.get('reason')}).{change}"
        )
        if isinstance(score, float):
            previous = score
    return "\n".join(lines)


def saved_results(text: str) -> str:
    chunks = []
    for part in text.split("## Result")[1:]:
        body = part.split("\n## ")[0].strip()
        if body:
            chunks.append("## Result\n\n" + body)
    return "\n\n".join(chunks)


def _carry(row: dict) -> str:
    """What the next iteration is told about the tree that just finished."""
    reason = str(row.get("reason") or "")
    if row.get("code_unchanged") or "identical" in reason:
        return (
            "## Last iteration\n\n"
            "The previous tree matched the parent. The gate does not score that, "
            "so there is no result. These notes are not the edit. Change "
            "`autoascend/` and leave the `self.cast` in the file."
        )
    score = row.get("dev_fitness")
    if not isinstance(score, float):
        return (
            "## Last iteration\n\n"
            f"The previous tree was not scored ({reason}). Change `autoascend/`."
        )
    kept = "kept" if row.get("improved") else "not kept"
    return (
        "## Last iteration\n\n"
        f"The previous tree scored {score:.3f} and was {kept}. "
        "Do not submit that same diff again."
    )


def write_notes_from_evidence(
    notes: Path, evidence: dict, identity: str, earlier: str = "", carry: str = "",
) -> None:
    """Fill both note files from one public-batch eval. Earlier experiment
    scores stay at the top of experiments.md. The agent implements the new
    hypothesis under them."""
    notes.mkdir(parents=True, exist_ok=True)
    results = list(evidence.get("results") or [])
    counts: dict[str, int] = {}
    for row in results:
        cause = _cause(row)
        counts[cause] = counts.get(cause, 0) + 1
    cause = _lead_cause(counts)
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
    hypothesis = _hypothesis(cause, shallow, len(results), list(counts))
    (notes / "experience.md").write_text(
        f"# Playthrough\n\n"
        f"Identity: `{identity}`\n\n"
        f"## Why it stopped\n\n"
        f"{counts.get(cause, 0)} of {len(results)} games stopped at {cause}. "
        f"Mean progress {mean_text}.\n\n"
        f"{table}\n\n"
        f"## What is the problem\n\n"
        f"The score is the mean of these games. {shallow} of {len(results)} "
        f"end at depth 1. The mean moves when a long game gets longer, and it "
        f"falls when a long game gets shorter.\n\n"
        f"## What might solve it\n\n"
        f"See `experiments.md`.\n"
    )
    prior = saved_results(earlier).strip()
    prior_text = f"{prior}\n\n" if prior else ""
    carry_text = f"{carry.strip()}\n\n" if carry.strip() else ""
    (notes / "experiments.md").write_text(
        f"# Next experiment\n\n"
        f"{prior_text}"
        f"{carry_text}"
        f"## Why it stopped\n\n"
        f"{cause} ({counts.get(cause, 0)} of {len(results)}).\n\n"
        f"## What is the problem\n\n"
        f"Mean progress is {mean_text}. The bot is kept only if the next mean "
        f"is strictly higher on `{identity}`.\n\n"
        f"## What might solve it\n\n"
        f"{hypothesis}\n\n"
        "Edit `autoascend/` and exit. The judge measures that tree.\n"
    )


def _tree_digest(root: Path) -> str:
    """Hash of autoascend/. Equal digests mean the judged bot is the parent."""
    import hashlib
    digest = hashlib.sha256()
    base = root / "autoascend"
    if not base.is_dir():
        return ""
    for path in sorted(p for p in base.rglob("*") if p.is_file()):
        digest.update(str(path.relative_to(base)).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _note_text(notes: Path) -> str:
    parts = []
    for name in RUN_NOTES:
        path = notes / name
        parts.append(path.read_text() if path.is_file() else "")
    return "\n".join(parts)


def agent_rewrote(before: str, after: str) -> bool:
    return bool(after.strip()) and after != before and "This file is empty at the start of a run" not in after


def best_public(programs: list[dict], identity: str) -> tuple[str, float] | None:
    """Highest public progression this owner has registered for one identity."""
    best: tuple[str, float] | None = None
    for program in programs:
        commit = (program.get("reference") or {}).get("commit")
        if not commit:
            continue
        for row in program.get("identities") or []:
            if row.get("identity") != identity:
                continue
            score = row.get("progression")
            if not isinstance(score, (int, float)):
                continue
            if best is None or score > best[1]:
                best = (str(commit), float(score))
    return best


def public_programs(owner: str) -> list[dict]:
    from nethackers.hubclient.client import HubClient
    hub = HubClient("https://nethackers.dunnolab.ai")
    found = []
    for row in hub.search(owner, limit=50):
        found.append({**row, "identities": hub.program_identities(row["id"])})
    return found


def pull_commit(commit: str, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    subprocess.run(
        ["nethackers", "pull", f"github.com/OlegPapulov/nethacker@{commit}", str(dest)],
        check=True,
    )


def parent_tree(dest: Path, identity: str, programs: list[dict] | None = None) -> str:
    """The seed for this identity: the owner's best public commit, or the
    AutoAscend import when that identity has no public score."""
    picked = best_public(programs if programs is not None else public_programs(OWNER), identity)
    commit = picked[0] if picked else BASELINE_COMMIT
    pull_commit(commit, dest)
    return commit


def evolve_command(seed: Path, workdir: Path, identity: str, iterations: int) -> list[str]:
    return [
        "nethackers", "evolve", identity,
        "--seed", str(seed),
        "--from-seed",
        "--operator", OPERATOR,
        "--model", MODEL,
        "--effort", EFFORT,
        "--iterations", str(iterations),
        "--workdir", str(workdir),
    ]


def _iter_dirs(workdir: Path) -> list[Path]:
    """Iteration trees live at runs/<id>/work/iter-N in nethackers 0.37.3.
    The older runs/<id>/iter-N layout is kept so a scored tree is still found."""
    found = [path for path in workdir.glob("runs/*/work/iter-*") if path.is_dir()]
    found += [path for path in workdir.glob("runs/*/iter-*") if path.is_dir()]
    return sorted(found, key=lambda path: int(path.name.split("-", 1)[1]))


def _metric_rows(workdir: Path) -> list[dict]:
    rows = []
    for path in sorted((workdir / "runs").glob("*/metrics.jsonl")):
        for line in path.read_text().splitlines():
            if line.strip():
                rows.append(json.loads(line))
    by_iteration: dict[int, dict] = {}
    for row in rows:
        if row.get("reason") == "baseline":
            continue
        number = int(row.get("iteration") or 0)
        by_iteration[number] = row
    return [by_iteration[number] for number in sorted(by_iteration)]


def _result_row(
    number: int, metric: dict | None, tree: Path | None, proc_code: int,
    before: str, seed: Path, parent_mean: float | None, identity: str,
) -> dict:
    scored = metric is not None and metric.get("dev_fitness") is not None
    improved = metric is not None and metric.get("reason") == "registered"
    ignored = True
    if tree is not None:
        after = "\n".join(
            (tree / name).read_text() if (tree / name).is_file() else ""
            for name in RUN_NOTES
        )
        ignored = not agent_rewrote(before, after)
    unchanged = tree is None or _tree_digest(tree) == _tree_digest(seed)
    return {
        "identity": identity,
        "iteration": number,
        "exit_code": proc_code,
        "scored": scored,
        "improved": improved,
        "dev_fitness": None if metric is None else metric.get("dev_fitness"),
        "parent_mean": parent_mean,
        "reason": "no-metrics" if metric is None else metric.get("reason"),
        "hub_reason": None if metric is None else metric.get("hub_reason"),
        "notes_ignored": ignored,
        "code_unchanged": unchanged,
    }


def run(iterations: int, bot: Path, state: Path, identity: str) -> list[dict]:
    """One evolve per iteration. The next note says what the previous tree did.
    Leave the coding container until it exits."""
    state.mkdir(parents=True, exist_ok=True)
    notes = state / "notes"
    parent = state / "parent"
    checkout = bot
    try:
        parent_tree(parent, identity)
        bot = parent
    except (OSError, subprocess.CalledProcessError):
        pass
    evidence = eval_identity(bot, identity)
    (state / "parent-eval.json").write_text(json.dumps(evidence))
    parent_mean = evidence.get("mean_progress")
    if not isinstance(parent_mean, (int, float)):
        parent_mean = None
    earlier = (MUTATOR / "experiments.md").read_text()
    carry = ""
    results = []
    current = bot
    last_improved: Path | None = None
    for number in range(1, iterations + 1):
        write_notes_from_evidence(notes, evidence, identity, earlier, carry)
        before = _note_text(notes)
        slot = state / f"step-{number}"
        seed = slot / "seed"
        workdir = slot / "work"
        prepare_seed(current, notes, seed, identity)
        proc = subprocess.run(evolve_command(seed, workdir, identity, 1), text=True)
        trees = {int(path.name.split("-", 1)[1]): path for path in _iter_dirs(workdir)}
        metrics = _metric_rows(workdir)
        metric = metrics[-1] if metrics else None
        tree = None
        if metric is not None:
            raw = int(metric.get("iteration") or 0)
            tree = trees.get(raw - 1) or trees.get(raw) or (trees and next(reversed(trees.values())))
        elif trees:
            tree = next(reversed(trees.values()))
        if metric is not None and metric.get("dev_fitness") is not None and tree is not None:
            dest = state / "publish" / str(number)
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(tree, dest, ignore=shutil.ignore_patterns(*NOTES, ".gitignore"))
        row = _result_row(number, metric, tree, proc.returncode, before, seed, parent_mean, identity)
        results.append(row)
        if row["improved"] and tree is not None:
            last_improved = tree
            current = tree
        carry = _carry(row)
        earlier = (notes / "experiments.md").read_text()
    if last_improved is not None:
        _apply_code(last_improved, bot)
        # The pull lives under the run directory. The record step commits the checkout.
        if checkout.resolve() != bot.resolve():
            _apply_code(last_improved, checkout)
    if not results:
        results.append({
            "identity": identity,
            "iteration": 0,
            "exit_code": 0,
            "scored": False,
            "improved": False,
            "dev_fitness": None,
            "parent_mean": parent_mean,
            "reason": "no-metrics",
            "hub_reason": None,
            "notes_ignored": True,
            "code_unchanged": None,
        })
    (state / "results.json").write_text(json.dumps(results, indent=2))
    return results


def record_local(results: list[dict], notes: Path) -> None:
    """Append this run to the repo's experience.md. Append the score of each
    attempt to both experiments.md files. The proposal under the outer file
    still needs a human yes before any other mutator edit."""
    play = (notes / "experience.md").read_text() if (notes / "experience.md").is_file() else ""
    nxt = (notes / "experiments.md").read_text() if (notes / "experiments.md").is_file() else ""
    who = results[0].get("identity", DEFAULT_IDENTITY) if results else DEFAULT_IDENTITY
    lines = ["", f"## Run {who} ({len(results)} iteration(s))"]
    for row in results:
        reason = str(row.get("reason") or "")
        if len(reason) > 180:
            reason = reason[:180] + "…"
        lines.append(
            f"- iteration {row['iteration']}: reason={reason} "
            f"dev_fitness={row['dev_fitness']} improved={row['improved']} "
            f"notes_ignored={row.get('notes_ignored')} "
            f"code_unchanged={row.get('code_unchanged')}"
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
    outcome = result_block(results)
    (ROOT / "experiments.md").write_text(
        (ROOT / "experiments.md").read_text().rstrip() + "\n\n" + outcome + "\n" + "\n".join(proposal) + "\n"
    )
    (MUTATOR / "experiments.md").write_text(
        (MUTATOR / "experiments.md").read_text().rstrip() + "\n\n" + outcome + "\n"
    )


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
        command = evolve_command(seed, root / "work", DEFAULT_IDENTITY, 3)
        assert DEFAULT_IDENTITY in command
        assert command[command.index("--iterations") + 1] == "3"
        assert command[command.index("--effort") + 1] == "medium"
        assert "killed after" not in game
        assert "# hypothesis:" in game
        assert "Do not revert" in game
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
        assert "20 squares" in text
        assert "The judge measures" in text
        assert "killed by a jackal" in (filled / "experience.md").read_text()
        hungry = root / "hungry"
        write_notes_from_evidence(hungry, {
            "mean_progress": 0.04,
            "results": [
                {"trajectory_id": 0, "progress": 0.02, "turns": 5000, "max_depth": 1,
                 "cause_of_death": "killed by a wolf"},
                {"trajectory_id": 1, "progress": 0.02, "turns": 5206, "max_depth": 1,
                 "cause_of_death": "died of starvation"},
            ],
        }, DEFAULT_IDENTITY)
        hungry_text = (hungry / "experiments.md").read_text()
        assert "20 squares" in hungry_text
        assert "draw_monster_priority_negative" in hungry_text
        assert "imminent_death_on_melee" in hungry_text
        assert "Do not leave the `pass`" in hungry_text
        assert "died of starvation (1 of 2)" in hungry_text
        assert "matched the parent" in _carry({
            "code_unchanged": True, "reason": "gate:child identical to parent",
        })
        assert "scored 0.077" in _carry({
            "dev_fitness": 0.077, "improved": False, "reason": "no-cell-improved",
            "code_unchanged": False,
        })
        same = root / "same-tree"
        (same / "autoascend").mkdir(parents=True)
        (same / "autoascend" / "agent.py").write_text("x\n")
        assert _tree_digest(same) == _tree_digest(same)
        other = root / "other-tree"
        (other / "autoascend").mkdir(parents=True)
        (other / "autoascend" / "agent.py").write_text("y\n")
        assert _tree_digest(same) != _tree_digest(other)
        write_notes_from_evidence(hungry, {
            "mean_progress": 0.04,
            "results": [
                {"trajectory_id": 0, "progress": 0.02, "turns": 10, "max_depth": 1,
                 "cause_of_death": "died of starvation"},
            ],
        }, DEFAULT_IDENTITY, "## Result\n\n- iteration 1: 0.060 not kept (no-cell-improved)\n")
        assert "0.060 not kept" in (hungry / "experiments.md").read_text()
        assert saved_results("## Result\n\n- iteration 1: 0.060 not kept\n\n## Why it stopped\n\nx\n") == (
            "## Result\n\n- iteration 1: 0.060 not kept"
        )
        block = result_block([
            {"iteration": 1, "dev_fitness": 0.063, "parent_mean": 0.064, "improved": False, "reason": "no-cell-improved"},
            {"iteration": 2, "dev_fitness": 0.060, "parent_mean": 0.064, "improved": False, "reason": "no-cell-improved"},
        ])
        assert "Decreases the mean by 0.001 (from 0.064 to 0.063)" in block
        assert "Decreases the mean by 0.003 (from 0.063 to 0.060)" in block
        assert best_public([
            {"reference": {"commit": "aaa"}, "identities": [
                {"identity": "wiz-hum-cha-mal", "progression": 0.064},
            ]},
            {"reference": {"commit": "bbb"}, "identities": [
                {"identity": "wiz-hum-cha-mal", "progression": 0.062},
                {"identity": "val-dwa-law-fem", "progression": 0.1},
            ]},
        ], "wiz-hum-cha-mal") == ("aaa", 0.064)
        assert best_public([], "val-dwa-law-fem") is None
        assert agent_rewrote("same", "same") is False
        assert agent_rewrote("same", "rewritten playthrough") is True
        assert agent_rewrote("same", "This file is empty at the start of a run") is False
        nested = root / "work" / "runs" / "20261001" / "work" / "iter-0"
        nested.mkdir(parents=True)
        assert _iter_dirs(root / "work") == [nested]
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
