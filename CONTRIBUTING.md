# Contributing to Git-Mastery CLI App

Thank you for your interest in contributing! This guide covers everything you need to get started.

## Table of Contents

- [Getting Started](#getting-started)
- [Making Changes](#making-changes)
- [Pull Request Etiquette](#pull-request-etiquette)
- [Code Standards](#code-standards)
- [Running Tests](#running-tests)
- [Adding Yourself as a Contributor](#adding-yourself-as-a-contributor)

---

## Getting Started

Before contributing, please:

1. Read the [development setup guide](https://git-mastery.org/developers/docs/getting-started/setup/) — this is the primary reference for setting up your local environment.
2. Check existing [issues](https://github.com/git-mastery/app/issues) and [pull requests](https://github.com/git-mastery/app/pulls) to avoid duplicating work.
3. For non-trivial changes, open an issue first to discuss the approach before writing code.

---

## Making Changes

1. Fork the repository and create a branch from `main`.
2. Make your changes, keeping commits focused and atomic.
3. Ensure all tests pass and code quality checks are clean before opening a PR.
4. Open a pull request against `main`.

> NOTE: Request for the issue to be assigned to you before starting work. This helps avoid duplicate efforts and ensures maintainers are aware of your contribution.

---

## Pull Request Etiquette

- **Keep PRs small and focused.** One logical change per PR makes review faster and easier.
- **Write a clear PR description.** Explain _what_ changed and _why_. Link any related issues.
- **Do not force-push after review has started.** Use new commits for review feedback so reviewers can see what changed.
- **Respond to review comments promptly.** If you disagree with a suggestion, discuss it — don't silently ignore it.

---

## Code Standards

**Before submitting, run:**

```bash
# Type checking
uv run mypy .

# Lint and format
uv run ruff check .
uv run ruff format .
```

Pre-commit hooks are managed by [lefthook](https://github.com/evilmartians/lefthook). If you have it installed, hooks run automatically on commit.

---

## Running Tests

Tests are end-to-end and require a valid `GH_TOKEN` environment variable (a GitHub personal access token).

```bash
# Run all E2E tests
uv run pytest tests/e2e/ -v

# Run a specific test file
uv run pytest tests/e2e/test_foo.py -v
```

CI runs tests on Ubuntu, macOS, and Windows against Python 3.13. Ensure your changes pass on all platforms if they touch platform-specific behaviour.

---

## Adding Yourself as a Contributor

This project uses the [All Contributors](https://allcontributors.org) bot to recognise all types of contributions.

**To add yourself (or someone else) after a merged contribution:**

Comment on any issue or pull request in this repository:

```
@all-contributors please add @<your-github-username> for <contribution-type>
```

For example:

```
@all-contributors please add @<your-github-username> for code, doc
```

The bot will open a pull request updating the contributors list automatically.

**Common contribution types:**

| Type          | Meaning                  |
| ------------- | ------------------------ |
| `code`        | Writing code             |
| `doc`         | Documentation            |
| `bug`         | Reporting bugs           |
| `test`        | Writing tests            |
| `review`      | Reviewing pull requests  |
| `ideas`       | Ideas and planning       |
| `infra`       | Infrastructure and CI/CD |
| `maintenance` | Maintenance tasks        |

For the full list of contribution types, see the [All Contributors emoji key](https://allcontributors.org/docs/en/emoji-key).

> The bot must be installed on the repository. If it does not respond to your comment, contact a maintainer.
