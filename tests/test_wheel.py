import shutil
from pathlib import Path

import pytest
from pdm.core import Core
from pdm.project.core import Project
from pdm.utils import cd


@pytest.fixture(scope="module")
def example_project_no_lock(main):
    tmp_path = Path(__file__).parent / ".testing"
    if tmp_path.exists():
        shutil.rmtree(tmp_path)
    tmp_path.mkdir()
    tmp_path.joinpath("app.py").write_text("import requests\ndef main():\n    print(requests.__version__)\n")
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
                "requires": ["pdm.backend"],
                "build-backend": "pdm.backend",
            },
        }
    )
    project.pyproject.write()

    return project


@pytest.fixture()
def example_project(tmp_path: Path):
    shutil.copy2(Path(__file__).parent / "fixtures" / "pyproject.toml", tmp_path)
    shutil.copy2(Path(__file__).parent / "fixtures" / "pdm.lock", tmp_path)
    core = Core()

    pj = core.create_project(tmp_path)
    pj.global_config._file_data["cache_dir"] = tmp_path / "cache"
    return pj


def test_create_main_error(example_project_no_lock: Project, invoke) -> None:
    # Patch cwd to return the example project root
    with cd(example_project_no_lock.root):
        # Make sure we are pwd is the example project root
        assert Path.cwd().absolute() == example_project_no_lock.root.absolute()

        result = invoke(["wheel"], raising=False, obj=example_project_no_lock)

        # Assert that the command failed
        assert result.exit_code != 0


# Test that locked packages are used
def test_lockfile_matches(example_project: Project):
    with cd(example_project.root):
        # Make sure we are pwd is the example project root
        assert str(Path.cwd().absolute()) == str(example_project.root.absolute())

        example_project.core.main(["wheel"], obj=example_project)

        # Assert that the lockfile matches the expected output
        assert Path(example_project.root, "wheels").exists()

        all_wheels = list(example_project.root.joinpath("wheels").glob("*.whl"))
        # Asset we have the right number of wheels (+/- because of the python version)
        assert len(all_wheels) in [11, 12]

        # XXX Assert that lockfiles entries match the wheels created


# Test --group works

# Test --dev


def test_help(example_project: Project, invoke):
    """Test that the help message is correct."""
    result = invoke(["wheel", "--help"], raising=False, obj=example_project)

    # Assert that the command failed
    assert result.exit_code == 0

    # Assert that the help message is correct
    assert "Build Wheel archives for your requirements and dependencies, from your lockfile." in result.output


# Test default dirpath


# Test command dirpath


def test_clean(example_project: Project, invoke):
    """Test that the help message is correct."""
    example_project.root.joinpath("wheels").mkdir()
    file_to_be_deleted = Path(example_project.root, "wheels", "bad_file.txt")
    file_to_be_deleted.touch()

    with cd(example_project.root):
        result = invoke(["wheel", "--clean"], raising=False, obj=example_project)

    assert result.exit_code == 0
    assert "Cleaning target directory." in result.output
    assert not file_to_be_deleted.exists()
    # Assert directory contains .whl files
    assert len(list(example_project.root.joinpath("wheels").glob("*.whl"))) > 0


def test_running_against_file(example_project: Project, invoke):
    """Test that the help message is correct."""
    wheels_file = example_project.root.joinpath("wheels")
    wheels_file.touch()

    with cd(example_project.root):
        result = invoke(
            ["wheel", "-v", "--clean", "--wheel-dir", wheels_file.resolve().as_posix()],
            raising=False,
            obj=example_project,
        )

    assert result.exit_code == 1
    assert "is not a directory." in str(result.exception) or "is not a directory." in result.stderr
