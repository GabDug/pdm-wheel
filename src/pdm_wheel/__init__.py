from __future__ import annotations

from typing import TYPE_CHECKING

from pdm_wheel.wheel import ExportWheelsCommand

if TYPE_CHECKING:
    from pdm.core import Core


def register_pdm_plugin(core: Core) -> None:
    """Register wheel command and post_build hook with PDM."""
    core.register_command(ExportWheelsCommand, "wheel")
