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


def test_resolve_wanted_auto_returns_all(tmp_path):
    mod = _load()
    assert mod.resolve_wanted("auto") == list(mod.AGENT_ORDER)


def test_resolve_wanted_unknown_errors():
    mod = _load()
    with pytest.raises(SystemExit):
        mod.resolve_wanted("codex,bogus")


def test_partition_installed_splits_by_which():
    mod = _load()
    present = {"codex", "grok"}
    fake_which = lambda name: name if name in present else None
    installed, missing = mod.partition_installed(["codex", "claude", "agy", "grok"], which=fake_which)
    assert installed == ["codex", "grok"]
    assert missing == ["claude", "agy"]


def _fake_cmd_script(tmp_path, name, body):
    script = tmp_path / name
    script.write_text("#!/bin/sh\n" + body)
    script.chmod(0o755)
    return script


def test_run_agent_excludes_stderr_on_success(tmp_path, monkeypatch):
    mod = _load()
    script = _fake_cmd_script(tmp_path, "ok.sh", "echo REVIEW_OK\necho noise 1>&2\nexit 0\n")
    monkeypatch.setattr(mod, "command_for", lambda *a, **k: ["sh", str(script)])
    prompt = tmp_path / "p.md"; prompt.write_text("hi", encoding="utf-8")
    out = tmp_path / "o.md"
    res = mod.run_agent("claude", tmp_path, prompt, out, 30, False)
    assert res["status"] == "ok"
    text = out.read_text()
    assert "REVIEW_OK" in text
    assert "noise" not in text


def test_run_agent_includes_stderr_on_failure(tmp_path, monkeypatch):
    mod = _load()
    script = _fake_cmd_script(tmp_path, "fail.sh", "echo problem 1>&2\nexit 3\n")
    monkeypatch.setattr(mod, "command_for", lambda *a, **k: ["sh", str(script)])
    prompt = tmp_path / "p.md"; prompt.write_text("hi", encoding="utf-8")
    out = tmp_path / "o.md"
    res = mod.run_agent("claude", tmp_path, prompt, out, 30, False)
    assert res["status"] == "failed"
    assert "problem" in out.read_text()


def test_run_agent_timeout(tmp_path, monkeypatch):
    mod = _load()
    monkeypatch.setattr(mod, "command_for", lambda *a, **k: ["sleep", "5"])
    prompt = tmp_path / "p.md"; prompt.write_text("hi", encoding="utf-8")
    out = tmp_path / "o.md"
    res = mod.run_agent("claude", tmp_path, prompt, out, 1, False)
    assert res["status"] == "timeout"


def test_run_agent_oserror_on_missing_binary(tmp_path, monkeypatch):
    mod = _load()
    monkeypatch.setattr(mod, "command_for", lambda *a, **k: ["/nonexistent/binary_xyz123"])
    prompt = tmp_path / "p.md"; prompt.write_text("hi", encoding="utf-8")
    out = tmp_path / "o.md"
    res = mod.run_agent("claude", tmp_path, prompt, out, 5, False)
    assert res["status"] == "failed"
    assert "Failed to start" in out.read_text()
