#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from agent_system import AgentOrchestrator


def print_report(path: Path) -> None:
    print("\n" + "=" * 80)
    print(f"RUN REPORT: {path}")
    print("=" * 80)
    print(path.read_text(encoding="utf-8"))
    print("=" * 80 + "\n")


def latest_report_path(output_dir: str = "runs") -> Path | None:
    runs_path = Path(output_dir)
    if not runs_path.exists():
        return None
    reports = sorted(runs_path.glob("*.md"))
    if not reports:
        return None
    return reports[-1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a collaborative multi-agent planning session.")
    parser.add_argument("--task", type=str, help="Task to give the agent team.")
    parser.add_argument("--interactive", action="store_true", help="Prompt for tasks in a loop.")
    parser.add_argument(
        "--latest",
        action="store_true",
        help="Print the latest saved run report from runs/ without executing a new run.",
    )
    parser.add_argument(
        "--no-print",
        action="store_true",
        help="Do not print report body to terminal (still saves report file).",
    )
    args = parser.parse_args()

    if args.latest:
        path = latest_report_path()
        if path is None:
            print("No saved reports found in runs/ yet.")
            return
        print_report(path)
        return

    orchestrator = AgentOrchestrator()

    if args.interactive:
        print("Interactive mode ready. Type your task, 'latest' to view newest run, or 'exit'.")
        while True:
            task = input("\nEnter task for agent team: ").strip()
            if task.lower() in {"exit", "quit"}:
                break
            if task.lower() == "latest":
                path = latest_report_path()
                if path is None:
                    print("No saved reports found in runs/ yet.")
                    continue
                print_report(path)
                continue
            if not task:
                continue

            path = orchestrator.run(task)
            print(f"\nRun report saved to: {path}")
            if not args.no_print:
                print_report(path)
        return

    if not args.task:
        parser.error("Provide --task, --interactive, or --latest")

    path = orchestrator.run(args.task)
    print(f"Run report saved to: {path}")
    if not args.no_print:
        print_report(path)


if __name__ == "__main__":
    main()
