# Multi-Agent Builder (Salesforce + UI Mimic)

This repo includes a **working multi-agent orchestration runtime** you can prompt with a task.

It creates a team of specialist agents that collaborate in sequence:

1. **Product Strategist** – clarifies scope and acceptance criteria.
2. **Salesforce Architect** – maps Salesforce objects, APIs, auth, and data contracts.
3. **UI Reverse Engineer** – breaks down on-screen behavior into component and interaction specs.
4. **Implementation Engineer** – produces build steps, service contracts, and delivery slices.
5. **QA & Guardrails** – generates test plan, security checks, and release gates.

The orchestrator saves a full run artifact under `runs/` so you can review output, reuse it, and hand it to implementation workflows.

## What do I do now? (first 5 minutes)

1. Run one task:

```bash
python3 run_agents.py --task "Clone my Salesforce opportunity board UX and data sync"
```

2. You will immediately see:
   - the path to the saved report, and
   - the full report printed in your terminal.

3. Re-open the most recent run at any time:

```bash
python3 run_agents.py --latest
```

4. Iterate with a tighter follow-up prompt:

```bash
python3 run_agents.py --task "Turn this into sprint tickets with estimates and dependencies"
```

## How to give agents instructions

Use one prompt per desired outcome. Best format:

- **Goal:** what to build
- **Source UX:** page/process to mimic
- **Data sources:** Salesforce objects/APIs required
- **Constraints:** stack, timeline, compliance
- **Definition of done:** acceptance criteria

Example prompt:

```text
Build a web app that mirrors our Salesforce Opportunity Kanban behavior.
Source UX: stage changes, owner assignment, inline amount edits, activity timeline.
Data sources: Opportunity, Account, Contact, Task via Salesforce APIs.
Constraints: React frontend, Python API backend, OAuth connected app, least privilege.
Definition of done: clickable Kanban UI + live read/write sync in sandbox.
```

## UX options in CLI

### One-shot mode

```bash
python3 run_agents.py --task "..."
```

### Interactive mode (continuous)

```bash
python3 run_agents.py --interactive
```

Inside interactive mode:
- Enter any task to run agent collaboration.
- Enter `latest` to view the newest saved report.
- Enter `exit` to quit.

### Quiet mode (save file, suppress terminal report)

```bash
python3 run_agents.py --task "..." --no-print
```

## LLM configuration

By default, the runtime works in local fallback mode, so you can run it without credentials.

To use a real model via an OpenAI-compatible API:

1. Copy `.env.example` to `.env` (or export variables in your shell)
2. Set:
   - `OPENAI_API_KEY`
   - `OPENAI_MODEL` (optional, default `gpt-4o-mini`)
   - `OPENAI_BASE_URL` (optional, default `https://api.openai.com`)

Example:

```bash
export OPENAI_API_KEY="..."
export OPENAI_MODEL="gpt-4o-mini"
```

## Output

Each run writes a Markdown report file like:

- `runs/20260227_120501_build-a-clone-of-my-opportunity-pipeline-page.md`

The report includes:
- Intake prompt
- Per-agent outputs
- Consolidated execution roadmap
- Suggested next command
