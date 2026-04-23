# Orchestrator Overview

## Purpose

The orchestrator coordinates multiple agents over a target workspace that may live outside this repository.

## Target Workspace Model

- The orchestrator repo contains the orchestration logic.
- The target workspace contains the application code under review or modification.
- The architect agent inspects the target project for hexagonal boundaries and Java build signals, including JIB-related configuration when present.

## Agent Order

1. Intake and classify task.
2. Run developer and documenter lanes when needed.
3. Run architect review as the approval gate.
4. Publish only after architect approval.
