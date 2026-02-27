from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List

from .agents import Agent, build_default_agents
from .llm import LLMClient
from .models import RunContext, WorkItem


class AgentOrchestrator:
    def __init__(self, agents: List[Agent] | None = None, output_dir: str = "runs") -> None:
        self.agents = agents or build_default_agents()
        self.llm = LLMClient()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self, user_task: str) -> Path:
        context = RunContext(user_task=user_task)

        work_items = [
            WorkItem(
                title="Scope + Acceptance Criteria",
                objective="Turn user intent into concrete outcomes and constraints.",
                inputs=["user objective", "delivery urgency", "must-have features"],
            ),
            WorkItem(
                title="Salesforce Integration Design",
                objective="Define auth, object mappings, API choices, and data sync strategy.",
                inputs=["scope document", "security constraints"],
            ),
            WorkItem(
                title="UI Behavior Parity Plan",
                objective="Map observed page behavior to target components and interactions.",
                inputs=["scope document", "source page observations"],
            ),
            WorkItem(
                title="Build Plan",
                objective="Create implementation sequence with modules, interfaces, and milestones.",
                inputs=["integration design", "UI parity plan"],
            ),
            WorkItem(
                title="Test + Release Guardrails",
                objective="Create quality gates, monitoring requirements, and rollout checklist.",
                inputs=["build plan", "security expectations"],
            ),
        ]

        for agent, work_item in zip(self.agents, work_items):
            result = agent.run(work_item, context, self.llm)
            context.history.append(result)
            context.memory[work_item.title] = result.response

        report_path = self._write_report(context)
        return report_path

    def _write_report(self, context: RunContext) -> Path:
        stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        slug = "-".join(context.user_task.lower().split()[:10])[:80].strip("-") or "run"
        path = self.output_dir / f"{stamp}_{slug}.md"

        lines = [
            "# Multi-Agent Run Report",
            "",
            "## User Task",
            context.user_task,
            "",
            f"LLM mode: {'API' if self.llm.enabled else 'Fallback (no API key)'}",
            "",
            "## Agent Outputs",
            "",
        ]

        for result in context.history:
            lines.extend(
                [
                    f"### {result.agent_name} — {result.role}",
                    f"**Work item:** {result.work_item_title}",
                    "",
                    result.response,
                    "",
                ]
            )

        lines.extend(
            [
                "## Consolidated Next Step",
                "Use the Build Plan + Test Guardrails sections to create your first implementation tickets.",
                "",
                "Suggested command:",
                "```bash",
                "python3 run_agents.py --task \"Refine this into sprint tickets with estimates\"",
                "```",
            ]
        )

        path.write_text("\n".join(lines), encoding="utf-8")
        return path
