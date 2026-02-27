from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass
class WorkItem:
    title: str
    objective: str
    inputs: List[str] = field(default_factory=list)


@dataclass
class AgentResult:
    agent_name: str
    role: str
    work_item_title: str
    response: str
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class RunContext:
    user_task: str
    memory: Dict[str, str] = field(default_factory=dict)
    history: List[AgentResult] = field(default_factory=list)

    def summarize_history(self) -> str:
        if not self.history:
            return "No prior agent outputs."
        lines: List[str] = []
        for item in self.history:
            lines.append(f"- {item.agent_name} ({item.role}): {item.work_item_title}")
        return "\n".join(lines)
