# Project Roadmap

This roadmap communicates intended sequence, not delivery dates or permission to implement later phases. Scope is approved one Sprint at a time. Each phase should leave the repository usable, documented, and tested at its actual level of maturity.

## Phase 0 — Foundation

Establish a professional open source project baseline.

- project vision and objectives;
- architecture and roadmap documentation;
- guidance for contributors and AI Coding Agents;
- ADR process;
- project metadata and placeholder developer commands.

**Exit condition:** the project's direction, constraints, and contribution workflow are understandable without application code.

## Phase 1 — Local Runtime

Prove that Airflow can run a manually authored Python job in a separate container.

- Docker Compose environment;
- JupyterLab;
- Apache Airflow and PostgreSQL;
- one manually authored Python job;
- Airflow `DockerOperator` execution;
- logs visible through Airflow;
- local setup and teardown documentation.

**Exit condition:** a contributor can start the environment and execute the example job end to end.

## Phase 2 — Deterministic Publisher

Connect notebook development to job publication without relying on model inference.

- notebook parsing;
- minimal versioned Job Specification (`JobSpec`);
- Publisher command-line interface;
- deterministic or fake `AIProvider` for testing;
- generated job structure;
- validation and atomic publication;
- automated end-to-end test.

**Exit condition:** an example notebook can become a reviewable job and run through Airflow reproducibly.

For the MVP, publication writes a job candidate to the local publication area for validation and human review. It does not deploy directly to a production environment.

## Phase 3 — Local AI

Introduce real AI assistance while keeping execution governed.

- local model integration through `AIProvider`;
- structured notebook context;
- versioned prompt templates;
- structured response validation;
- generation metadata and useful failures;
- explicit human review before publication and execution.

**Exit condition:** a local model can propose a valid job from the example notebook without bypassing review.

## Phase 4 — MVP hardening and developer experience

Turn the demonstrated flow into a reliable open source MVP.

- stable CLI ergonomics;
- job and notebook examples;
- unit, integration, and end-to-end coverage;
- dependency and image hygiene;
- documented resource requirements and limitations;
- contribution workflow and release automation;
- basic generation and execution security controls.

**Exit condition:** a new contributor can install, understand, test, and extend the MVP using documented workflows.

## Phase 5 — Distributed data processing

Add Spark only after the Python job lifecycle is stable.

- concrete Spark workload contract;
- local Spark development and execution experience;
- Airflow orchestration;
- representative distributed transformation example;
- compatibility and resource documentation.

**Exit condition:** Spark adds a validated workload type without complicating the existing Python path unnecessarily.

## Phase 6 — Kubernetes execution

Move selected workloads from the local Docker runtime to a cluster environment.

- Kubernetes deployment model;
- workload isolation and resource controls;
- secrets and persistent storage integration;
- cluster-native job execution;
- operational observability;
- development-cluster documentation.

**Exit condition:** the same product concepts support a documented cluster workflow with appropriate security boundaries.

## Phase 7 — ML workflows and Kubeflow

Support reproducible machine learning lifecycle use cases.

- training and evaluation jobs;
- experiment and artifact tracking decisions;
- Kubeflow pipeline integration;
- model promotion and serving boundaries;
- lineage between data, code, runs, and models.

**Exit condition:** an ML workflow can be reproduced, inspected, and governed through explicit artifacts.

## Phase 8 — Governed AI agents

Add agentic capabilities only after permissions and execution boundaries are mature.

- explicit agent tools and permissions;
- sandboxed execution;
- audit trail and approval gates;
- defenses for prompt injection and data exfiltration;
- human-in-the-loop workflows;
- operational limits and failure handling.

**Exit condition:** agents can assist with bounded platform tasks without gaining implicit authority over infrastructure or data.

## Roadmap principles

- Complete and validate the current phase before expanding scope.
- Prefer one working path over several incomplete paths.
- Record major architectural changes with ADRs.
- Keep future technologies out of current runtime dependencies.
- Revisit this roadmap as evidence from users and contributors changes priorities.
