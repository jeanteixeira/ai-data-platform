"""Command-line entry point for the local Data Platform AI environment."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from collections.abc import Sequence
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


JUPYTER_HEALTH_URL = "http://localhost:8888/api"
AIRFLOW_HEALTH_URL = "http://localhost:8080/api/v2/monitor/health"
SUPPORTED_JOBS = {"hello_world": "hello_world_python_job"}


def run_command(command: Sequence[str], timeout: int = 10) -> tuple[bool, str]:
    """Run a local command and return its success state and diagnostic output."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            check=False,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return False, str(error)

    output = result.stdout.strip() or result.stderr.strip()
    return result.returncode == 0, output


def fetch_json(url: str) -> tuple[dict[str, Any] | None, str]:
    """Fetch a local JSON health endpoint."""
    try:
        with urlopen(url, timeout=3) as response:
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        return None, str(error)
    return payload, "available"


def print_check(name: str, available: bool, detail: str) -> None:
    status = "OK" if available else "FAILED"
    print(f"[{status}] {name}: {detail}")


def doctor() -> int:
    """Check the dependencies and health of the local Platform environment."""
    failed = False

    docker_path = shutil.which("docker")
    if docker_path is None:
        docker_ok, docker_detail = False, "docker executable not found"
    else:
        docker_ok, docker_detail = run_command(
            [docker_path, "version", "--format", "{{.Server.Version}}"]
        )
        if docker_ok:
            docker_detail = f"Docker daemon {docker_detail}"
    print_check("Docker", docker_ok, docker_detail)
    failed |= not docker_ok

    if docker_path is None:
        compose_ok, compose_detail = False, "Docker is unavailable"
    else:
        compose_ok, compose_detail = run_command(
            [docker_path, "compose", "version", "--short"]
        )
        if compose_ok:
            compose_detail = f"Docker Compose {compose_detail}"
    print_check("Docker Compose", compose_ok, compose_detail)
    failed |= not compose_ok

    jupyter_health, jupyter_detail = fetch_json(JUPYTER_HEALTH_URL)
    jupyter_ok = jupyter_health is not None
    print_check("JupyterLab", jupyter_ok, jupyter_detail)
    failed |= not jupyter_ok

    airflow_health, airflow_detail = fetch_json(AIRFLOW_HEALTH_URL)
    airflow_ok = airflow_health is not None
    print_check("Airflow", airflow_ok, airflow_detail)
    failed |= not airflow_ok

    if airflow_health is None:
        metadata_ok = scheduler_ok = False
        metadata_detail = scheduler_detail = "Airflow health endpoint unavailable"
    else:
        metadata_detail = airflow_health.get("metadatabase", {}).get(
            "status", "unknown"
        )
        scheduler_detail = airflow_health.get("scheduler", {}).get(
            "status", "unknown"
        )
        metadata_ok = metadata_detail == "healthy"
        scheduler_ok = scheduler_detail == "healthy"

    print_check("Airflow metadata database", metadata_ok, metadata_detail)
    print_check("Airflow scheduler", scheduler_ok, scheduler_detail)
    failed |= not metadata_ok or not scheduler_ok

    print("Platform is ready." if not failed else "Platform is not ready.")
    return 1 if failed else 0


def list_jobs() -> int:
    """List the manually supported jobs."""
    print("Available jobs:")
    for job_name in SUPPORTED_JOBS:
        print(f"- {job_name}")
    return 0


def run_job(job_name: str) -> int:
    """Ask Airflow to orchestrate a supported job."""
    dag_id = SUPPORTED_JOBS[job_name]
    command = [
        "docker",
        "compose",
        "exec",
        "-T",
        "airflow-scheduler",
        "airflow",
        "dags",
        "trigger",
        dag_id,
    ]
    success, detail = run_command(command, timeout=30)
    if not success:
        print(f"Failed to trigger job '{job_name}': {detail}", file=sys.stderr)
        return 1

    print(f"Triggered job '{job_name}' through Airflow DAG '{dag_id}'.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dataplatform",
        description="Manage the local Data Platform AI environment.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("doctor", help="Check local Platform dependencies")

    jobs_parser = subparsers.add_parser("jobs", help="Inspect and run jobs")
    jobs_subparsers = jobs_parser.add_subparsers(dest="jobs_command", required=True)
    jobs_subparsers.add_parser("list", help="List supported jobs")
    run_parser = jobs_subparsers.add_parser("run", help="Trigger a job through Airflow")
    run_parser.add_argument("job_name", choices=SUPPORTED_JOBS)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "doctor":
        return doctor()
    if args.jobs_command == "list":
        return list_jobs()
    return run_job(args.job_name)
