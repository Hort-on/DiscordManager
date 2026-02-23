from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings_manager import StorageTarget

from features.auto_moderation.verification.modals import AntiBotModal
from features.auto_moderation.verification.view import VerificationView

from ui.embed_constructor.embed_constructor import InfoEmbed, ErrorEmbed, SuccessEmbed, WarningEmbed
from ui.yes_no_service.yes_no_view import YesNoView

if TYPE_CHECKING:
    from core.bot_config import Bot
    from database.settings_storage.settings import SettingsStorage
    from ui.yes_no_service.yes_no_factory import YesNoViewFactory
    from features.auto_moderation.verification.service import VerificationService


class VerificationFlow:
    def __init__(
            self,
            bot: Bot,
            settings: SettingsStorage,
            yes_no_factory: YesNoViewFactory,
            service: VerificationService
    ):
        self.bot = bot
        self.settings = settings
        self.yes_no_factory = yes_no_factory
        self.service = service

    async def agreement_start(self, interaction: discord.Interaction):
        anti_bot = self.settings.dict_storage.for_dict_get(
            'anti_bot',
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id
        )

        if anti_bot:
            await interaction.response.send_modal(AntiBotModal(
                flow=self
            ))
            return

        await self.service.assign_role(
            guild=interaction.guild,
            member=interaction.user
        )

    async def word_verification(self, interaction: discord.Interaction, word: str) -> None:
        await interaction.response.defer(ephemeral=True)

        result_word = await self.service.check_the_word(
            guild_id=interaction.guild_id,
            member=interaction.user,
            word=word
        )

        if not result_word:
            fail_embed = ErrorEmbed(
                description='You wrote the word incorrectly.'
                            ' You have one more attempt.'
                            ' If you fail, you will be kicked off the server'
            )
            await interaction.followup.send(embed=fail_embed)

            return

        result, message = await self.service.assign_role(
            guild=interaction.guild,
            member=interaction.user
        )
        if result:
            embed = SuccessEmbed(
                description=message
            )

            scenario = self.yes_no_factory.for_birthday()
            view = YesNoView(
                scenario=scenario
            )

            try:
                await interaction.user.send(
                    'Welcome to our community.'
                    ' Would you like to set your birthday? The bot will automatically congrats you.',
                    view=view
                )
            except discord.Forbidden:
                pass
        else:
            embed = ErrorEmbed(
                description=message
            )

        await interaction.followup.send(embed=embed)

    @staticmethod
    async def disagreement_start(interaction: discord.Interaction):
        info_embed = InfoEmbed(
            description='You have declined the rules, you will not be given an access to this server,'
                        ' until you agree with the rules.'
        )
        await interaction.response.send_message(
            embed=info_embed,
            ephemeral=True
        )

    async def prepare_verification_channel(self):
        view = VerificationView(
            bot=self.bot,
            settings=self.settings,
            yes_no_factory=self.yes_no_factory,
            service=self.service
        )

        self.bot.add_view(view=view)

        for guild in self.bot.guilds:
            channel = self.service.is_verification_enabled(
                guild=guild
            )

            if isinstance(channel, discord.TextChannel):
                await self.ensure_verification_message(
                    channel=channel,
                    view=view
                )

    async def ensure_verification_message(self, channel, view):
        found = False
        async for message in channel.history(limit=25):
            if message.author == self.bot.user and message.components:
                found = True
                break

        if not found:
            embed = WarningEmbed(
                description='Please before you agree make sure you have carefully read the rules.'
            )

            await channel.send(embed=embed, view=view)
