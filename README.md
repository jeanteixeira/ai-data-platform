# Data Platform AI

Data Platform AI is an open source platform for developing, publishing, orchestrating, and running data and AI workloads. The project aims to provide a cohesive developer experience that begins with exploratory notebooks and grows into reproducible production jobs.

The platform is being built incrementally. Each Sprint must deliver a small, understandable capability without anticipating infrastructure or abstractions that have not yet proved necessary.

> **Project status:** foundation phase. No application or infrastructure is implemented yet.

## Vision

Data engineers should be able to explore data in a notebook, use AI to turn that work into maintainable production code, and run the resulting job through a consistent orchestration and execution experience.

The long-term vision includes:

- notebook-based development;
- Python and Spark data pipelines;
- orchestration with Apache Airflow;
- an AI coding assistant;
- publishing notebooks as production jobs;
- machine learning workflows and AI agents;
- local development with Docker Compose;
- scalable execution with Kubernetes and Kubeflow.

## Objectives

- Keep development and production concerns separate: notebooks are for exploration; jobs are reproducible production artifacts.
- Offer a local-first onboarding experience before introducing distributed infrastructure.
- Make generated code visible, reviewable, testable, and versionable.
- Adopt stable, explicit contracts only when the product needs them.
- Build a welcoming, documented, and maintainable open source project.

## Target architecture

The first MVP will demonstrate one end-to-end flow:

```text
Notebook
   ↓
Publisher + AIProvider
   ↓
Reviewable job candidate + Job Specification
   ↓
Apache Airflow
   ↓
DockerOperator
   ↓
Isolated job container
```

The target architecture may later add Spark, Kubernetes, Kubeflow, ML workflows, and AI agents. These capabilities are deliberately outside the current implementation scope. See [the architecture documentation](docs/architecture/README.md) for the boundaries and evolution strategy.

In this project, the Publisher creates a reviewable job candidate in the local workspace. Publishing makes that candidate available for validation and human review; it does not deploy the job directly to a production environment.

## Roadmap

1. **Foundation:** project documentation, conventions, and metadata.
2. **Local Runtime:** Docker Compose, JupyterLab, Airflow, PostgreSQL, and a manually authored example job.
3. **Publisher:** notebook parsing, a minimal Job Specification, deterministic publishing, and end-to-end validation.
4. **Local AI:** local model integration through `AIProvider`, generation safeguards, and human review.
5. **Developer experience:** stronger CLI, templates, tests, documentation, and release automation.
6. **Distributed workloads:** Spark and Kubernetes execution when justified by validated use cases.
7. **ML and agents:** Kubeflow-backed ML workflows and governed AI agents.

The detailed plan is maintained in [docs/roadmap](docs/roadmap/README.md).

## Planned technologies

| Area | Planned technology |
|---|---|
| Primary language | Python |
| Local environment | Docker Compose |
| Notebook development | JupyterLab |
| Orchestration | Apache Airflow |
| Local job execution | Docker and Airflow `DockerOperator` |
| Airflow metadata | PostgreSQL |
| Local AI inference | Ollama or a compatible local provider |
| Distributed data processing | Apache Spark, in a later phase |
| Cluster orchestration | Kubernetes, in a later phase |
| ML workflows | Kubeflow, in a later phase |

Technology choices listed for later phases express direction, not current dependencies or commitments.

## Repository structure

```text
docs/
├── architecture/  Target architecture and system boundaries
├── roadmap/       Incremental delivery plan
└── adr/           Architectural decision records
```

Application and infrastructure directories will be introduced only by the Sprint that implements them.

## Development

The repository does not contain runnable application code yet. Make targets exist only as placeholders for the future developer interface:

```bash
make start
make stop
make test
make lint
make format
make clean
```

See [AGENTS.md](AGENTS.md) before contributing with an AI Coding Agent.
Human contributors should also read [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Data Platform AI is available under the [MIT License](LICENSE).
