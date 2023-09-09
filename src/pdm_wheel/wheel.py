from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Any, Sequence

from pdm import termui
from pdm.cli.actions import check_lockfile, resolve_candidates_from_lockfile
from pdm.cli.commands.base import BaseCommand
from pdm.cli.filters import GroupSelection
from pdm.cli.options import groups_group, lockfile_option
from pdm.cli.utils import check_project_file

try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"

if TYPE_CHECKING:
    import argparse
    from argparse import Namespace

    from pdm.models.candidates import Candidate
    from pdm.models.requirements import Requirement
    from pdm.project.core import Project


class ExportWheelsCommand(BaseCommand):
    """PDM implementation of `pip wheel`
    Build Wheel archives for your requirements and dependencies, from your lockfile.
    """

    description = (
        "PDM implementation of `pip wheel`\nBuild Wheel archives for your requirements and dependencies, from your lockfile.\nProvided by pdm_wheel v"
        + __version__
    )

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        lockfile_option.add_to_parser(parser)
        groups_group.add_to_parser(parser)

        pdm_wheel_group = parser.add_argument_group("Export Wheels Options")
        pdm_wheel_group.add_argument(
            "-w",
            "--wheel-dir",
            dest="wheel_dir",
            metavar="dir",
            default=os.getenv("PDM_WHEEL_DIR"),
            help="Specify the directory to save wheels. Default: ./wheels. [env var: PDM_WHEEL_DIR]",
        )
        pdm_wheel_group.add_argument(
            "--clean",
            dest="clean",
            action="store_true",
            default=False,
            help="Clean the target directory before building.",
        )
        pdm_wheel_group.add_argument(
            "--no-clean",
            dest="clean",
            action="store_false",
            default=False,
            help="Do not clean the target directory before building.",
        )

    def handle(self, project: Project, options: argparse.Namespace) -> None:
        # XXX --force flag to ignore warnings?
        project.core.ui.echo("Checking project file...", err=False)
        check_project_file(project)
        project.core.ui.echo("Checking lockfile...", err=False)
        check_lockfile(project, raise_not_exist=True)

        if not project.lockfile.static_urls:
            project.core.ui.echo(
                "The lockfile does not contain static file URLs. Exporting wheel may be longer than expected, and make calls to indexes.",
                style="warning",
                err=True,
            )
            project.core.ui.echo(
                "Use `pdm lock --refresh --static-urls` to include static file URLs in the lockfile.",
                style="warning",
                err=True,
            )

        project.core.ui.echo("Resolving wheel candidates for this platform...", err=False)
        candidates = self._get_candidates(project, options)

        # Create output directory if it doesn't exist
        wheel_dir = Path(options.wheel_dir) if options.wheel_dir else Path().cwd().joinpath("wheels")

        if not wheel_dir.exists():
            project.core.ui.echo(f"Creating target directory: {wheel_dir}", err=False)
            wheel_dir.mkdir(parents=True, exist_ok=True)
        else:
            project.core.ui.echo(f"Target directory: {wheel_dir}", err=False)

        if not wheel_dir.is_dir():
            raise RuntimeError(f"Wheel target {wheel_dir} is not a directory.")

        # Clean the target directory if the flag is set
        if options.clean:
            project.core.ui.echo("Cleaning target directory.", err=False)
            self._clean_target_directory(wheel_dir)

        build_failures: list[Any] = []

        for candidate in candidates.values():
            candidate.prepare(environment=project.environment)
            assert candidate.prepared
            path = candidate.prepared.build()

            # Copy the wheel to the specified directory
            try:
                rel_path = shutil.copy(path, wheel_dir)
            except OSError as exc:
                project.core.ui.echo(f"Building wheel for {candidate.format()} failed: {exc}", style="error", err=True)
                build_failures.append(candidate)
            else:
                project.core.ui.echo(
                    f"[success]{termui.Emoji.SUCC}[/success] Saved {Path(rel_path).name} for {candidate.format()}"
                )
        project.core.ui.echo(f"\n{termui.Emoji.POPPER} Done exporting wheels!\n", err=False)

        if len(build_failures) > 0:
            project.core.ui.echo(
                f" [error]{termui.Emoji.FAIL} Failed to export [bold]{len(build_failures)}[/bold] wheels: {build_failures}[/error]",
                style="error",
                err=True,
            )
            # XXX Exit with non-zero status code
            msg = f"Failed to export {len(build_failures)} wheels"
            raise RuntimeError(msg)

    def _clean_target_directory(self, wheel_dir: Path, ignore: Sequence[str] | None = None) -> None:
        if not wheel_dir.exists():
            raise RuntimeError(f"Wheel directory {wheel_dir} does not exist.")

        if not wheel_dir.is_dir():
            raise RuntimeError(f"Wheel target {wheel_dir} is not a directory.")

        # If root or system path, raise
        if wheel_dir == Path("/") or wheel_dir == Path("C:\\"):
            raise RuntimeError(f"Cannot clean root or system path {wheel_dir}.")

        if ignore is None:
            ignore = []

        for f_path in os.listdir(wheel_dir):
            if f_path not in ignore:
                Path.unlink(wheel_dir / f_path)
        return

    def _get_candidates(self, project: Project, options: Namespace) -> dict[str, Candidate]:
        selection = GroupSelection.from_options(project, options)
        requirements: dict[str, Requirement] = {}
        for group in selection:
            requirements.update(project.get_dependencies(group=group))

        project.core.ui.echo(
            "The exported wheels are no longer cross-platform. "
            "Using it them other platforms may cause unexpected result.",
            style="warning",
            err=True,
        )
        candidates = resolve_candidates_from_lockfile(project, requirements.values())

        # Remove candidates with [extras] because the bare candidates are already included
        return {name: candidate for name, candidate in candidates.items() if not candidate.req.extras}
