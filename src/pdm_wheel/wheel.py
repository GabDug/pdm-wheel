from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse

    from pdm.models.requirements import Requirement
    from pdm.project.core import Project

from pathlib import Path

from pdm.cli.actions import resolve_candidates_from_lockfile
from pdm.cli.commands.base import BaseCommand
from pdm.cli.options import groups_group, lockfile_option
from pdm.cli.utils import check_project_file, translate_groups


class WheelCommand(BaseCommand):
    """PDM implementation of `pip wheel`
    Build Wheel archives for your requirements and dependencies.
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        lockfile_option.add_to_parser(parser)
        groups_group.add_to_parser(parser)
        parser.add_argument(
            "-w",
            "--wheel-dir",
            help="Specify the directory to save wheels, where the default is the current directory",
        )

    def handle(self, project: Project, options: argparse.Namespace) -> None:
        check_project_file(project)

        project.environment.get_working_set()
        groups: list[str] = list(options.groups)
        # if options.pyproject:
        #     options.hashes = False
        groups = translate_groups(
            project,
            options.default,
            options.dev,
            options.groups or (),
        )
        requirements: dict[str, Requirement] = {}
        for group in groups:
            requirements.update(project.get_dependencies(group))

        project.core.ui.echo(
            "The exported wheels are no longer cross-platform. "
            "Using it on other platforms may cause unexpected result.",
            style="warning",
            err=True,
        )
        candidates = resolve_candidates_from_lockfile(project, requirements.values())
        # Remove candidates with [extras] because the bare candidates are already
        # included
        (candidate for candidate in candidates.values() if not candidate.req.extras)
        # Create output directory if it doesn't exist
        if options.wheel_dir:
            wheel_dir = Path(options.wheel_dir)
            wheel_dir.mkdir(parents=True, exist_ok=True)
        else:
            wheel_dir = Path.cwd()

        for candidate in candidates.values():
            environment = project.environment
            prepared_candidate = candidate.prepare(environment=environment)

            path = prepared_candidate.build()

            # Move the wheel to the specified directory
            try:
                rel_path = path.rename(wheel_dir / path.name)
            except FileExistsError:
                pass
            else:
                project.core.ui.echo(f"Saved ./{rel_path}", err=False)
