import os
from pathlib import Path

import pytest
from pdm_wheel import ExportWheelsCommand


class TestCleanTargetDirectory:
    # Test case for the case where wheel_dir does not exist
    def test_wheel_dir_not_exists(self, tmp_path):
        command = ExportWheelsCommand()
        tmp_path = tmp_path / "does_not_exist"
        with pytest.raises(RuntimeError):
            command._clean_target_directory(tmp_path)

    # Test case for the case where wheel_dir is not a directory
    def test_wheel_dir_not_a_directory(self, tmp_path: Path):
        command = ExportWheelsCommand()
        temp_file = tmp_path / "temp_file.txt"
        temp_file.touch(exist_ok=True)
        with pytest.raises(RuntimeError):
            command._clean_target_directory(temp_file)

    # Test case for the case where wheel_dir is root or system path
    def test_wheel_dir_is_root_or_system_path(self):
        command = ExportWheelsCommand()
        with pytest.raises(RuntimeError):
            command._clean_target_directory(Path("/"))
        with pytest.raises(RuntimeError):
            command._clean_target_directory(Path("C:\\"))

    # Test case for the case where ignore list is provided
    def test_ignore_list_provided(self, tmp_path: Path):
        command = ExportWheelsCommand()
        ignore_list = ["file1.txt", "file2.txt"]
        for file_name in ignore_list:
            (tmp_path / file_name).touch()
        tmp_path.joinpath("file3.txt").touch()

        command._clean_target_directory(tmp_path, ignore=ignore_list)

        # Check that only files in the ignore list are not deleted
        for file_name in ignore_list:
            assert (tmp_path / file_name).exists()
        # Check that other files are deleted
        for file_name in os.listdir(tmp_path):
            if file_name not in ignore_list:
                assert not (tmp_path / file_name).exists()
        # Check the number of files in the directory
        assert len(os.listdir(tmp_path)) == len(ignore_list)

    # Test case for the case where ignore list is not provided
    def test_ignore_list_not_provided(self, tmp_path: Path):
        command = ExportWheelsCommand()
        temp_file = tmp_path / "temp_file.txt"
        temp_file.touch()

        command._clean_target_directory(tmp_path)

        assert tmp_path.exists()
        assert not temp_file.exists()
