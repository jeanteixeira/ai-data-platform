# Contributing to Data Platform AI

Thank you for your interest in contributing to Data Platform AI. The project evolves through small, explicitly scoped Sprints, and contributions should preserve that incremental approach.

## Before contributing

- Read [README.md](README.md) for the project vision and current status.
- Read [AGENTS.md](AGENTS.md) for architectural principles and repository conventions. These principles apply to human contributors as well as AI Coding Agents.
- Review the [target architecture](docs/architecture/README.md), [roadmap](docs/roadmap/README.md), and relevant [Architecture Decision Records](docs/adr/README.md).
- Confirm that the proposed change belongs to the active Sprint or an approved issue.

## Contribution principles

- Keep changes small, focused, and easy to review.
- Do not implement roadmap items before their scope is approved.
- Prefer straightforward solutions and avoid premature abstractions.
- Keep notebooks as development artifacts and jobs as reviewable production candidates.
- Treat AI-generated output as untrusted until it has been reviewed and validated.
- Update documentation when behavior or an architectural boundary changes.
- Never commit credentials, tokens, private data, or machine-specific configuration.

## Making a change

1. Inspect the current repository state and active Sprint scope.
2. Make only the changes required by that scope.
3. Add or update tests when behavior is introduced or changed.
4. Run the available validation commands and report any that cannot run.
5. Review the final diff for unrelated changes and stale documentation.
6. Submit a clear description of the problem, approach, validation, and limitations.

The Make targets are the intended contributor interface, but some remain placeholders during the foundation phase. A placeholder must not be interpreted as a completed validation.

## Architectural decisions

Create an ADR only for decisions that establish durable boundaries, select foundational technology, or are costly to reverse. Follow the process and template in [docs/adr/README.md](docs/adr/README.md). Architectural changes require human approval.

## License

By contributing, you agree that your contributions will be licensed under the repository's [MIT License](LICENSE).
