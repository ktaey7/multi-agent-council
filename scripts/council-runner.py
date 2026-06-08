#!/usr/bin/env python3
"""Run or stage a Multi-Agent Council review.

Default mode is safe: write prompt files and a runbook, but do not call agents.
Use --execute to invoke available local CLIs in parallel.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


AGENT_ORDER = ("codex", "claude", "agy", "grok")

PERSPECTIVES = {
    "codex": "implementation correctness, test gaps, and Codex maintainer workflow fit",
    "claude": "facilitation quality, user adoption, installability, and decision record clarity",
    "agy": "conceptual differentiation, alternate approaches, and product/UX impact",
    "grok": "skeptical OSS maintainer review, failure scenarios, and counterfactual critique",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create prompts or execute a Multi-Agent Council review."
    )
    parser.add_argument("--question", help="Review question.")
    parser.add_argument(
        "--evidence",
        action="append",
        default=[],
        help="Evidence path, URL, issue, PR, or short note. Repeatable.",
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Repository/workspace root for agent commands. Defaults to cwd.",
    )
    parser.add_argument(
        "--agents",
        default="auto",
        help="Comma-separated agents: codex,claude,agy,grok or auto.",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output directory. Defaults to .council-runs/<timestamp>.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually invoke available local agent CLIs. Default only writes prompts.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="Per-agent timeout in seconds when --execute is used.",
    )
    parser.add_argument(
        "--allow-grok-without-sandbox",
        action="store_true",
        help=(
            "Let Grok run without --sandbox read-only if the local Grok sandbox "
            "is unavailable. Use only in trusted repos."
        ),
    )
    parser.add_argument(
        "--check-prereqs",
        action="store_true",
        help="Check optional local agent CLI availability and exit.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="With --check-prereqs, exit nonzero when any checked CLI is missing.",
    )
    return parser.parse_args()


def repo_root(path: str) -> Path:
    return Path(path).expanduser().resolve()


def output_dir(repo: Path, raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    return repo / ".council-runs" / stamp


def select_agents(raw: str) -> list[str]:
    if raw == "auto":
        return [agent for agent in AGENT_ORDER if shutil.which(agent)]
    selected = [part.strip() for part in raw.split(",") if part.strip()]
    unknown = [agent for agent in selected if agent not in AGENT_ORDER]
    if unknown:
        raise SystemExit(f"unknown agent(s): {', '.join(unknown)}")
    return selected


def check_prereqs(strict: bool) -> int:
    labels = {
        "codex": "Codex CLI",
        "claude": "Claude Code",
        "agy": "Gemini (agy)",
        "grok": "Grok CLI",
    }
    available = 0
    total = len(AGENT_ORDER)
    print("Multi-Agent Council prerequisite check\n")
    for agent in AGENT_ORDER:
        path = shutil.which(agent)
        label = labels[agent]
        if not path:
            print(f"missing {label:<18} install it or use manual copy/paste fallback")
            continue
        available += 1
        version = version_line(agent)
        if version:
            print(f"found   {label:<18} {version} (auth not checked)")
        else:
            print(f"found   {label:<18} installed (auth not checked)")
    print(
        f"""
Available: {available}/{total}

Notes:
- This script checks command availability, not provider authentication.
- A full four-agent council is optional.
- If a CLI is missing or not logged in, run the council with the remaining tools
  or copy prompts into web/app UIs.
"""
    )
    return 1 if strict and available != total else 0


def version_line(command: str) -> str:
    try:
        proc = subprocess.run(
            [command, "--version"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    lines = [line.strip() for line in (proc.stdout or "").splitlines() if line.strip()]
    for line in lines:
        if not line.lower().startswith("warning:"):
            return line
    return lines[0] if lines else ""


def evidence_lines(evidence: list[str]) -> str:
    if not evidence:
        return "- No evidence supplied. Ask the maintainer to add files, diffs, logs, or docs."
    return "\n".join(f"- {item}" for item in evidence)


def build_prompt(agent: str, question: str, evidence: list[str], repo: Path) -> str:
    perspective = PERSPECTIVES[agent]
    return f"""You are one reviewer in a Multi-Agent Council.

Read-only analysis only. Do not modify files. Do not run destructive commands.

Question:
{question}

Repository/workspace:
{repo}

Evidence sources:
{evidence_lines(evidence)}

Assigned perspective:
{perspective}

Council rules:
- Equal Standing: evaluate arguments by evidence, not by model name.
- Constructive Dissent: challenge assumptions with specific failure scenarios.
- Evidence Required: cite files, diffs, logs, tests, docs, or direct observations.
- Pass When Empty: use PASS only when there is no new evidence and no blocking objection.
- Preserve independence: answer from your own perspective before seeing other reviews.

