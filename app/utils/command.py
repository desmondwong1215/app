import logging
import os
import subprocess
from dataclasses import dataclass
from subprocess import CalledProcessError, CompletedProcess
from typing import Dict

from typing_extensions import List

from app.utils.click import get_verbose


@dataclass
class CommandResult:
    result: CompletedProcess[str]

    def is_success(self) -> bool:
        return self.result.returncode == 0

    @property
    def stdout(self) -> str:
        return self.result.stdout.strip()

    @property
    def stderr(self) -> str:
        return self.result.stderr.strip()

    @property
    def returncode(self) -> int:
        return self.result.returncode


def run(command: List[str], env: Dict[str, str] = {}) -> CommandResult:
    verbose = get_verbose()
    logger = logging.getLogger(__name__)
    logger.info("Running command: %s", command)

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            env=dict(os.environ, **env),
            encoding="utf-8",
            check=True,
        )
    except FileNotFoundError:
        error_msg = f"Command not found: {command[0]}"
        result = CompletedProcess(command, returncode=127, stdout="", stderr=error_msg)
    except PermissionError:
        error_msg = f"Permission denied: {command[0]}"
        result = CompletedProcess(command, returncode=126, stdout="", stderr=error_msg)
    except OSError as e:
        error_msg = f"OS error when running command {command}: {e}"
        result = CompletedProcess(command, returncode=1, stdout="", stderr=error_msg)
    except CalledProcessError as e:
        result = CompletedProcess(
            command, returncode=e.returncode, stdout="", stderr=e.stderr
        )

    if env:
        logger.info("Env: %s", env)

    if result.returncode != 0:
        logger.error(result.stderr)
        print("\t" + result.stderr)
    elif verbose:
        logger.info(result.stdout)
        print("\t" + result.stdout)

    return CommandResult(result=result)
