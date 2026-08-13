"""Minimal Job Specification for Python job candidates."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


JOB_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,62}$")


class JobSpecError(ValueError):
    """Raised when a Job Specification is invalid."""


@dataclass(frozen=True)
class JobSpec:
    """Versioned metadata required by the current Python job template."""

    name: str
    schedule: str | None = None
    version: int = 1
    runtime: str = "python"
    python_version: str = "3.12"
    entrypoint: str = "src/main.py"

    def validate(self) -> None:
        if self.version != 1:
            raise JobSpecError("JobSpec version must be 1")
        if not JOB_NAME_PATTERN.fullmatch(self.name):
            raise JobSpecError(
                "job name must start with a lowercase letter and contain only "
                "lowercase letters, numbers, or underscores (maximum 63 characters)"
            )
        if self.runtime != "python":
            raise JobSpecError("runtime must be 'python'")
        if self.python_version != "3.12":
            raise JobSpecError("python_version must be '3.12'")
        if self.entrypoint != "src/main.py":
            raise JobSpecError("entrypoint must be 'src/main.py'")
        if self.schedule is not None and (
            not self.schedule.strip() or "\n" in self.schedule or "\r" in self.schedule
        ):
            raise JobSpecError("schedule must be a non-empty single-line value")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        document: dict[str, Any] = {
            "version": self.version,
            "name": self.name,
            "runtime": self.runtime,
            "python_version": self.python_version,
            "entrypoint": self.entrypoint,
        }
        if self.schedule is not None:
            document["schedule"] = self.schedule
        return document
