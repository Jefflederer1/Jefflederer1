# Multi-Agent Blueprint for Salesforce + UI-Mirroring Development

This document outlines a practical and safe way to run multiple agents that can:
1. work on top of your Salesforce data model and integrations,
2. understand what is visible in your application UI,
3. continuously help prototype and ship a "vibe-coded" clone with similar features.

## What I can help you with immediately

- Define an agent architecture (planner, builder, tester, deployer, monitor).
- Set up Salesforce-safe access patterns (OAuth scopes, sandbox-first, audit trails).
- Build a page-observation loop (DOM + screenshots + interaction traces) to infer feature behavior.
- Translate observed behavior into reproducible tickets, schema specs, and implementation tasks.
- Set up 24/7 automation with CI/CD, queues, retries, health checks, and alerting.

## Recommended architecture (fast + safe)

### 1) Orchestrator agent
- Owns backlog and priorities.
- Breaks goals into bounded tasks.
- Dispatches to specialist agents.
- Enforces branch protections and merge policies.

### 2) Salesforce integration agent
- Pulls metadata (objects, fields, flows, permission sets) from a **sandbox** first.
- Generates connection adapters (REST/Bulk/Streaming as needed).
- Maintains a typed contract for data access.

### 3) UI observer agent
- Runs browser automation against your target app pages.
- Captures: DOM structure, screenshots, network calls, and user-event traces.
- Produces feature maps: forms, tables, filters, workflows, validations.

### 4) Feature implementation agent
- Converts feature maps + data contracts into app code.
- Builds components and endpoints in vertical slices.
- Opens PRs with tests for each slice.

### 5) QA and regression agent
- Generates end-to-end tests for critical paths.
- Performs visual diffs for key screens.
- Runs contract tests against Salesforce adapters.

### 6) Security/compliance agent
- Scans for secrets and overbroad permissions.
- Validates least-privilege OAuth scopes.
- Audits access logs and data egress rules.

## Salesforce login and data strategy

Use this sequence:

1. **Create a dedicated integration user** in Salesforce (no shared human credentials).
2. Configure a **Connected App** with OAuth (JWT bearer or web-server flow).
3. Start with **minimum scopes** and expand only when blocked.
4. Keep all credentials in a secrets manager (never in prompts/repos).
5. Point agents to **sandbox org first**, then promote to production after test gates.

## "See my page" strategy (without unsafe remote-control patterns)

Instead of giving agents unrestricted desktop control:

- Use a controlled browser automation layer (Playwright/Cypress-like runner).
- Limit allowed domains and actions with policy rules.
- Record every action and artifact (screenshots, network HAR, logs).
- Require human approval for destructive steps (delete/update/publish).

This gives agents page awareness while preserving security and traceability.

## 24/7 multi-agent ops model

- Queue system for tasks (priority + SLA).
- Workers per agent role with concurrency caps.
- Auto-retries with backoff and dead-letter queues.
- Observability dashboard:
  - task throughput,
  - fail rate,
  - PR cycle time,
  - test pass rate,
  - API error budgets.
- Pager/alerts for repeated failures or auth drift.

## Fastest path to a working pilot (7 steps)

1. Pick one business workflow to clone (e.g., lead intake + qualification).
2. Export Salesforce metadata for only relevant objects.
3. Capture 3-5 real UI sessions of that workflow.
4. Generate a feature map + data contract.
5. Build one vertical slice (UI + API + sync) in a staging app.
6. Add regression tests and visual checks.
7. Run continuous agent loop on that slice before expanding.

## Guardrails you should keep

- Human-in-the-loop approvals for schema migrations and production writes.
- No direct use of your personal Salesforce credentials.
- Strict environment separation (dev/stage/prod orgs and keys).
- Mandatory PR checks: tests, lint, secret scan, dependency scan.

## If you want, I can next produce

- A concrete agent runbook (roles, prompts, escalation rules).
- A Salesforce connected-app checklist and scope matrix.
- A reference task board structure for round-the-clock execution.
- A minimal architecture starter (repo layout + CI + agent queue definitions).
