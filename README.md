# Data Platform AI

Data Platform AI is an open source platform for developing, publishing, orchestrating, and running data and AI workloads. The project aims to provide a cohesive developer experience that begins with exploratory notebooks and grows into reproducible production jobs.

The platform is being built incrementally. Each Sprint must deliver a small, understandable capability without anticipating infrastructure or abstractions that have not yet proved necessary.

> **Project status:** Sprint 4 provides deterministic notebook publishing alongside the local Platform CLI and Runtime. AI assistance is not implemented yet.

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

### Prerequisites

- Git
- Docker with Docker Compose

### Start the Local Runtime

Clone the repository, enter its directory, and start the Local Runtime:

```bash
git clone https://github.com/jeanteixeira/ai-data-platform.git
cd ai-data-platform
make start
```

After all services become healthy, open:

- JupyterLab: [http://localhost:8888](http://localhost:8888)
- Apache Airflow: [http://localhost:8080](http://localhost:8080)

No credentials are required. Both interfaces are exposed only on the local loopback interface, and their authentication is disabled strictly for this local development environment.

The local [`notebooks`](notebooks) directory is mounted at `/home/jovyan/work` in the container. Notebooks created or changed in JupyterLab therefore persist after the container is stopped or replaced. A small pandas example is available at [`notebooks/examples/pandas-transformation.ipynb`](notebooks/examples/pandas-transformation.ipynb).

Airflow uses PostgreSQL for metadata, stores metadata and logs in persistent Docker volumes, and discovers DAGs from [`airflow/dags`](airflow/dags). The `platform_health_check` DAG validates the orchestration services. The `hello_world_python_job` DAG uses `DockerOperator` to execute the independent example under [`jobs/hello_world`](jobs/hello_world); neither DAG contains business logic.

The local Airflow deployment uses `LocalExecutor` with parallelism limited to four processes. It does not include Celery, Redis, or workers.

### Run the example Python job

`make start` builds the example job image as part of the local setup. To build or run it independently:

```bash
docker compose build hello-world-job
docker compose run --rm hello-world-job
```

To trigger its Airflow DAG from the command line:

```bash
docker compose exec airflow-scheduler airflow dags trigger hello_world_python_job
```

Alternatively, open Airflow, select `hello_world_python_job`, and use **Trigger**. Open the resulting DAG run, select `run_hello_world_job`, and choose **Logs** to inspect the job's standard output.

> **Local security limitation:** `airflow-scheduler` mounts the host Docker socket so `DockerOperator` can create the isolated job container. Access to this socket is effectively host-level control and is acceptable only for this single-user local POC. Do not expose this deployment to untrusted users. The job container itself does not receive the socket and runs without a network when launched by the DAG.

### Platform CLI

From the repository root, create an isolated Python environment and install the CLI in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --editable .
```

The initial commands are:

```bash
dataplatform doctor
dataplatform jobs list
dataplatform jobs run hello_world
dataplatform publish notebooks/examples/pandas-transformation.ipynb
```

`doctor` checks Docker, Docker Compose, JupyterLab, Airflow, the Airflow metadata database, and the scheduler. `jobs run` asks Airflow to trigger the existing DAG; it does not execute job code itself. Use the Airflow UI to follow the triggered run and inspect its task logs.

### Publish a notebook deterministically

Publishing reads supported Python code cells and creates a reviewable job candidate under `jobs/generated/<job_name>/`:

```bash
dataplatform publish notebooks/examples/pandas-transformation.ipynb

dataplatform publish notebooks/examples/pandas-transformation.ipynb \
  --name daily_sales \
  --schedule "0 12 * * *"
```

The generated candidate contains `job.yaml`, `src/main.py`, `requirements.txt`, `Dockerfile`, and a review guide. The command does not register a job, generate an Airflow DAG, build an image, deploy, schedule, or execute anything. If the destination already exists, publishing fails unless `--force` is explicitly supplied.

The deterministic Publisher currently supports sequential, syntactically valid Python code cells. Markdown and saved cell outputs are ignored. IPython magics, shell commands, help syntax, `get_ipython()` calls, non-Python notebooks, and hidden notebook state are unsupported. Code is preserved without semantic refactoring, so reviewers must verify execution order, side effects, paths, and runtime assumptions.

Dependencies are never inferred. A notebook may declare exact versions in metadata:

```json
{
  "dataplatform": {
    "requirements": ["pandas==2.3.3"]
  }
}
```

Only requirements pinned with `==` are accepted. After publication, review the generated source, Job Specification, dependencies, and container definition before manually validating or promoting the candidate.

### Runtime commands

```bash
make start   # Build the runtime and job images, then start local services
make stop    # Stop and remove local containers while preserving data volumes
make logs    # Follow logs from all local services
make status  # Show all service states, including Airflow initialization
make test    # Run the focused CLI test suite
```

The remaining placeholder Make targets clearly report when their functionality is not implemented.

See [AGENTS.md](AGENTS.md) before contributing with an AI Coding Agent.
Human contributors should also read [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Data Platform AI is available under the [MIT License](LICENSE).
