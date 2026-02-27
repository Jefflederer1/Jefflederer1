from pathlib import Path

from agent_system import AgentOrchestrator


def test_orchestrator_generates_report() -> None:
    out_dir = Path("runs/test_output")
    orchestrator = AgentOrchestrator(output_dir=str(out_dir))
    report = orchestrator.run("Create a Salesforce-backed dashboard clone")

    assert report.exists()
    text = report.read_text(encoding="utf-8")
    assert "# Multi-Agent Run Report" in text
    assert "## Agent Outputs" in text
