"""
Nox test script. Requires `nox uv` to be installed.
"""

from collections.abc import Generator

import nox

coverage_html = "/tmp/django-actual-admin-docs-htmlcov"  # noqa:  S108 Probable insecure usage of temporary file

# Python: [Django, Django] Version Testmatrix
python_django = {
    "3.9": ["3.2", "4.0", "4.1", "4.2"],
    "3.10": ["3.2", "4.0", "4.1", "4.2"],
    "3.11": ["3.2", "4.0", "4.1", "4.2", "5.0", "5.1"],
    "3.12": ["3.2", "4.0", "4.1", "4.2", "5.0", "5.1"],
    "3.13": ["4.2", "5.0", "5.1"],
}


def testmatrix(matrix: dict[str, list[str]]) -> Generator[tuple[str, str]]:
    """
    Expand above testmatrix to individual items.

    ("3.13", "4.2.*"),
    ("3.13", "5.0.*"),
    ("3.13", "5.1.*"),
    ...
    """
    for python, djangos in matrix.items():
        for django in djangos:
            yield python, f"{django}.*"


@nox.session(venv_backend="uv")
@nox.parametrize("python,django", testmatrix(python_django))
@nox.parametrize("poetry_arg", ["--with highlight", "--without highlight"])
def pytest(session: nox.Session, django: str, poetry_arg: str) -> None:
    session.install("poetry")
    session.run("poetry", "install", "--with", "test", *poetry_arg.split())
    session.run("uv", "pip", "install", f"django=={django}")
    session.run(
        "pytest",
        "--cov-append",
        "actual_admin_docs",
    )
    session.notify("coverage")


@nox.session
def lint(session: nox.Session) -> None:
    session.install("ruff")
    session.run("ruff", "check", "actual_admin_docs")
    session.run("ruff", "format", "--check", "actual_admin_docs")


@nox.session
def coverage(session: nox.Session) -> None:
    session.install("coverage")
    session.run("coverage", "html", "-d", coverage_html)
