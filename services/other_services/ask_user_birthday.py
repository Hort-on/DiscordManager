import discord

from database.settings_storage.settings_manager import StorageTarget

from services.yes_no_service.yes_no_view import YesNoView


class UserBirthdayService:
    def __init__(self, parent):
        self.settings = parent.settings
        self.yes_no_factory = parent.yes_no_factory

    async def check(self, member):
        guild_id = member.guild.id

        data = self.settings.dict_storage.for_dict_get(
            'verification',
            'birthday',
            target=StorageTarget.SETTINGS,
            guild_id=guild_id,
        )

        if not data.get('birthday'):
            return

        if not data.get('verification'):
            scenario = self.yes_no_factory.for_birthday()
            view = YesNoView(
                scenario=scenario
            )
            try:
                await member.send(
                    'Welcome to our community.'
                    ' Would you like to set your birthday? The bot will automatically congrats you.',
                    view=view
                )
            except discord.Forbidden:
                pass
