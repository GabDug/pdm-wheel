from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Sequence

try:
    from check_wheel_contents import __main__ as check_wheel_contents
except ImportError:
    check_wheel_contents = None

if TYPE_CHECKING:
    from pdm.cli.hooks import HookManager
    from pdm.core import Project


def post_build_listener(project: Project, hooks:HookManager, artifacts: Sequence[str], config_settings: dict[str, str] | None, *args, **kwargs):
    """
    This function is connected to the 'post_build' signal and is triggered after the build process.
    It runs the 'check-wheel-contents' command on each artifact.
    """
    if check_wheel_contents is None:
        project.core.ui.echo("check-wheel-contents is not installed. Skipping post-build check.", err=False)
        return

    for artifact in artifacts:
        if artifact.endswith('.whl'):
            project.core.ui.echo(f"Checking contents of {artifact} with check-wheel-contents", err=False)
            # Run check-wheel-contents with the path to the wheel file
            sys.argv = ["", artifact]
            check_wheel_contents.main()
