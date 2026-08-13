"""Deterministic conversion of supported notebooks into job candidates."""

from __future__ import annotations

import ast
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

import nbformat
import yaml

from dataplatform.jobspec import JOB_NAME_PATTERN, JobSpec, JobSpecError


DEFAULT_OUTPUT_ROOT = Path("jobs/generated")
PINNED_REQUIREMENT_PATTERN = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9._-]*(?:\[[A-Za-z0-9_,.-]+\])?"
    r"==[A-Za-z0-9][A-Za-z0-9._+!-]*$"
)

DOCKERFILE_TEMPLATE = """FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt

COPY src/ ./src/

RUN useradd --create-home --uid 10001 job
USER job

ENTRYPOINT [\"python\", \"src/main.py\"]
"""

README_TEMPLATE = """# {name}

This directory is a deterministic job candidate generated from `{notebook}`.

The candidate must be reviewed and validated before promotion. Publishing did not register, schedule, build, deploy, or execute this job.

## Review checklist

- Review `src/main.py` for notebook-only assumptions and hidden state.
- Confirm every dependency and version in `requirements.txt`.
- Review `job.yaml`, including any schedule metadata.
- Build and run the container manually when the candidate is ready for validation.

```bash
docker build --tag data-platform-ai/{name}:candidate jobs/generated/{name}
docker run --rm data-platform-ai/{name}:candidate
```
"""


class PublisherError(ValueError):
    """Raised when a notebook cannot be published safely."""


def normalize_job_name(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    if not JOB_NAME_PATTERN.fullmatch(normalized):
        raise PublisherError(
            "job name must start with a letter and contain only letters, numbers, "
            "or underscores after normalization"
        )
    return normalized


def read_notebook(path: Path) -> Any:
    if not path.is_file():
        raise PublisherError(f"notebook does not exist: {path}")
    try:
        return nbformat.read(path, as_version=4)
    except (OSError, nbformat.ValidationError, nbformat.reader.NotJSONError) as error:
        raise PublisherError(f"unable to parse notebook: {error}") from error


def validate_python_notebook(notebook: Any) -> None:
    language = str(notebook.metadata.get("language_info", {}).get("name", ""))
    kernel_language = str(notebook.metadata.get("kernelspec", {}).get("language", ""))
    if language.lower() != "python" and kernel_language.lower() != "python":
        raise PublisherError("only notebooks with Python language metadata are supported")


def extract_python(notebook: Any) -> str:
    sources: list[str] = []
    for index, cell in enumerate(notebook.cells, start=1):
        if cell.cell_type != "code" or not cell.source.strip():
            continue
        source = str(cell.source).rstrip()
        for line in source.splitlines():
            if line.lstrip().startswith(("%", "!", "?")):
                raise PublisherError(
                    f"code cell {index} contains an unsupported notebook command"
                )
        try:
            tree = ast.parse(source, filename=f"notebook cell {index}")
        except SyntaxError as error:
            raise PublisherError(f"code cell {index} is not valid Python: {error.msg}") from error
        if any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "get_ipython"
            for node in ast.walk(tree)
        ):
            raise PublisherError(
                f"code cell {index} uses unsupported IPython runtime behavior"
            )
        sources.append(f"# Notebook code cell {index}\n{source}")

    if not sources:
        raise PublisherError("notebook does not contain executable Python code cells")

    generated = (
        '"""Deterministically generated from a reviewed Python notebook."""\n\n'
        + "\n\n".join(sources)
        + "\n"
    )
    try:
        compile(generated, "src/main.py", "exec")
    except SyntaxError as error:
        raise PublisherError(f"generated entrypoint is not valid Python: {error.msg}") from error
    return generated


def read_requirements(notebook: Any) -> list[str]:
    metadata = notebook.metadata.get("dataplatform", {})
    requirements = metadata.get("requirements", [])
    if not isinstance(requirements, list) or not all(
        isinstance(item, str) for item in requirements
    ):
        raise PublisherError(
            "metadata.dataplatform.requirements must be a list of pinned strings"
        )
    for requirement in requirements:
        if not PINNED_REQUIREMENT_PATTERN.fullmatch(requirement):
            raise PublisherError(
                f"requirement must use an exact version with '==': {requirement!r}"
            )
    return requirements


def write_candidate(
    destination: Path,
    notebook_path: Path,
    job_spec: JobSpec,
    source: str,
    requirements: list[str],
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=f".{job_spec.name}-", dir=destination.parent)
    )
    try:
        (staging / "src").mkdir()
        (staging / "src/main.py").write_text(source, encoding="utf-8")
        requirements_text = "".join(f"{item}\n" for item in requirements)
        (staging / "requirements.txt").write_text(
            requirements_text, encoding="utf-8"
        )
        (staging / "job.yaml").write_text(
            yaml.safe_dump(job_spec.to_dict(), sort_keys=False), encoding="utf-8"
        )
        (staging / "Dockerfile").write_text(DOCKERFILE_TEMPLATE, encoding="utf-8")
        (staging / "README.md").write_text(
            README_TEMPLATE.format(name=job_spec.name, notebook=notebook_path),
            encoding="utf-8",
        )
        staging.rename(destination)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def publish_notebook(
    notebook_path: Path,
    *,
    name: str | None = None,
    schedule: str | None = None,
    force: bool = False,
    output_root: Path = DEFAULT_OUTPUT_ROOT,
) -> Path:
    """Create a reviewable job candidate without deploying or executing it."""
    job_name = normalize_job_name(name or notebook_path.stem)
    destination = output_root / job_name
    if destination.exists() and not force:
        raise PublisherError(
            f"job candidate already exists: {destination}; use --force to replace it"
        )

    notebook = read_notebook(notebook_path)
    validate_python_notebook(notebook)
    source = extract_python(notebook)
    requirements = read_requirements(notebook)
    job_spec = JobSpec(name=job_name, schedule=schedule)
    try:
        job_spec.validate()
    except JobSpecError as error:
        raise PublisherError(f"invalid JobSpec: {error}") from error

    if destination.exists():
        shutil.rmtree(destination)
    write_candidate(destination, notebook_path, job_spec, source, requirements)
    return destination
