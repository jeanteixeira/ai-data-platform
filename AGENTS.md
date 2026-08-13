# AI Coding Agent Guide

This file is the primary operating guide for AI Coding Agents working in the Data Platform AI repository. Instructions in a more deeply nested `AGENTS.md`, if one is introduced later, apply to that subtree and may refine this guide.

## Project vision

Data Platform AI is an open source platform for taking data work from exploration to reliable execution. Its defining workflow begins in a notebook, uses AI to help produce a reviewable production job, and delegates orchestration and execution to established tools.

The long-term platform may support Python and Spark pipelines, Apache Airflow, ML workflows, AI agents, Kubernetes, and Kubeflow. Long-term direction must not be confused with current scope.

## Project philosophy

- Deliver a working vertical slice before expanding the platform surface.
- Prefer simple, explicit code over speculative generalization.
- Treat notebooks as development artifacts and jobs as production artifacts.
- Treat AI output as untrusted, reviewable input—not as an authority.
- Use established open source components where they provide clear value.
- Keep local development accessible and reproducible.
- Make security, observability, and documentation part of design decisions.
- Introduce abstractions only after a concrete need appears.

## Architectural principles

1. **Local first:** the MVP must run locally with Docker Compose.
2. **Clear promotion boundary:** Airflow must execute jobs, not notebooks.
3. **Review before execution:** AI-generated code must be inspectable before it is published or run.
4. **Minimal contracts:** the Job Specification (`JobSpec`) describes only information used by the current product.
5. **Replaceable AI integration:** `AIProvider` isolates the Publisher from one model vendor without creating a general plugin framework.
6. **Thin orchestration:** jobs must not import or depend on Airflow internals.
7. **Isolated jobs:** production jobs run in their own containers and communicate through explicit inputs, outputs, environment, and logs.
8. **Incremental evolution:** Spark, Kubernetes, Kubeflow, ML, and agents remain deferred until their Sprint.
9. **Document significant choices:** record durable or costly-to-reverse decisions as ADRs.

Do not introduce a full hexagonal architecture, generic execution layer, job registry, distributed control plane, or plugin system without an approved requirement.

## MVP scope

The MVP will eventually prove this flow:

```text
Jupyter notebook
  → Publisher using an AIProvider
  → reviewable Python job candidate with a minimal Job Specification
  → Apache Airflow DAG
  → DockerOperator
  → job container
```

The planned MVP is single-user, local, and development-oriented. It does not promise production cluster operation, multitenancy, high availability, or distributed execution.

The Publisher writes a job candidate to the local publication area so it can be validated and reviewed. In the MVP, "publish" never means deploying directly to a production environment.

### Current Sprint 1A scope

Only the local JupyterLab environment is in scope:

- one JupyterLab service managed by Docker Compose;
- a persistent local notebook workspace;
- one small pandas example notebook;
- minimal Make commands and startup documentation.

Airflow, PostgreSQL, Streamlit, AI, Spark, Kubernetes, Kubeflow, and application code remain outside Sprint 1A.

## Technologies

### Current

- Markdown documentation;
- TOML project metadata;
- Make as the local command interface;
- Docker and Docker Compose;
- JupyterLab and pandas;
- Git and the MIT License.

### Planned for the MVP

- Python application code;
- Apache Airflow and `DockerOperator`;
- PostgreSQL for Airflow metadata;
- a local AI provider, initially expected to be Ollama.

### Future, not current scope

- Apache Spark;
- Kubernetes;
- Kubeflow;
- ML workflow tooling;
- governed AI agents;
- production-grade security, storage, and observability integrations.

Do not add a future technology merely because it appears in this list.

## Code conventions

These conventions apply when Python code is introduced:

- Target the Python version declared in `pyproject.toml`.
- Use type hints for public functions and important internal boundaries.
- Keep functions and modules small, cohesive, and explicitly named.
- Prefer standard-library solutions when they remain clear and maintainable.
- Separate side effects from transformation logic where practical.
- Raise specific exceptions with actionable messages.
- Do not silently catch errors or hide failed validation.
- Never embed credentials, tokens, or machine-specific paths.
- Add tests for new behavior and regressions.
- Keep generated production jobs independent from Jupyter and Airflow imports.
- Avoid generic base classes, factories, registries, and dependency injection unless the active requirement needs them.

Formatting, linting, and test tools must be selected in the Sprint that first needs them. Do not infer configured tooling from placeholder Make targets.

## Documentation conventions

- Write user-facing documentation in clear English unless a document explicitly targets another language.
- Use short sections, descriptive headings, and runnable examples when implementation exists.
- Distinguish current behavior from planned behavior.
- Do not describe a planned component as already available.
- Update relevant documentation in the same change as behavior or architecture.
- Use relative links for repository documents.
- Add an ADR for important decisions that constrain future work or are expensive to reverse.
- Follow the process in `docs/adr/README.md` for ADRs.

## How agents must work

For every task:

1. Read this file and any more specific `AGENTS.md` in the target directory.
2. Inspect the repository and current working tree before editing.
3. Restate the requested scope and give a brief implementation strategy.
4. Implement only the active Sprint or task; do not prepare unrelated future components.
5. Preserve user changes and avoid destructive Git operations.
6. Prefer the smallest coherent change that satisfies the request.
7. Run relevant validations when possible.
8. Review the diff for accidental scope growth, secrets, and stale documentation.
9. Summarize changed files, validations, decisions, and remaining limitations.
10. Wait for review before starting a new Sprint.

Agents must ask for direction when a missing decision would materially alter the design. Otherwise, make the smallest reasonable assumption and state it.

## Prohibited scope expansion

Unless explicitly requested by the active Sprint, do not:

- create services, containers, or deployment manifests;
- add application code or dependencies;
- implement future roadmap capabilities;
- add unused directory hierarchies or placeholder modules;
- add frameworks for hypothetical integrations;
- publish packages, create releases, or modify external systems;
- mix broad refactoring with a focused task.

The roadmap communicates direction; it is not authorization to implement future phases.

## Project Language

The official language of this repository is English.

All permanent artifacts must be written in English, including:

- documentation
- comments
- code
- commit messages
- pull requests
- ADRs
- architecture documents

Conversations with AI agents may happen in any language, but all generated repository content must be written in English.