Return:
1. Core judgment
2. Evidence with labels: empirical, mechanistic, strategic, ethical, or heuristic
3. Implementation impact
4. Risks and failure scenarios
5. Highest-leverage improvements
"""


def command_for(agent: str, repo: Path, prompt_path: Path, allow_grok_without_sandbox: bool) -> list[str]:
    if agent == "codex":
        return ["codex", "exec", "--sandbox", "read-only", "-C", str(repo), "-"]
    if agent == "claude":
        return [
            "claude",
            "--print",
            "--permission-mode",
            "dontAsk",
            "--allowedTools",
            "Read,Glob,Grep",
        ]
    if agent == "agy":
        return ["agy", "--sandbox", "--print", prompt_path.read_text(), "--print-timeout", "5m"]
    if agent == "grok":
        cmd = [
            "grok",
            "--cwd",
            str(repo),
            "--prompt-file",
            str(prompt_path),
            "--permission-mode",
            "dontAsk",
            "--disable-web-search",
            "--max-turns",
            "10",
            "--no-alt-screen",
        ]
        if not allow_grok_without_sandbox:
            cmd.extend(["--sandbox", "read-only"])
        return cmd
    raise ValueError(agent)


def run_agent(
    agent: str,
    repo: Path,
    prompt_path: Path,
    output_path: Path,
    timeout: int,
    allow_grok_without_sandbox: bool,
) -> dict[str, object]:
    cmd = command_for(agent, repo, prompt_path, allow_grok_without_sandbox)
    prompt_text = prompt_path.read_text()
    stdin = prompt_text if agent in {"codex", "claude"} else None
    start = dt.datetime.now(dt.timezone.utc)
    try:
        proc = subprocess.run(
            cmd,
            input=stdin,
            text=True,
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        combined = ""
        if proc.stdout:
            combined += proc.stdout
        if proc.stderr:
            if combined:
                combined += "\n\n--- stderr ---\n"
            combined += proc.stderr
        output_path.write_text(combined, encoding="utf-8")
        status = "ok" if proc.returncode == 0 and combined.strip() else "failed"
        return {
            "agent": agent,
            "status": status,
            "returncode": proc.returncode,
            "output": str(output_path),
            "started_at": start.isoformat(),
            "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "command": redact_command(cmd),
        }
    except OSError as exc:
        output_path.write_text(f"Failed to start {agent}: {exc}\n", encoding="utf-8")
        return {
            "agent": agent,
            "status": "failed",
            "returncode": None,
            "output": str(output_path),
            "started_at": start.isoformat(),
            "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "command": redact_command(cmd),
        }
    except subprocess.TimeoutExpired as exc:
        output_path.write_text(f"Timed out after {timeout}s\n{exc}", encoding="utf-8")
        return {
            "agent": agent,
            "status": "timeout",
            "returncode": None,
            "output": str(output_path),
            "started_at": start.isoformat(),
            "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "command": redact_command(cmd),
        }


def redact_command(cmd: list[str]) -> list[str]:
    # Prompts can be very long and may contain project details. Keep command shape only.
    if cmd[:3] == ["agy", "--sandbox", "--print"]:
        return ["agy", "--sandbox", "--print", "<prompt>", "--print-timeout", "5m"]
    return cmd


def write_runbook(out: Path, agents: list[str], execute: bool, repo: Path) -> None:
    lines = [
        "# Council Runbook",
        "",
        f"Repository: `{repo}`",
        f"Mode: `{'execute' if execute else 'prompt-only'}`",
        "",
        "## Agents",
        "",
    ]
    for agent in agents:
        lines.append(f"- `{agent}` prompt: `prompts/{agent}.md`")
        if execute:
            lines.append(f"  output: `outputs/{agent}.md`")
    lines.extend(
        [
            "",
            "## Next Steps",
            "",
            "1. Review independent outputs.",
            "2. Fill `comparison.md` by evidence quality, not majority vote.",
            "3. Run a counterfactual round if the answer converged too quickly.",
            "4. Write the maintainer-owned decision record.",
        ]
    )
    (out / "RUNBOOK.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_comparison_template(out: Path, agents: list[str]) -> None:
    rows = "\n".join(f"| {agent} |  |  |  |  |" for agent in agents)
    text = f"""# Council Comparison

| Reviewer | Core judgment | Strongest evidence | Main risk | Blocking objection |
| --- | --- | --- | --- | --- |
{rows}

## Agreement

- 

## Disagreement

- 

## Missing Evidence

- 

## Decision Options

- 
"""
    (out / "comparison.md").write_text(text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    if args.check_prereqs:
        return check_prereqs(args.strict)
    if not args.question:
        raise SystemExit("--question is required unless --check-prereqs is used")
    repo = repo_root(args.repo)
    out = output_dir(repo, args.out)
    prompts_dir = out / "prompts"
    outputs_dir = out / "outputs"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    agents = select_agents(args.agents)
    if not agents:
        print("No requested agents are installed. Wrote no prompts.", file=sys.stderr)
        return 2

    metadata: dict[str, object] = {
        "question": args.question,
        "evidence": args.evidence,
        "repo": str(repo),
        "out": str(out),
        "execute": args.execute,
        "agents": agents,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }

    prompt_paths: dict[str, Path] = {}
    for agent in agents:
        prompt = build_prompt(agent, args.question, args.evidence, repo)
        prompt_path = prompts_dir / f"{agent}.md"
        prompt_path.write_text(prompt, encoding="utf-8")
        prompt_paths[agent] = prompt_path

    write_runbook(out, agents, args.execute, repo)
    write_comparison_template(out, agents)

    results: list[dict[str, object]] = []
    if args.execute:
        with ThreadPoolExecutor(max_workers=len(agents)) as executor:
            futures = {
                executor.submit(
                    run_agent,
                    agent,
                    repo,
                    prompt_paths[agent],
                    outputs_dir / f"{agent}.md",
                    args.timeout,
                    args.allow_grok_without_sandbox,
                ): agent
                for agent in agents
            }
            for future in as_completed(futures):
                results.append(future.result())
        results.sort(key=lambda item: AGENT_ORDER.index(str(item["agent"])))
        metadata["results"] = results

    (out / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Council run staged: {out}")
    if args.execute:
        ok_count = sum(1 for result in results if result["status"] == "ok")
        print(f"Executed {ok_count}/{len(results)} agents successfully")
    else:
        print("Prompt-only mode. Add --execute to call local CLIs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
