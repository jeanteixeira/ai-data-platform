from datetime import datetime, timezone

from airflow.sdk import DAG, task


with DAG(
    dag_id="platform_health_check",
    description="Validates local Airflow scheduling and task execution.",
    schedule=None,
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    tags=["example", "health"],
) as dag:

    @task
    def confirm_airflow_is_ready() -> str:
        """Return a deterministic message for local orchestration validation."""
        return "Airflow orchestration is ready."

    confirm_airflow_is_ready()
