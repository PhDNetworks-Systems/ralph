# Ralph Agent Instructions

## Overview

Ralph is an autonomous AI agent loop that runs AI coding tools (Amp or Claude Code) repeatedly until all PRD items are complete. Each iteration is a fresh instance with clean context.

## Commands

```bash
# Run the flowchart dev server
cd flowchart && npm run dev

# Build the flowchart
cd flowchart && npm run build

# Run Ralph with Amp (default)
./ralph.sh [max_iterations]

# Run Ralph with Claude Code
./ralph.sh --tool claude [max_iterations]
```

## Key Files

- `ralph.sh` - The bash loop that spawns fresh AI instances (supports `--tool amp` or `--tool claude`)
- `prompt.md` - Instructions given to each AMP instance
-  `CLAUDE.md` - Instructions given to each Claude Code instance
- `prd.json.example` - Example PRD format
- `flowchart/` - Interactive React Flow diagram explaining how Ralph works

## Flowchart

The `flowchart/` directory contains an interactive visualization built with React Flow. It's designed for presentations - click through to reveal each step with animations.

To run locally:
```bash
cd flowchart
npm install
npm run dev
```

## Patterns

- Each iteration spawns a fresh AI instance (Amp or Claude Code) with clean context
- Memory persists via git history, `progress.txt`, and `prd.json`
- Stories should be small enough to complete in one context window
- Always update AGENTS.md with discovered patterns for future iterations

## Ship Standard — Cloud execution and release boundaries

Engineering runs only in a verified remote Cloud executor. Before mutation,
record the provider/configuration and runtime/task identity, actual host/OS and
working directory, repository remote/branch/HEAD/tree and clean status, tool
versions, and measured synthetic/read-only command exits. Never use an owner's
Mac/Windows checkout, terminal, filesystem service or desktop automation as an
engineering fallback. Never print credentials or customer records.

Preserve the target project's existing owner, lease/fencing/ledger, dependency
order and production protections. This loop is not a second orchestrator. Use
included subscription capacity only; do not spend API credits, add services or
switch accounts to evade a limit. Stop on a CLI error or permission denial.
Normal CLI permissions remain enabled; an unattended permission request must
fail closed rather than be bypassed.

Ship bounded work through a normal PR with scoped checks and a fresh independent
review from a different model family. Same-family preparation alone does not
satisfy that review gate. Obtain packet-specific approval before transferring
sensitive review material to an external service; old approvals do not cover new
packets. Keep merge/deploy held while a required gate is unmet.

Preserve protected merge methods, deployments and rollback contracts. Record the
exact checked commit/tree, review, merge, actual deployment and live evidence
before claiming delivery. Do not revive dormant/archived products or alter DNS,
billing, production data or customer messaging. WordPress writes retain exact
release approval and a fresh backup. Apple qualification requires a verified
Cloud macOS executor; Linux checks cannot prove iOS or App Store readiness.

The canonical rollout contract is maintained in
https://github.com/PhDNetworks-Systems/quoteforge/blob/main/docs/standards/SHIP-STANDARD.md
and its companion `CODEX-ROLLOUT.md`. Apply the current owner's stricter scope.
