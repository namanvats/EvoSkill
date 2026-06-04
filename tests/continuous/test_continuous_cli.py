"""CLI tests for `evoskill harvest` (dry-run) and `evoskill candidates`.

Full harvest (LLM distillation) is covered by test_harvest.py against a fake
distiller; here we exercise the click wiring, argument resolution, and the
no-LLM paths.
"""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from src.cli.commands.candidates import candidates_cmd
from src.cli.commands.harvest import harvest_cmd
from src.continuous.candidates import Candidate, CandidateStore

from .conftest import make_trial


def _project(tmp_path: Path, continuous_toml: str = "") -> Path:
    evoskill = tmp_path / ".evoskill"
    evoskill.mkdir()
    (evoskill / "config.toml").write_text('[harness]\nname = "claude"\n' + continuous_toml)
    return evoskill / "config.toml"


class TestHarvestCli:
    def test_dry_run_collects_and_clusters(self, tmp_path):
        cfg = _project(tmp_path)
        traces = tmp_path / "traces"
        # three failing trials with identical task text → one cluster
        for i in range(3):
            make_trial(traces, f"t{i}__X{i}", reward="0", task_name=f"bench/t{i}")
        result = CliRunner().invoke(harvest_cmd, [
            "--config", str(cfg), "--traces", str(traces),
            "--source", "harbor", "--dry-run", "--min-cluster-size", "1",
        ])
        assert result.exit_code == 0, result.output
        assert "Collected 3 episode(s)" in result.output
        assert "no candidates written" in result.output

    def test_no_usable_sources_errors(self, tmp_path):
        cfg = _project(tmp_path)
        # jsonl source but no jsonl_path configured → build_readers yields nothing
        result = CliRunner().invoke(harvest_cmd, ["--config", str(cfg), "--source", "jsonl"])
        assert result.exit_code == 1
        assert "no usable trace sources" in result.output


class TestCandidatesCli:
    def test_empty(self, tmp_path):
        cfg = _project(tmp_path)
        result = CliRunner().invoke(candidates_cmd, ["--config", str(cfg)])
        assert result.exit_code == 0
        assert "No candidates yet" in result.output

    def test_list_and_show(self, tmp_path):
        cfg = _project(tmp_path)
        from src.cli.config import load_config
        store = CandidateStore(load_config(config_path=cfg).continuous_candidates_dir)
        store.save(Candidate(
            candidate_id="my-skill-abc",
            skill_name="my-skill",
            skill_markdown="---\nname: my-skill\ndescription: d\n---\nthe body rule",
            target_pattern="recurring thing",
            episode_ids=["e1", "e2", "e3"],
            cluster_size=3,
        ))

        listing = CliRunner().invoke(candidates_cmd, ["--config", str(cfg)])
        assert listing.exit_code == 0
        assert "my-skill-abc" in listing.output
        assert "1 candidate(s)" in listing.output

        shown = CliRunner().invoke(candidates_cmd, ["--config", str(cfg), "--show", "my-skill-abc"])
        assert shown.exit_code == 0
        assert "the body rule" in shown.output
        assert "recurring thing" in shown.output  # full pattern, not truncated in --show

    def test_show_missing(self, tmp_path):
        cfg = _project(tmp_path)
        result = CliRunner().invoke(candidates_cmd, ["--config", str(cfg), "--show", "nope"])
        assert result.exit_code == 1
        assert "no candidate" in result.output

    def test_status_filter(self, tmp_path):
        cfg = _project(tmp_path)
        from src.cli.config import load_config
        store = CandidateStore(load_config(config_path=cfg).continuous_candidates_dir)
        store.save(Candidate(candidate_id="a", skill_name="a", skill_markdown="x", episode_ids=["e"]))
        store.save(Candidate(candidate_id="b", skill_name="b", skill_markdown="y",
                             episode_ids=["f"], status="graduated"))
        result = CliRunner().invoke(candidates_cmd, ["--config", str(cfg), "--status", "graduated"])
        assert result.exit_code == 0
        assert "b" in result.output
        # 'a' (pending) should be filtered out of the table rows
        assert "1 candidate(s)" in result.output
