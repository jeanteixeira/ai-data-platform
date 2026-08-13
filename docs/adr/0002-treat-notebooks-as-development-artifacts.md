# ADR-0002: Treat Notebooks as Development Artifacts

- Status: Accepted
- Date: 2026-08-12
- Decision owners: Data Platform AI maintainers

## Context

Notebooks are effective for interactive exploration, iterative development, and communicating data analysis. They can also depend on hidden kernel state, non-linear cell execution, local files, interactive commands, and undeclared dependencies. Those characteristics make a notebook an unsuitable production runtime for the Platform.

Data Platform AI needs an explicit boundary between exploratory development and repeatable orchestration. The Publisher is intended to help transform notebook work into a reviewable job candidate with a Job Specification, while Apache Airflow will eventually orchestrate the resulting job artifact.

## Decision

Treat notebooks exclusively as development artifacts. The Platform will never use a notebook as a production runtime or ask Apache Airflow to execute a notebook directly.

Production-oriented execution must use a separate, reviewable job artifact that can run independently from Jupyter. Publishing creates a job candidate for validation and human review; it does not deploy that candidate directly to a production environment.

## Consequences

- Notebook users retain an interactive environment for exploration.
- Production jobs must declare their executable code, dependencies, configuration, inputs, and outputs explicitly as they are introduced.
- Job candidates remain visible, reviewable, testable, and versionable.
- The Publisher must not preserve hidden notebook state as an execution dependency.
- Some notebook constructs may require manual restructuring before they can become valid jobs.
- The Platform must clearly communicate the promotion boundary to users.

## Alternatives considered

### Execute notebooks directly in Airflow

Direct execution would shorten the initial path but would carry notebook state and development-only behavior into orchestration, weakening reproducibility and separation of responsibilities.

### Treat notebooks as both development and production artifacts

A dual role would blur lifecycle boundaries and make validation, dependency management, testing, and operational ownership less explicit.

### Require users to rewrite every notebook manually

Manual rewriting would preserve the runtime boundary, but it would not support the Platform's goal of using AI to assist the creation of reviewable job candidates.
