import discord

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget
from modules.buttons.verification_buttons.view import VerificationView


class CheckVerification:
    def __init__(self, bot, settings: SettingsStorage):
        self.bot = bot
        self.settings = settings

    async def prepare(self):
        for guild in self.bot.guilds:
            verf_enabled = self.settings.dict_storage.for_dict_get(
                target=StorageTarget.SETTINGS,
                guild_id=guild.id,
                key='verification'
            )
            channel_id = self.settings.dict_storage.for_dict_get(
                target=StorageTarget.SETTINGS,
                guild_id=guild.id,
                key='verification_channel_id'
            )

            if verf_enabled and channel_id:
                channel = guild.get_channel(channel_id)
                if not channel:
                    try:
                        channel = await self.bot.fetch_channel(channel_id)
                    except discord.NotFound:
                        continue

                if isinstance(channel, discord.TextChannel):
                    view = VerificationView()

                    await self.ensure_verification_message(channel, view)

    async def ensure_verification_message(self, channel, view):
        found = False
        async for message in channel.history(limit=25):
            if message.author == self.bot.user and message.components:
                found = True
                break

        if not found:
            await channel.send(
                content='```Please read the rules and confirm your agreement:```',
                view=view
            )
