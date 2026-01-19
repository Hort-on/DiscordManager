import discord

from datetime import datetime

from core.bot_container import AppContainer
from core.main import BotController

from database.settings_storage.settings_manager import StorageTarget
from database.settings_storage.settings import SettingsStorage

from services.factories.db_factory.db_scenario_factory import DBFactory
from services.utils.messages import BIRTHDAY_MSGS, SYSTEM_MSGS, DB_MSGS, GENERAL_MSGS


class BirthdayManager:
    def __init__(self, bot):
        controller: BotController = AppContainer.get()

        self.bot = bot

        self.settings: SettingsStorage = controller.settings
        self.db_factory: DBFactory = controller.db_factory

    async def add_new_birthday(
            self,
            interaction: discord.Interaction,
            user_id: int,
            guild_id: int,
            user_birthday: str
    ) -> None:

        try:
            datetime.strptime(user_birthday, '%d.%m')
        except ValueError:
            await interaction.edit_original_response(
                content=GENERAL_MSGS.get('invalid_date_msg')
            )
            return

        member = interaction.guild.get_member(user_id)
        if not member:
            await interaction.edit_original_response(
                content=GENERAL_MSGS.get('user_not_found_msg')
            )
            return

        exists_scenario = self.db_factory.for_exists_birthday_check(
            guild_id=guild_id,
            user_id=user_id

        )
        if await exists_scenario.db_proceed():
            await interaction.edit_original_response(
                content=BIRTHDAY_MSGS.get('user_exists_msg').format(member=member.display_name)
            )
            return

        add_scenario = self.db_factory.for_add_birthday(
            guild_id=guild_id,
            user_id=user_id,
            user_birthday=user_birthday
        )

        if await add_scenario.db_proceed():
            await interaction.edit_original_response(
                content=BIRTHDAY_MSGS.get('success_msg').format(
                    member=member.display_name,
                    user_birthday=user_birthday
                )
            )
            return

        await interaction.edit_original_response(
            content=SYSTEM_MSGS.get('failure_msg')
        )

    async def delete_birthday(
            self,
            interaction: discord.Interaction,
            user_id: int,
            guild_id: int
    ) -> None:

        exists_scenario = self.db_factory.for_exists_birthday_check(
            guild_id=guild_id,
            user_id=user_id
        )

        if not await exists_scenario.db_proceed():
            await interaction.edit_original_response(
                content=DB_MSGS.get('user_not_found_msg').format(user_id=user_id)
            )
            return

        delete_scenario = self.db_factory.for_delete_birthday(
            guild_id=guild_id,
            user_id=user_id
        )

        if await delete_scenario.db_proceed():
            await interaction.edit_original_response(
                content=DB_MSGS.get('delete_user_msg').format(user_id=user_id)
            )
            return

        await interaction.edit_original_response(
            content=SYSTEM_MSGS.get('failure_msg')
        )

    async def check_daily_birthday(self) -> None:
        for guild in self.bot.guilds:
            is_enabled = self.settings.dict_storage.for_dict_get(
                target=StorageTarget.SETTINGS,
                guild_id=guild.id,
                key='birthday'
            )

            if not is_enabled:
                continue

            # TODO: зробити точну часову зону для кожної гільдії
            today = datetime.now()
            today_str = today.strftime('%d.%m')

            if today.month == 1 and today.day == 1:
                reset_scenario = self.db_factory.for_reset_congrats()
                await reset_scenario.db_proceed()

            today_birthdays_scenario = self.db_factory.for_get_today_birthday(
                guild_id=guild.id,
                today=today_str
            )

            birthdays = await today_birthdays_scenario.db_proceed()

            if not birthdays:
                continue

            await self.prepare_data(
                guild_id=guild.id,
                today_str=today_str,
                birthdays=birthdays
            )

    async def prepare_data(
            self,
            guild_id: int,
            today_str: str,
            birthdays: list
    ) -> None:

        settings_scenario = self.db_factory.for_get_data(
            guild_id=guild_id,
            table_name='settings',
            *'congrats_channel_id'
        )
        settings = await settings_scenario.db_proceed()

        if not settings:
            return

        channel = self.bot.get_channel(settings.get('congrats_channel_id'))
        if not channel:
            return

        guild = self.bot.get_guild(guild_id)
        if not guild:
            return

        await self.send_congrats(
            guild=guild,
            channel=channel,
            birthdays=birthdays,
            today_str=today_str
        )

    async def send_congrats(
            self,
            guild: discord.Guild,
            channel,
            birthdays: list,
            today_str: str
    ) -> None:

        for user_id_tuple in birthdays:
            user_id = user_id_tuple[0]
            member = guild.get_member(user_id)

            if not member:
                delete_scenario = self.db_factory.for_delete_birthday(
                    guild.id,
                    user_id
                )
                await delete_scenario.db_proceed()
                continue

            message = await channel.send(BIRTHDAY_MSGS.get('congrats_msg') + member.mention)

            await message.add_reaction('🎂')
            await self.update_congrats(guild.id, user_id, today_str)

    async def update_congrats(
            self,
            guild_id: int,
            user_id: int,
            today_str: str
    ) -> None:

        update_scenario = self.db_factory.for_update_last_congrats(
            guild_id=guild_id,
            user_id=user_id,
            today_str=today_str
        )

        await update_scenario.db_proceed()
