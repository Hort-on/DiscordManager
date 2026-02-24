from __future__ import annotations

import discord

from dataclasses import dataclass

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from database.db_base_service import DBBaseService


@dataclass
class BirthdayServiceReturn:
    value: bool
    message: str


class BirthdayService(DBBaseService):
    def __init__(self, bot: Bot, settings: SettingsStorage, db_factory: DBFactory):
        super().__init__(settings)

        self.bot = bot
        self.settings = settings
        self.db_factory = db_factory

    async def validate_date(
            self,
            guild: discord.Guild,
            user_id: int,
            birthday: str
    ) -> BirthdayServiceReturn:

        member = guild.get_member(user_id)  # TODO: має бути у flow а не тут

        if member is None:
            return BirthdayServiceReturn(
                value=False,
                message='User not found. Please try again.'
            )

        if not self._is_valid_date(birthday):
            return BirthdayServiceReturn(
                value=False,
                message='Invalid date format. Use DD.MM.'
            )

        return await self.add_birthday(
            user_id=user_id,
            guild_id=guild.id,
            user_birthday=birthday
        )

    async def add_birthday(
            self,
            user_id: int,
            guild_id: int,
            user_birthday: str
    ) -> BirthdayServiceReturn:

        exists_scenario = self.db_factory.for_exists_birthday_check(
            guild_id=guild_id,
            user_id=user_id

        )
        if await exists_scenario.db_proceed():
            return BirthdayServiceReturn(
                value=False,
                message='This user already has his birthday.'
            )

        add_scenario = self.db_factory.for_add_birthday(
            guild_id=guild_id,
            user_id=user_id,
            user_birthday=user_birthday
        )

        result = self.update_db_and_cache(
            scenario=add_scenario,
            guild_id=guild_id
        )

        if not result:
            return BirthdayServiceReturn(
                value=False,
                message='Something went wrong, please try again later.'
            )

        return BirthdayServiceReturn(
            value=True,
            message=f'The user is successfully saved with birthday date: {user_birthday}'
        )

    async def delete_birthday(
            self,
            user_id: int,
            guild_id: int
    ) -> BirthdayServiceReturn:

        exists_scenario = self.db_factory.for_exists_birthday_check(
            guild_id=guild_id,
            user_id=user_id
        )

        if not await exists_scenario.db_proceed():
            return BirthdayServiceReturn(
                value=False,
                message='The user not found, please try again.'
            )

        delete_scenario = self.db_factory.for_delete_birthday(
            guild_id=guild_id,
            user_id=user_id
        )

        result = self.update_db_and_cache(
            scenario=delete_scenario,
            guild_id=guild_id
        )

        if not result:
            return BirthdayServiceReturn(
                value=False,
                message='Something went wrong, please try again later.'
            )

        return BirthdayServiceReturn(
            value=True,
            message='The user was successfully deleted from birthday.'
        )

    @staticmethod
    def _is_valid_date(value: str) -> bool:
        try:
            day, month = map(int, value.split('.'))
        except ValueError:
            return False

        days_in_month = {
            1: 31, 2: 29, 3: 31, 4: 30,
            5: 31, 6: 30, 7: 31, 8: 31,
            9: 30, 10: 31, 11: 30, 12: 31
        }

        return month in days_in_month and 1 <= day <= days_in_month[month]
