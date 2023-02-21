# Do not push commits that begin with "WIP"
from __future__ import annotations

#from argparse import ArgumentParser
import subprocess, os, sys
from typing import TYPE_CHECKING, TypeVar

STDERR = sys.stderr

if TYPE_CHECKING:
    from typing import Any, Optional
    T = TypeVar('T')

def printf(fmt: str, *args: Any, **kw) -> None:
    """
    Print a string with fields specified in *ARGS.

    Keyword arguments are the same as for print().
    """
    print(fmt % args, **kw)

def getenv(key: str, /, default: Optional[T]=None, typ: Optional[type]=None) -> T | Any:
    """Get a value from the environment, or return DEFAULT."""
    env = os.getenv(key)
    if env is None:
        return default

    if env is not None:
        if isinstance(env, str) and typ is not None:
            return typ(env)
    return env

def _missing_env(name: str) -> bool:
    import logging

    code = name == ''
    if code:
        logging.error("missing variable: %s", name)

    return code

def bash_command(cmd: str, **kw):
    cmdl = ['bash', '-c', cmd]
    return subprocess.run(cmdl, **kw)

def main () -> int:
    import functools, logging

    bashcmdcapout = functools.partial(
        bash_command,
        capture_output=True,
        text=True
    )

    cp = bashcmdcapout('git hash-object --stdin </dev/null', check=True)
    zeroes = '0' * len(cp.stdout.rstrip())

    remote_rev = getenv('PRE_COMMIT_FROM_REF', '')
    if _missing_env('PRE_COMMIT_FROM_REF'): return 1

    local_rev = getenv('PRE_COMMIT_TO_REF', '')
    if _missing_env('PRE_COMMIT_TO_REF'): return 1

    remote_branch = getenv('PRE_COMMIT_REMOTE_BRANCH', '')
    if _missing_env('PRE_COMMIT_REMOTE_BRANCH'): return 1

    local_branch = getenv('PRE_COMMIT_LOCAL_BRANCH', '')
    if _missing_env('PRE_COMMIT_LOCAL_BRANCH'): return 1

    if local_rev == zeroes:
        # Handle delete
        pass
    else:
        if remote_rev == zeroes:
            # New branch, examine all commits
            rng = local_rev
        else:
            # Update to existing branch, examine new commits
            rng = f"{remote_rev}..{local_rev}"

        # Check for WIP commit
        cp = bashcmdcapout(f"git rev-list -n 1 --grep '^WIP' {rng}")

        if cp.stdout.rstrip():
            printf("Found WIP commit in %s, not pushing", local_branch, file=STDERR)
            return 1

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
