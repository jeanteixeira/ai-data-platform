# ADR-0001: Use Docker Compose for the Local Development Runtime

- Status: Accepted
- Date: 2026-08-12
- Decision owners: Data Platform AI maintainers

## Context

Data Platform AI needs an accessible and reproducible local development experience for its MVP. The initial workflow will eventually coordinate multiple established components, including JupyterLab, Apache Airflow, PostgreSQL, and local job containers. Sprint 0 does not implement those components, but the project requires a clear runtime direction for subsequent Sprints.

The MVP is intentionally single-user and local. Introducing a cluster orchestrator at this stage would increase setup cost and operational complexity before the core notebook-to-job workflow has been validated.

## Decision

Use Docker Compose as the Local Development Runtime for the MVP.

Docker Compose will define and coordinate the local services introduced by future approved Sprints. This decision establishes the local runtime direction only; it does not define a production deployment architecture and does not authorize implementation outside the active Sprint.

## Consequences

- Contributors will have one local entry point for starting and stopping the Platform environment.
- Service dependencies and local networking can be documented and reproduced consistently.
- The MVP can validate its end-to-end workflow without requiring Kubernetes.
- Contributors must have a compatible Docker environment.
- Local behavior may not reproduce every operational characteristic of a future cluster environment.
- Security limitations associated with local Docker access must be documented when the runtime is implemented.

## Alternatives considered

### Native host installation

Installing every dependency directly on the host could reduce container overhead, but it would create greater variation across contributor environments and increase setup and support costs.

### Kubernetes for the MVP

Kubernetes could align with the long-term direction, but it would introduce premature operational complexity and raise the barrier to local contribution before the core workflow is proven.

### A custom local orchestrator

A project-specific process manager would duplicate established tooling and create application code unrelated to the MVP's primary value.
