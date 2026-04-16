from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import discord

from database.db_base_service import DBBaseService
from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from general_services.translator.translator import Translator


class BirthdayManager(DBBaseService):
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

    async def check_daily_birthday(self) -> None:
        for guild in self.bot.guilds:
            is_enabled = self.settings.dict_storage.get_value(
                key="birthday", target=StorageTarget.SETTINGS, guild_id=guild.id
            )

            if not is_enabled:
                continue

            today = datetime.now()
            today_str = today.strftime("%d.%m")

            if today.month == 1 and today.day == 1:
                reset_scenario = self.db_factory.for_reset_congrats()
                await reset_scenario.db_proceed()

            today_birthdays_scenario = self.db_factory.for_get_today_birthday(
                guild_id=guild.id, today=today_str
            )

            birthdays = await today_birthdays_scenario.db_proceed()

            if not birthdays:
                continue

            await self.prepare_data(
                guild_id=guild.id, today_str=today_str, birthdays=birthdays
            )

    async def prepare_data(
        self, guild_id: int, today_str: str, birthdays: list
    ) -> None:
        settings_scenario = self.db_factory.for_get_data(
            guild_id=guild_id, table_name="settings", *"congrats_channel_id"
        )
        settings = await settings_scenario.db_proceed()

        if not settings:
            return

        channel = self.bot.get_channel(settings.get("congrats_channel_id"))
        if not isinstance(channel, (discord.TextChannel, discord.Thread)):
            return

        guild = self.bot.get_guild(guild_id)
        if not guild:
            return

        await self.send_congrats(
            guild=guild, channel=channel, birthdays=birthdays, today_str=today_str
        )

    async def send_congrats(
        self,
        guild: discord.Guild,
        channel: discord.TextChannel | discord.Thread,
        birthdays: list,
        today_str: str,
    ) -> None:
        members = []

        for user_id in birthdays:
            member = guild.get_member(user_id)

            if not member:
                delete_scenario = self.db_factory.for_delete_birthday(
                    guild_id=guild.id, user_id=user_id
                )
                await delete_scenario.db_proceed()
                continue

            members.append(member)

        if not members:
            return

        mentions = " ".join(member.mention for member in members)

        names = ", ".join(member.display_name for member in members)

        congrats_msg = self.translator.t(
            guild_id=guild.id,
            section="BIRTHDAYS",
            key="congrats",
            names=names,
        )

        message = await channel.send(f"{mentions}\n```{congrats_msg}```")

        await message.add_reaction("🎂")
        await message.add_reaction("🎉")
        await message.add_reaction("❤️")

        for member in members:
            await self.update_congrats(
                guild_id=guild.id,
                user_id=member.id,
                today_str=today_str,
            )

    async def update_congrats(
        self, guild_id: int, user_id: int, today_str: str
    ) -> None:
        update_scenario = self.db_factory.for_update_last_congrats(
            guild_id=guild_id, user_id=user_id, today_str=today_str
        )

        await update_scenario.db_proceed()
