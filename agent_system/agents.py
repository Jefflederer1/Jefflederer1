from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .llm import LLMClient
from .models import AgentResult, RunContext, WorkItem


@dataclass
class Agent:
    name: str
    role: str
    system_prompt: str

    def run(self, work_item: WorkItem, context: RunContext, llm: LLMClient) -> AgentResult:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {
                "role": "user",
                "content": self._compose_prompt(work_item, context),
            },
        ]
        response = llm.complete(messages, role_hint=self.role)
        return AgentResult(
            agent_name=self.name,
            role=self.role,
            work_item_title=work_item.title,
            response=response,
        )

    def _compose_prompt(self, work_item: WorkItem, context: RunContext) -> str:
        memory_lines = "\n".join(
            f"- {k}: {v[:300]}" for k, v in context.memory.items()
        ) or "(none)"
        work_inputs = "\n".join(f"- {i}" for i in work_item.inputs) or "(none)"

        return (
            f"User objective:\n{context.user_task}\n\n"
            f"Work item title: {work_item.title}\n"
            f"Work item objective: {work_item.objective}\n"
            f"Inputs required:\n{work_inputs}\n\n"
            f"Prior outputs:\n{context.summarize_history()}\n\n"
            f"Shared memory:\n{memory_lines}\n\n"
            "Respond in concise markdown with:\n"
            "1. Key decisions\n"
            "2. Concrete output\n"
            "3. Risks\n"
            "4. Next handoff"
        )


def build_default_agents() -> List[Agent]:
    return [
        Agent(
            name="Ava",
            role="Product Strategist",
            system_prompt=(
                "You are a senior product strategist. Convert vague requests into"
                " clear scope, acceptance criteria, and delivery slices."
            ),
        ),
        Agent(
            name="Soren",
            role="Salesforce Architect",
            system_prompt=(
                "You are a Salesforce solution architect. Focus on security, OAuth connected apps,"
                " object model mapping, APIs, and integration risk."
            ),
        ),
        Agent(
            name="Mira",
            role="UI Reverse Engineer",
            system_prompt=(
                "You analyze UI behavior and map it to reproducible components,"
                " state flows, and interaction contracts."
            ),
        ),
        Agent(
            name="Kian",
            role="Implementation Engineer",
            system_prompt=(
                "You are a principal engineer. Turn plans into actionable, sprint-ready"
                " build steps with interfaces and milestones."
            ),
        ),
        Agent(
            name="Nora",
            role="QA & Guardrails",
            system_prompt=(
                "You ensure releases are safe. Provide tests, observability, compliance checks,"
                " and launch gates."
            ),
        ),
    ]
