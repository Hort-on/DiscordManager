from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass

from features.for_everyone.role_manager.services import RoleManagerService

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage


@dataclass
class RoleManagerModule:
    service: RoleManagerService


def build_role_manager_module(settings: SettingsStorage) -> RoleManagerModule:
    service = RoleManagerService(
        settings=settings
    )
    return RoleManagerModule(
        service=service
    )
