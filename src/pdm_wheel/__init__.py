from __future__ import annotations

from typing import TYPE_CHECKING

from pdm.signals import post_build

from pdm_wheel.check_built_wheel import post_build_listener
from pdm_wheel.wheel import ExportWheelsCommand

if TYPE_CHECKING:
    from pdm.core import Core



def wheel_plugin(core: Core) -> None:
    """Register wheel command and post_build hook with PDM."""
    core.register_command(ExportWheelsCommand, "wheel")
    post_build.connect(post_build_listener)
