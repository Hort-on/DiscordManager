from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.bot_config import Bot

    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage

    from .services.settings_formatter import SettingsFormatter

from dataclasses import dataclass

from .services.hidden_channels import HiddenChannelsService
from .services.hidden_roles import HiddenRolesService
from .services.system_channels import SystemChannelsService


@dataclass
class EditeSettingsModule:
    hidden_ch_service: HiddenChannelsService
    hidden_roles_service: HiddenRolesService
    system_channels_service: SystemChannelsService
    settings_formatter_service: SettingsFormatter


def build(
        bot: Bot,
        db_factory: DBFactory,
        settings: SettingsStorage,
        formatter: SettingsFormatter,
) -> EditeSettingsModule:

    hidden_ch_service = HiddenChannelsService(
        db_factory=db_factory,
        settings=settings,
        formatter=formatter
    )

    hidden_roles_service = HiddenRolesService(
        db_factory=db_factory,
        settings=settings,
        formatter=formatter
    )

    system_channels_service = SystemChannelsService(
        bot=bot,
        db_factory=db_factory,
        settings=settings,
        formatter=formatter
    )

    settings_formatter_service = SettingsFormatter()

    return EditeSettingsModule(
        hidden_ch_service=hidden_ch_service,
        hidden_roles_service=hidden_roles_service,
        system_channels_service=system_channels_service,
        settings_formatter_service=settings_formatter_service
    )
