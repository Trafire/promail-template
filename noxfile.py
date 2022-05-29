"""Nox sessions."""
import os
import tempfile
from typing import Any, IO

import nox
from nox import Session

locations = "src", "tests", "noxfile.py", "docs/conf.py"


def install_with_constraints(session: Session, *args: str, **kwargs: str) -> None:
    """Install packages constrained by Poetry's lock file."""
    with CustomNamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


nox.options.sessions = (
    "lint",
    "tests",
    "safety",
    "mypy",
)


@nox.session(python=["3.8"])
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    install_with_constraints(
        session,
        "black",
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
    )
    session.run("black", *locations)
    session.run("flake8", *args)


@nox.session(python=["3.8"])
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs or ["--cov", "-m", "not e2e"]

    session.run("poetry", "install", external=True)

    install_with_constraints(
        session, "coverage[toml]", "pytest", "pytest-cov", "pytest-mock"
    )
    session.run("pytest", *args)


@nox.session(python="3.8")
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python="3.8")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    with CustomNamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install("safety")
        session.run(
            "safety",
            "check",
            f"--file={requirements.name}",
            "--full-report",
            external=True,
        )


@nox.session(python=["3.10"])
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    install_with_constraints(session, "mypy", "--verbose")
    session.run("mypy", *args)


@nox.session(python="3.8")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "docs/_build")

@nox.session(python="3.8")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    install_with_constraints(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)



@nox.session(python=["3.8"])
def poetry_update(session: Session) -> None:
    """Update Lock File."""
    session.run("poetry", "update", external=True)


class CustomNamedTemporaryFile:
    """Alternative Temp file to allow compatibility with windows.

    This custom implementation is needed because of the following limitation of
    tempfile.NamedTemporaryFile:

    > Whether the name can be used to open the file a second time,
    while the named temporary file is still open,
    > varies across platforms (it can be so used on Unix;
     it cannot on Windows NT or later).

    """

    def __init__(self, mode: str = "wb", delete: bool = True) -> None:
        """Initiates CustomNamedTemporaryFile."""
        self._mode = mode
        self._delete = delete

    def __enter__(self) -> IO[Any]:
        """Creates and opens temp file."""
        # Generate a random temporary file name
        file_name = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
        # Ensure the file is created
        open(file_name, "x").close()
        # Open the file in the given mode
        self._tempFile = open(file_name, self._mode)
        return self._tempFile

    def __exit__(self, *args: tuple, **kwargs: dict) -> None:
        """Closes temp file."""
        self._tempFile.close()
