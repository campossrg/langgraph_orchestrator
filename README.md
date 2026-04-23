# LangGraph Orchestrator

This project provides a LangGraph-based orchestrator that delegates work to three subagents over an external target workspace, such as a parallel Java backend repository.

## Agents

- `developer`: implements and verifies code changes in the target workspace.
- `documenter`: updates `README.md`, Obsidian docs, `CHANGELOG.md`, and version metadata.
- `architect`: reviews hexagonal-architecture compliance, checks Java backend signals such as JIB-related build configuration, and gates publication.

## Scope

The orchestrator is designed to work over a target project path instead of assuming that the target code lives inside this repository.

Typical uses:

- orchestrate work over a parallel Java backend project
- review whether the target repository follows ports-and-adapters boundaries
- prepare docs and version updates after code work completes
- publish approved work through Git CLI workflows

## Project Structure

```text
src/langgraph_orchestrator/
  domain/        Core models and policies
  application/   Use cases and orchestration services
  adapters/      Filesystem, git, and project inspection adapters
  agents/        Agent contracts and execution logic
  graph/         LangGraph nodes and graph builder
  cli/           Command-line interface
  config/        Runtime configuration
```

## Usage

Install locally:

```bash
pip install -e .[dev]
```

Optional local environment file:

```bash
copy .env.example .env
```

## API Keys

Set provider credentials in either:

- a local `.env` file in the project root
- your shell environment variables

Supported variables:

- `ORCHESTRATOR_MODEL_PROVIDER` with `openai` or `anthropic`
- `ORCHESTRATOR_MODEL_NAME`
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`

Example `.env`:

```dotenv
ORCHESTRATOR_MODEL_PROVIDER=openai
ORCHESTRATOR_MODEL_NAME=gpt-4o-mini
OPENAI_API_KEY=your-openai-api-key
```

If no API key is configured, the orchestrator falls back to deterministic local agent behavior.

Run the orchestrator against a target workspace:

```bash
orchestrator run --task "Implement a booking cancellation endpoint" --target-path "C:/path/to/backend"
```

With publication enabled:

```bash
orchestrator run --task "Implement a booking cancellation endpoint" --target-path "C:/path/to/backend" --publish
```

Architect-only review:

```bash
orchestrator review --task "Review architecture" --target-path "C:/path/to/backend"
```

## Notes About GitLab And JIB

- The orchestrator currently uses `git` for publication workflows.
- `glab` can be added later behind the GitLab adapter.
- JIB is treated as a target-project concern. The architect agent inspects Java repositories for JIB-related configuration but the orchestrator itself does not depend on the JIB library.
