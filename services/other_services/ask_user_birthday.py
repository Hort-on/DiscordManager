import discord

from database.settings_storage.settings_manager import StorageTarget

from services.yes_no_view.view.yes_no import YesNoView
from services.yes_no_view.yes_no_view_factory.yes_no_factory import YesNoViewFactory


class UserBirthdayService:
    def __init__(self, parent):
        self.settings = parent.settings

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
            scenario = YesNoViewFactory.for_birthday()
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
