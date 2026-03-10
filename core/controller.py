from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from event_services.member_left import MemberLeftNotification

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from database.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from features.auto_moderation.verification.service import VerificationService
    from features.auto_moderation.verification.view_service import VerificationViewService
    from features.for_admins.send_messages.services.send_rules_service import RulesService
    from features.auto_moderation.message_moderation.module import AutoModModule


class Controller:
    def __init__(
            self,
            bot,
            settings: SettingsStorage,
            db_factory: DBFactory,
            navigator: Navigator,
            verification_service: VerificationService,
            verification_view_service: VerificationViewService,
            rules_service: RulesService,
            moderation_service: AutoModModule
    ):
        self.bot = bot
        self.settings = settings
        self.db_factory = db_factory
        self.navigator = navigator
        self.verification_service = verification_service
        self.verification_view_service = verification_view_service
        self.rules_service = rules_service
        self.moderation_service = moderation_service

        bot.add_listener(self.on_ready)
        bot.add_listener(self.on_message)
        bot.add_listener(self.on_member_remove)
        bot.add_listener(self.on_guild_remove)
        bot.add_listener(self.on_guild_join)

    # --------------------------- EVENTS --------------------------- #
    async def on_ready(self) -> None:
        print(f'Ми приєдналися як {self.bot.user.name}')

        # if not self.daily_birthday_check.is_running():
        #     self.daily_birthday_check.start()
        await self.settings.load_all_guilds_settings()

        await self.verification_view_service.register_persistent_view()
        await self.verification_view_service.ensure_all_guild_messages()

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        if not message.guild:
            await self.rules_service.send_message(
                message=message.content,
                user_id=message.author.id
            )

        await self.moderation_service.moderation_service.process_message(message=message)

    async def on_member_remove(self, member) -> None:
        await MemberLeftNotification(bot=self.bot, settings=self.settings).check_if_notification(member)

    async def on_guild_remove(self, guild: discord.Guild) -> None:
        print(f'Бот від\'єднався від {guild.name}')
        delete_guild_scenario = self.db_factory.for_cleanup_guild(guild.id)
        await delete_guild_scenario.db_proceed()

    async def on_guild_join(self, guild: discord.Guild) -> None:
        print(f'бот приєднався до {guild.name}')
        scenario = self.db_factory.for_init_guild(guild.id)
        await scenario.db_proceed()

    # --------------------------- LOOPS ---------------------------

    # @tasks.loop(hours=24)
    # async def daily_birthday_check(self) -> None:
    #     await self.birthday_manager.check_daily_birthday()
    #
