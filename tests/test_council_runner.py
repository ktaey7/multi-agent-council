import importlib.util
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
RUNNER = ROOT / "scripts" / "council-runner.py"


def _load():
    spec = importlib.util.spec_from_file_location("council_runner", RUNNER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_prompts_from_dir_discovers_present_agents(tmp_path):
    mod = _load()
    (tmp_path / "codex.md").write_text("codex prompt", encoding="utf-8")
    (tmp_path / "claude.md").write_text("claude prompt", encoding="utf-8")
    found = mod.prompts_from_dir(tmp_path, None)
    assert list(found.keys()) == ["codex", "claude"]
    assert found["codex"].read_text() == "codex prompt"


def test_prompts_from_dir_missing_requested_agent_errors(tmp_path):
    mod = _load()
    (tmp_path / "codex.md").write_text("x", encoding="utf-8")
    with pytest.raises(SystemExit):
        mod.prompts_from_dir(tmp_path, ["codex", "claude"])


def test_prompts_from_dir_empty_errors(tmp_path):
    mod = _load()
    with pytest.raises(SystemExit):
        mod.prompts_from_dir(tmp_path, None)


def test_prompts_from_dir_missing_directory_errors(tmp_path):
    mod = _load()
    with pytest.raises(SystemExit):
        mod.prompts_from_dir(tmp_path / "nope", None)


def test_prompts_from_dir_preserves_requested_order(tmp_path):
    mod = _load()
    (tmp_path / "codex.md").write_text("c", encoding="utf-8")
    (tmp_path / "grok.md").write_text("g", encoding="utf-8")
    found = mod.prompts_from_dir(tmp_path, ["grok", "codex"])
    assert list(found.keys()) == ["grok", "codex"]


def test_prompts_dir_mode_stages_run(tmp_path):
    src = tmp_path / "round2"
    src.mkdir()
    (src / "codex.md").write_text("codex round2 prompt", encoding="utf-8")
    (src / "claude.md").write_text("claude round2 prompt", encoding="utf-8")
    out = tmp_path / "run"
    result = subprocess.run(
        [
            sys.executable, str(RUNNER),
            "--prompts-dir", str(src),
            "--agents", "codex,claude",
            "--out", str(out),
        ],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    import json
    meta = json.loads((out / "metadata.json").read_text())
    assert meta["agents"] == ["codex", "claude"]
    assert meta["prompts_dir"] == str(src.resolve())
