from pathlib import Path

from run_agents import latest_report_path


def test_latest_report_path_returns_newest_markdown_file(tmp_path: Path) -> None:
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()

    older = runs_dir / "20260101_old.md"
    newer = runs_dir / "20260102_new.md"
    older.write_text("old", encoding="utf-8")
    newer.write_text("new", encoding="utf-8")

    assert latest_report_path(str(runs_dir)) == newer


def test_latest_report_path_returns_none_for_missing_directory(tmp_path: Path) -> None:
    assert latest_report_path(str(tmp_path / "does_not_exist")) is None
