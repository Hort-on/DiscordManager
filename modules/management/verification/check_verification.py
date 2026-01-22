import discord

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

from modules.management.verification.view import VerificationView


class CheckVerification:
    def __init__(self, parent):
        self.bot = parent.bot
        self.settings = parent.settings

    async def prepare(self):
        for guild in self.bot.guilds:
            data = self.settings.dict_storage.for_dict_get(
                'verification',
                'verification_channel_id',
                target=StorageTarget.SETTINGS,
                guild_id=guild.id
            )

            channel_id = data.get('verification_channel_id')

            if data.get('verification') and channel_id:
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
