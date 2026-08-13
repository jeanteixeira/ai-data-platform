# Hello World Python Job

This minimal job proves that a pandas workload can run independently in an isolated container. It contains no Airflow-specific code; Airflow only builds the orchestration boundary around the image.

## Build

From the repository root:

```bash
docker compose build hello-world-job
```

## Run manually

```bash
docker compose run --rm hello-world-job
```

The job writes its input size, transformed category totals, and completion status to standard output. A successful run exits with status code `0`.

The container has no network access when started by the example Airflow DAG and never receives the host Docker socket.
