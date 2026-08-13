import ast
import tempfile
import unittest
from pathlib import Path

import nbformat
import yaml

from dataplatform.jobspec import JobSpec, JobSpecError
from dataplatform.publisher import PublisherError, publish_notebook


def write_notebook(
    path: Path,
    *,
    code: str = "value = 1\nprint(value)",
    markdown: str | None = None,
    language: str = "python",
    requirements: list[str] | None = None,
) -> None:
    cells = []
    if markdown is not None:
        cells.append(nbformat.v4.new_markdown_cell(markdown))
    cells.append(nbformat.v4.new_code_cell(code))
    notebook = nbformat.v4.new_notebook(cells=cells)
    notebook.metadata["kernelspec"] = {
        "display_name": language,
        "language": language,
        "name": language,
    }
    notebook.metadata["language_info"] = {"name": language}
    if requirements is not None:
        notebook.metadata["dataplatform"] = {"requirements": requirements}
    nbformat.write(notebook, path)


class PublisherTests(unittest.TestCase):
    def test_publishes_valid_python_notebook(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            notebook_path = root / "sales.ipynb"
            write_notebook(
                notebook_path,
                code="import pandas as pd\nprint(pd.Series([1, 2]).sum())",
                requirements=["pandas==2.3.3"],
            )

            destination = publish_notebook(
                notebook_path, output_root=root / "generated"
            )

            self.assertEqual(destination.name, "sales")
            self.assertEqual(
                sorted(path.relative_to(destination).as_posix() for path in destination.rglob("*")),
                ["Dockerfile", "README.md", "job.yaml", "requirements.txt", "src", "src/main.py"],
            )
            ast.parse((destination / "src/main.py").read_text())
            self.assertEqual(
                (destination / "requirements.txt").read_text(), "pandas==2.3.3\n"
            )

    def test_ignores_markdown_cells(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            notebook_path = root / "documented.ipynb"
            write_notebook(
                notebook_path,
                markdown="This text must not become executable code.",
            )

            destination = publish_notebook(
                notebook_path, output_root=root / "generated"
            )

            source = (destination / "src/main.py").read_text()
            self.assertNotIn("This text must not become executable code.", source)
            self.assertIn("value = 1", source)

    def test_rejects_unsupported_notebook_command(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            notebook_path = root / "magic.ipynb"
            write_notebook(notebook_path, code="%time value = 1")

            with self.assertRaisesRegex(PublisherError, "unsupported notebook command"):
                publish_notebook(notebook_path, output_root=root / "generated")

    def test_rejects_invalid_notebook_document(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            notebook_path = root / "invalid.ipynb"
            notebook_path.write_text("not JSON")

            with self.assertRaisesRegex(PublisherError, "unable to parse notebook"):
                publish_notebook(notebook_path, output_root=root / "generated")

    def test_protects_existing_target(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            notebook_path = root / "sales.ipynb"
            write_notebook(notebook_path)
            output_root = root / "generated"
            publish_notebook(notebook_path, output_root=output_root)

            with self.assertRaisesRegex(PublisherError, "already exists"):
                publish_notebook(notebook_path, output_root=output_root)

    def test_force_explicitly_replaces_existing_target(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            notebook_path = root / "sales.ipynb"
            write_notebook(notebook_path, code="value = 1")
            output_root = root / "generated"
            destination = publish_notebook(notebook_path, output_root=output_root)
            write_notebook(notebook_path, code="value = 2")

            publish_notebook(notebook_path, force=True, output_root=output_root)

            self.assertIn("value = 2", (destination / "src/main.py").read_text())

    def test_applies_optional_name_and_schedule(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            notebook_path = root / "sales.ipynb"
            write_notebook(notebook_path)

            destination = publish_notebook(
                notebook_path,
                name="daily_sales",
                schedule="0 12 * * *",
                output_root=root / "generated",
            )

            specification = yaml.safe_load((destination / "job.yaml").read_text())
            self.assertEqual(specification["name"], "daily_sales")
            self.assertEqual(specification["schedule"], "0 12 * * *")


class JobSpecTests(unittest.TestCase):
    def test_valid_minimal_jobspec(self):
        specification = JobSpec(name="daily_sales")

        self.assertEqual(
            specification.to_dict(),
            {
                "version": 1,
                "name": "daily_sales",
                "runtime": "python",
                "python_version": "3.12",
                "entrypoint": "src/main.py",
            },
        )

    def test_rejects_invalid_jobspec_name(self):
        with self.assertRaises(JobSpecError):
            JobSpec(name="Invalid Name").validate()
