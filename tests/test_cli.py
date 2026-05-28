"""Tests for vrp/cli.py — CLI commands via Click's test runner."""

from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner
from vrp.cli import _load_year_issue_ids, cli
from vrp.discovery import load_seed_issue_ids
from vrp.parser import build_issue
from vrp.utils import save_json

from tests.fixtures import make_raw_metadata, make_raw_updates


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.fixture()
def data_dir(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    (d / "issues").mkdir()
    return d


def _patch_paths(data_dir: Path):
    issues_dir = data_dir / "issues"
    return [
        patch("vrp.config.DATA_DIR", data_dir),
        patch("vrp.config.ISSUES_DIR", issues_dir),
        patch("vrp.config.INDEX_FILE", data_dir / "index.json"),
        patch("vrp.config.STATS_FILE", data_dir / "stats.json"),
        patch("vrp.config.QUEUE_FILE", data_dir / "discovery_queue.json"),
        patch("vrp.cli.DATA_DIR", data_dir),
        patch("vrp.cli.ISSUES_DIR", issues_dir),
        patch("vrp.cli.INDEX_FILE", data_dir / "index.json"),
        patch("vrp.cli.QUEUE_FILE", data_dir / "discovery_queue.json"),
        patch("vrp.index_builder.ISSUES_DIR", issues_dir),
        patch("vrp.index_builder.INDEX_FILE", data_dir / "index.json"),
        patch("vrp.index_builder.STATS_FILE", data_dir / "stats.json"),
        patch("vrp.markdown_gen.ISSUES_DIR", issues_dir),
        patch("vrp.extractor.ISSUES_DIR", issues_dir),
        patch("vrp.extractor.QUEUE_FILE", data_dir / "discovery_queue.json"),
    ]


class TestCLIHelp:
    def test_help_exits_zero(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0

    def test_help_lists_commands(self, runner):
        result = runner.invoke(cli, ["--help"])
        for cmd in ["run", "serve", "status", "update"]:
            assert cmd in result.output

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "1.0.0" in result.output


class TestStatusCommand:
    def test_status_empty(self, runner, data_dir):
        patches = _patch_paths(data_dir)
        for p in patches:
            p.start()
        try:
            result = runner.invoke(cli, ["status"])
        finally:
            for p in patches:
                p.stop()

        assert result.exit_code == 0
        assert "0" in result.output  # all counts are zero

    def test_status_counts_reports(self, runner, data_dir):
        issues_dir = data_dir / "issues"
        for i in range(2):
            idir = issues_dir / f"10000000{i}"
            idir.mkdir()
            raw_u = make_raw_updates()
            raw_m = make_raw_metadata()
            issue = build_issue(f"10000000{i}", raw_u, raw_m)
            save_json(idir / "report.json", issue.model_dump())
            save_json(idir / "raw_updates.json", raw_u)

        patches = _patch_paths(data_dir)
        for p in patches:
            p.start()
        try:
            result = runner.invoke(cli, ["status"])
        finally:
            for p in patches:
                p.stop()

        assert result.exit_code == 0
        assert "2" in result.output

    def test_status_ignores_master_queue_as_year_checkpoint(self, runner, data_dir):
        save_json(data_dir / "discovery_2026.json", ["1", "2"])
        save_json(data_dir / "discovery_queue.json", ["1", "2", "3"])

        patches = _patch_paths(data_dir)
        for p in patches:
            p.start()
        try:
            result = runner.invoke(cli, ["status"])
        finally:
            for p in patches:
                p.stop()

        assert result.exit_code == 0
        assert "2026(2)" in result.output
        assert "queue(3)" not in result.output


class TestYearScopedRun:
    def test_load_year_issue_ids_dedupes_selected_checkpoints(self, data_dir):
        save_json(data_dir / "discovery_2025.json", ["2", "1"])
        save_json(data_dir / "discovery_2026.json", ["2", "3"])

        patches = _patch_paths(data_dir)
        for p in patches:
            p.start()
        try:
            ids = _load_year_issue_ids([2025, 2026])
        finally:
            for p in patches:
                p.stop()

        assert ids == ["1", "2", "3"]


class TestSeedLoading:
    def test_load_seed_issue_ids_from_json(self, tmp_path):
        seed_file = tmp_path / "seeds.json"
        seed_file.write_text('["123", "456", "abc"]')
        assert load_seed_issue_ids(seed_file) == ["123", "456"]
