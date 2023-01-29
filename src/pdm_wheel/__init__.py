from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pdm.core import Core

from pdm_wheel.wheel import WheelCommand


def wheel_plugin(core: Core) -> None:
    core.register_command(WheelCommand, "wheel")
    core.register_command(WheelCommand, "wheel")
