import re
import sys
from typing import List, Optional

from app.utils.click import error, get_verbose
from app.utils.command import run


def run_command(
    command: List[str], env: dict = {}, exit_on_error: bool = False
) -> None:
    result = run(command, env)
    if not result.is_success() and exit_on_error:
        if get_verbose():
            error_msg = f"Command failed: {' '.join(command)}\n" + "\n".join(
                f"    {line}" for line in result.stderr.splitlines()
            )
        else:
            error_msg = (
                f"Command failed: {' '.join(command)}\n"
                f"    Run with --verbose to see full output."
            )
        error(error_msg)
        sys.exit(result.returncode)


def is_github_cli_installed() -> bool:
    # If git is not installed yet, we should expect a 127 exit code
    # 127 indicating that the command not found: https://stackoverflow.com/questions/1763156/127-return-code-from
    result = run(["gh", "--version"])
    return result.is_success()


def get_https_or_ssh() -> Optional[str]:
    result = run(["gh", "auth", "status"], {"GH_PAGER": "cat"})
    if result.is_success():
        regex = re.compile(r"Git operations protocol: (\w+)")
        match = regex.search(result.stdout)
        if match:
            protocol = match.group(1).lower()
            return protocol
    return None


def get_token_scopes() -> List[str]:
    result = run(["gh", "auth", "status"], {"GH_PAGER": "cat"})
    if result.is_success():
        regex = re.compile(r"Scopes:\s*(.+)", re.IGNORECASE)
        match = regex.search(result.stdout)
        if match:
            scopes_str = match.group(1).strip()
            scopes = re.split(r"[,\s]+", scopes_str)
            scopes = [s.strip().strip("'").lower() for s in scopes if s.strip()]
            return scopes
    return []


def has_delete_repo_scope() -> bool:
    return "delete_repo" in get_token_scopes()


def is_authenticated() -> bool:
    return run(["gh", "auth", "status"]).is_success()


def has_fork(fork_name: str) -> bool:
    result = run(
        ["gh", "repo", "view", fork_name, "--json", "isFork", "--jq", ".isFork"],
        env={"GH_PAGER": "cat"},
    )
    return result.is_success() and result.stdout == "true"


def get_repo_ssh_url(repo: str) -> Optional[str]:
    result = run(
        ["gh", "repo", "view", repo, "--json", "sshUrl", "--jq", ".sshUrl"],
        env={"GH_PAGER": "cat"},
    )
    if result.is_success():
        return result.stdout
    return None


def get_repo_https_url(repo: str) -> Optional[str]:
    result = run(
        ["gh", "repo", "view", repo, "--json", "url", "--jq", ".url"],
        env={"GH_PAGER": "cat"},
    )
    if result.is_success():
        return result.stdout + ".git"
    return None


def fork(
    repository_name: str,
    fork_name: str,
    all_branches: bool | None = False,
    exit_on_error: bool = False,
) -> None:
    fork_command = [
        "gh",
        "repo",
        "fork",
        repository_name,
        "--fork-name",
        fork_name,
    ]
    if all_branches is None or not all_branches:
        fork_command.append("--default-branch-only")
    run_command(fork_command, exit_on_error=exit_on_error)


def clone(repository_name: str, exit_on_error: bool = False) -> None:
    run_command(["gh", "repo", "clone", repository_name], exit_on_error=exit_on_error)


def clone_with_custom_name(
    repository_name: str, name: str, exit_on_error: bool = False
) -> None:
    run_command(
        ["gh", "repo", "clone", repository_name, name], exit_on_error=exit_on_error
    )


def delete_repo(repository_name: str, exit_on_error: bool = False) -> None:
    run_command(
        ["gh", "repo", "delete", repository_name, "--yes"], exit_on_error=exit_on_error
    )


def pull_request(
    repo: str, base: str, head: str, title: str, body: str, exit_on_error: bool = False
) -> None:
    run_command(
        [
            "gh",
            "pr",
            "create",
            "--repo",
            repo,
            "--base",
            base,
            "--head",
            head,
            "--title",
            title,
            "--body",
            body,
        ],
        exit_on_error=exit_on_error,
    )


def get_prs(repo: str, head: str, owner: str) -> List[str]:
    result = run(
        [
            "gh",
            "pr",
            "list",
            "--repo",
            repo,
            "--author",
            "@me",
            "--head",
            head,
            "--json",
            "headRepositoryOwner",
            "--json",
            "url",
            "-q",
            f'.[] | select ( .headRepositoryOwner.login == "{owner}" ) | .url',
        ],
        env={"GH_PAGER": "cat"},
    )

    if result.is_success():
        prs = result.stdout.splitlines()
        return prs
    return []


def get_username() -> str:
    result = run(["gh", "api", "user", "-q", ".login"])

    if result.is_success():
        username = result.stdout.splitlines()[0]
        return username
    return ""


def get_user_orgs() -> List[str]:
    result = run(
        [
            "gh",
            "api",
            "-H",
            "Accept: application/vnd.github+json",
            "/user/orgs",
            "--jq",
            ".[].login",
            "--paginate",
        ],
    )
    if result.is_success():
        org_names = result.stdout.splitlines()
        return org_names
    return []


def get_user_prs(repo: str, owner: str) -> List[str]:
    result = run(
        [
            "gh",
            "pr",
            "list",
            "--repo",
            repo,
            "--author",
            "@me",
            "--head",
            "submission",
            "--json",
            "headRepositoryOwner",
            "--json",
            "url",
            "-q",
            f'.[] | select ( .headRepositoryOwner.login == "{owner}" ) | .url',
        ],
        env={"GH_PAGER": "cat"},
    )
    if result.is_success():
        prs = result.stdout.splitlines()
        return prs
    return []


def close_prs(repo: str) -> None:
    """Close all open pull requests authored by the current user in `repo`."""

    result = run(
        [
            "gh",
            "pr",
            "list",
            "--repo",
            repo,
            "--author",
            "@me",
            "--state",
            "open",
            "--json",
            "number",
            "--jq",
            ".[].number",
        ],
        env={"GH_PAGER": "cat"},
    )

    if not result.is_success():
        return

    for pr_number in result.stdout.splitlines():
        run(
            [
                "gh",
                "pr",
                "close",
                pr_number,
                "--repo",
                repo,
            ],
            env={"GH_PAGER": "cat"},
        )
