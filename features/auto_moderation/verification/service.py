from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed
from ui.yes_no_service.yes_no_view import YesNoView

if TYPE_CHECKING:
    from ui.yes_no_service.yes_no_factory import YesNoViewFactory


class VerificationService:
    def __init__(self, settings: SettingsStorage, yes_no_factory: YesNoViewFactory):
        self.settings = settings
        self.yes_no_factory = yes_no_factory
        self.users_count: dict[tuple[int, int], int] = {}

    async def check_the_word(self, guild_id: int, user_id: int, word: str) -> bool:
        if word.lower() != 'hello':
            key = (guild_id, user_id)

            self.users_count[key] = self.users_count.get(key, 0) + 1

            if self.users_count.get(key) >= 2:
                try:
                    await user.kick(reason='has not passed verification')
                except discord.Forbidden:
                    self.users_count.pop(key, None)

            return False

        return True

        await self.assign_role(interaction=interaction)

    async def assign_role(self, guild: discord.Guild, member: discord.Member):
        data = self.settings.dict_storage.for_dict_get(
            'verification_role_id',
            target=StorageTarget.SETTINGS,
            guild_id=guild.id
        )

        verification_role = data.get('verification_role_id')

        if not verification_role:
            error_embed = ErrorEmbed(
                description='Verification role is not assigned yet, please contact with the admins of the server.'
            )
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return

        role = guild.get_role(verification_role)
        await member.add_roles(role)

        success_embed = SuccessEmbed(
            description='Congratulations! Welcome to our community. For additional info, please use "/help"'
        )

        self.users_count.pop((interaction.user.id, interaction.guild_id), None)

        if interaction.response.is_done():
            await interaction.response.edit_message(
                embed=success_embed,
            )
            return

        await interaction.response.send_message(
            embed=success_embed,
            ephemeral=True
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

    async def prepare(self):
        self.bot.add_view(VerificationView(
            settings=self.settings,
            yes_no_factory=self.yes_no_factory
        ))

        for guild in self.bot.guilds:
            data = self.settings.dict_storage.for_dict_get(
                'verification',
                target=StorageTarget.SETTINGS,
                guild_id=guild.id
            )

            verification_channel = self.settings.dict_storage.for_dict_get(
                'verification_channel_id',
                target=StorageTarget.SYSTEM_CHANNELS,
                guild_id=guild.id
            )

            channel_id = verification_channel.get('verification_channel_id')

            if data.get('verification', None) and channel_id is not None:
                channel = guild.get_channel(channel_id)
                if not channel:
                    try:
                        channel = await self.bot.fetch_channel(channel_id)
                    except discord.NotFound:
                        continue

                if isinstance(channel, discord.TextChannel):
                    view = VerificationView(
                        settings=self.settings,
                        yes_no_factory=self.yes_no_factory
                    )

                    await self.ensure_verification_message(channel, view)

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