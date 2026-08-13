# Target Architecture

## Purpose

This document describes the intended direction of Data Platform AI. It establishes system boundaries without claiming that the components are currently implemented.

The architecture will evolve through small, validated increments. The MVP is deliberately local and narrow; distributed capabilities are future extensions rather than initial foundations.

## Core workflow

```text
Development                         Production

JupyterLab notebook
        │
        ▼
Publisher ─── AIProvider
        │
        ▼
Reviewable job candidate + Job Specification
        │
        ▼
Apache Airflow
        │
        ▼
DockerOperator
        │
        ▼
Isolated job container
```

The promotion boundary between notebook and job is central. A notebook supports interactive exploration and may contain transient state. A production job must be explicit, reproducible, reviewable, and runnable without Jupyter.

## MVP components

### JupyterLab

Provides the local notebook development environment. It is not a production job runtime.

### Publisher

A small command-line workflow that reads a notebook, asks an `AIProvider` to propose a job, validates the result, and writes a reviewable job candidate to the local publication area. Publishing makes the candidate available for validation and human review; it does not deploy the job directly to a production environment. The Publisher will not initially be a long-running service or maintain its own database.

### AIProvider

A minimal boundary between the Publisher and an AI model. It exists because local deterministic testing and real model inference have different operational needs. It is not intended to become a generic plugin framework in the MVP.

AI-generated code is considered untrusted until reviewed and validated.

### Job Specification

The Job Specification (`JobSpec`) is a small, versioned description of a job containing only fields required by the MVP, such as its name, entrypoint, and image. It must not anticipate Spark or Kubernetes fields before those runtime capabilities exist.

### Apache Airflow

Discovers published job specifications, schedules runs, invokes Docker through `DockerOperator`, and exposes run status and logs. Job code must not depend on Airflow APIs.

### Job container

Runs the production artifact independently from the notebook environment. It accepts explicit configuration, logs to standard output and error, and returns a conventional exit status.

## MVP deployment model

The MVP is a single-user local environment managed with Docker Compose. Its expected runtime services are JupyterLab, Airflow, and PostgreSQL, with a local model service optionally included when AI inference is introduced.

Airflow's use of the host Docker daemon is a known local-development compromise. Job containers must not receive access to the Docker socket. Production deployment and stronger isolation are future concerns.

## Data and control boundaries

- Notebooks are editable development inputs.
- Published job directories contain reviewable job candidates, not production deployments.
- The Job Specification is the contract read by orchestration.
- Airflow controls scheduling but does not contain business logic.
- Job containers own workload execution.
- Logs flow to Airflow through the container runtime.
- Secrets must never be embedded in notebooks, generated source, or versioned configuration.

## Target evolution

After the local workflow is proven, the architecture may evolve in independently justified directions:

- Spark jobs for distributed data processing;
- Kubernetes for cluster execution and stronger workload isolation;
- Kubeflow for ML pipelines;
- model and data artifact management;
- governed AI agents with explicit tools and permissions;
- production security, observability, and multi-user controls.

The project will not build a universal execution abstraction in anticipation of these capabilities. Interfaces and contracts will evolve from concrete implementations and recorded decisions.

## Quality attributes

The architecture prioritizes:

1. **Simplicity:** a new contributor can understand the local flow.
2. **Reproducibility:** jobs and environments can be rebuilt consistently.
3. **Reviewability:** generated code and configuration remain visible.
4. **Isolation:** production jobs execute outside the notebook process.
5. **Traceability:** generation and execution can eventually be attributed to inputs and versions.
6. **Extensibility through evidence:** new boundaries appear only when working use cases require them.

## Architectural decisions

Significant changes to these boundaries must be recorded under [`docs/adr`](../adr/README.md). This document describes the current target; ADRs explain why durable decisions were made.
