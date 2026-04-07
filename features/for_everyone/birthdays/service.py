from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from database.db_base_service import DBBaseService

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from general_services.translator.translator import Translator


@dataclass
class BirthdayServiceReturn:
    value: bool
    message: str


class BirthdayService(DBBaseService):
    def __init__(
        self,
        bot: Bot,
        settings: SettingsStorage,
        db_factory: DBFactory,
        translator: Translator,
    ):
        super().__init__(settings=settings)

        self.bot = bot
        self.settings = settings
        self.db_factory = db_factory
        self.translator = translator

    async def save_birthday(
        self, user_id: int, guild_id: int, author_id: int, user_birthday: str
    ) -> BirthdayServiceReturn:
        if not self._is_valid_date(user_birthday):
            message = self.translator.t(
                guild_id=guild_id, section="BIRTHDAYS", key="invalid_date"
            )
            return BirthdayServiceReturn(value=False, message=message)

        exists_scenario = self.db_factory.for_exists_birthday_check(
            guild_id=guild_id, user_id=user_id
        )
        if await exists_scenario.db_proceed():
            message = self.translator.t(
                guild_id=guild_id,
                section="BIRTHDAYS",
                key=(
                    "already_has_b_same_user"
                    if user_id == author_id
                    else "already_has_b"
                ),
            )
            return BirthdayServiceReturn(value=False, message=message)

        add_scenario = self.db_factory.for_add_birthday(
            guild_id=guild_id, user_id=user_id, user_birthday=user_birthday
        )

        result = await self.update_db_and_cache(
            scenario=add_scenario, guild_id=guild_id
        )

        if not result:
            message = self.translator.t(
                guild_id=guild_id, section="SYSTEM_GENERAL", key="error_msg"
            )
            return BirthdayServiceReturn(value=False, message=message)

        message = self.translator.t(
            guild_id=guild_id,
            section="BIRTHDAYS",
            key="success_saved",
            user_birthday=user_birthday,
        )

        return BirthdayServiceReturn(value=True, message=message)

    async def delete_birthday(
        self, user_id: int, guild_id: int, author_id: int
    ) -> BirthdayServiceReturn:
        exists_scenario = self.db_factory.for_exists_birthday_check(
            guild_id=guild_id, user_id=user_id
        )

        if not await exists_scenario.db_proceed():
            message = self.translator.t(
                guild_id=guild_id, section="BIRTHDAYS", key="not_found_user"
            )
            return BirthdayServiceReturn(value=False, message=message)

        delete_scenario = self.db_factory.for_delete_birthday(
            guild_id=guild_id, user_id=user_id
        )

        result = await delete_scenario.db_proceed()

        if not result:
            message = self.translator.t(
                guild_id=guild_id, section="SYSTEM_GENERAL", key="error_msg"
            )
            return BirthdayServiceReturn(value=False, message=message)

        message = self.translator.t(
            guild_id=guild_id,
            section="BIRTHDAYS",
            key="success_del_same_user" if user_id == author_id else "success_del",
        )

        return BirthdayServiceReturn(value=True, message=message)

    @staticmethod
    def _is_valid_date(value: str) -> bool:
        try:
            day, month = map(int, value.split("."))
        except ValueError:
            return False

        days_in_month = {
            1: 31,
            2: 29,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }

        return month in days_in_month and 1 <= day <= days_in_month[month]
