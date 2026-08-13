from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.docker.operators.docker import DockerOperator


with DAG(
    dag_id="hello_world_python_job",
    description="Run the isolated hello world Python job container",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["example", "python-job"],
) as dag:
    DockerOperator(
        task_id="run_hello_world_job",
        image="data-platform-ai/hello-world-job:local",
        docker_url="unix://var/run/docker.sock",
        network_mode="none",
        mount_tmp_dir=False,
        auto_remove="success",
        force_pull=False,
    )
