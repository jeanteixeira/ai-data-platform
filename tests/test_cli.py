import io
import unittest
from unittest.mock import patch

from dataplatform import cli


class DoctorTests(unittest.TestCase):
    @patch("dataplatform.cli.fetch_json")
    @patch("dataplatform.cli.run_command")
    @patch("dataplatform.cli.shutil.which", return_value="/usr/bin/docker")
    def test_doctor_succeeds_when_platform_is_healthy(
        self, which_mock, run_command_mock, fetch_json_mock
    ):
        run_command_mock.side_effect = [(True, "28.0.0"), (True, "2.35.0")]
        fetch_json_mock.side_effect = [
            ({"version": "2.16.0"}, "available"),
            (
                {
                    "metadatabase": {"status": "healthy"},
                    "scheduler": {"status": "healthy"},
                },
                "available",
            ),
        ]

        with patch("sys.stdout", new_callable=io.StringIO) as output:
            exit_code = cli.main(["doctor"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Platform is ready.", output.getvalue())

    @patch("dataplatform.cli.fetch_json", return_value=(None, "connection refused"))
    @patch("dataplatform.cli.run_command", return_value=(False, "daemon unavailable"))
    @patch("dataplatform.cli.shutil.which", return_value="/usr/bin/docker")
    def test_doctor_fails_when_dependencies_are_unavailable(
        self, which_mock, run_command_mock, fetch_json_mock
    ):
        with patch("sys.stdout", new_callable=io.StringIO) as output:
            exit_code = cli.main(["doctor"])

        self.assertEqual(exit_code, 1)
        self.assertIn("[FAILED] Docker", output.getvalue())
        self.assertIn("Platform is not ready.", output.getvalue())


class JobsTests(unittest.TestCase):
    def test_jobs_list_displays_hello_world(self):
        with patch("sys.stdout", new_callable=io.StringIO) as output:
            exit_code = cli.main(["jobs", "list"])

        self.assertEqual(exit_code, 0)
        self.assertIn("- hello_world", output.getvalue())

    @patch("dataplatform.cli.run_command", return_value=(True, "triggered"))
    def test_jobs_run_delegates_to_airflow(self, run_command_mock):
        with patch("sys.stdout", new_callable=io.StringIO):
            exit_code = cli.main(["jobs", "run", "hello_world"])

        self.assertEqual(exit_code, 0)
        run_command_mock.assert_called_once_with(
            [
                "docker",
                "compose",
                "exec",
                "-T",
                "airflow-scheduler",
                "airflow",
                "dags",
                "trigger",
                "hello_world_python_job",
            ],
            timeout=30,
        )

    @patch("dataplatform.cli.run_command", return_value=(False, "scheduler unavailable"))
    def test_jobs_run_reports_airflow_failure(self, run_command_mock):
        with patch("sys.stderr", new_callable=io.StringIO) as error_output:
            exit_code = cli.main(["jobs", "run", "hello_world"])

        self.assertEqual(exit_code, 1)
        self.assertIn("scheduler unavailable", error_output.getvalue())


if __name__ == "__main__":
    unittest.main()
