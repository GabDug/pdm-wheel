from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from pdm.cli.actions import resolve_candidates_from_lockfile
from pdm.cli.commands.base import BaseCommand
from pdm.cli.options import groups_group, lockfile_option
from pdm.cli.utils import check_project_file, translate_groups

if TYPE_CHECKING:
    import argparse

    from pdm.models.requirements import Requirement
    from pdm.project.core import Project


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
            dest="wheel_dir",
            metavar="dir",
            default=os.curdir,
            help="Specify the directory to save wheels, where the default is the current directory",
        )

    def handle(self, project: Project, options: argparse.Namespace) -> None:
        check_project_file(project)

        project.environment.get_working_set()
        groups: list[str] = list(options.groups)

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
        wheel_dir = Path(options.wheel_dir)
        wheel_dir.mkdir(parents=True, exist_ok=True)

        build_failures = []

        for candidate_name, candidate in candidates.items():
            project.core.ui.echo(f"Building wheel for {candidate_name} {candidate.version}... ",  err=False)

            environment = project.environment
            prepared_candidate = candidate.prepare(environment=environment)

            path = prepared_candidate.build()

            # Copy the wheel to the specified directory
            try:
                rel_path = shutil.copy(path, wheel_dir)
            except OSError as e:
                project.core.ui.echo(
                    f"Building wheel for {candidate_name} failed: {e}",
                    err=True,
                )
                # build_failures.append(req)
            else:
                project.core.ui.echo(f"Saved ./{rel_path}", err=False)

        if len(build_failures) > 0:
            project.core.ui.echo(
                f"Failed to build {len(build_failures)} wheels: {build_failures}",
                style="error",
                err=True,
            )
            raise RuntimeError("Failed to build wheels")
