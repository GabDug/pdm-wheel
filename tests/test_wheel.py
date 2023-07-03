import os
import shutil
import stat
import subprocess
import sys
import zipfile
from pathlib import Path
from unittest.mock import patch

import pytest
from pdm.core import Core
from pdm.project.core import Project
from pdm.utils import cd


@pytest.fixture(scope="module")
def example_project_no_lock(invoke, main):
    tmp_path = Path(__file__).parent / ".testing"
    if tmp_path.exists():
        shutil.rmtree(tmp_path)
    tmp_path.mkdir()
    tmp_path.joinpath("app.py").write_text(
        "import requests\ndef main():\n    print(requests.__version__)\n"
    )
    project: Project = main.create_project(tmp_path)
    project.pyproject.set_data(
        {
            "project": {
                "name": "test_app",
                "version": "0.1.0",
                "requires-python": ">=3.7",
                "dependencies": ["requests==2.24.0"],
            },
            "build-system": {
                "requires": ["pdm-pep517"],
                "build-backend": "pdm.pep517.api",
            },
        }
    )
    project.pyproject.write()

    return project


@pytest.fixture()
# @pytest.fixture(scope="module")
def example_project(tmp_path: Path):
    # Load project from` fixtures`
    # project = main.create_project()
    # return project

    # @pytest.fixture()
    # def tmp_project(tmp_path: Path) -> Project:
    shutil.copy2(Path(__file__).parent / "fixtures" / "pyproject.toml", tmp_path)
    shutil.copy2(Path(__file__).parent / "fixtures" / "pdm.lock", tmp_path)
    core = Core()
    return core.create_project(tmp_path)


def test_create_main_error(example_project_no_lock: Project, invoke)->None:
    # Patch os.getcwd() to return the example project root
    with cd(example_project_no_lock.root), patch(
        "os.getcwd", return_value=example_project_no_lock.root
    ):
        # Make sure we are pwd is the example project root
        assert os.getcwd() == example_project_no_lock.root

        result = invoke(["wheel"], raising=False, obj=example_project_no_lock)

        # Assert that the command failed
        assert result.exit_code != 0


# Test that locked packages are used
def test_lockfile_matches(example_project: Project, invoke):
    with cd(example_project.root), patch(
        "os.getcwd", return_value=example_project.root
    ):
        # Make sure we are pwd is the example project root
        assert os.getcwd() == example_project.root
        print(os.getcwd())
        example_project.core.main(["wheel"], obj=example_project)

        # raise Exception("Not implemented")

        # Assert that the lockfile matches the expected output
        assert Path(example_project.root, "wheels").exists()

        # Assert that lockfiles entries match the wheels created

        # Assert we have exactly the rught number of wheels


# Test --group works

# Test --dev


# test thats --helps works
def test_help(example_project: Project, invoke):
    """Test that the help message is correct."""

    result = invoke(["wheel", "--help"], raising=False, obj=example_project)

    # Assert that the command failed
    assert result.exit_code == 0

    # Assert that the help message is correct
    assert (
        "Build Wheel archives for your requirements and dependencies, from your lockfile."
        in result.output
    )


# Test default dirpath


# Test command dirpath
