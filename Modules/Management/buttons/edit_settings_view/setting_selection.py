import discord

from Modules.Management.buttons.edit_settings_view.choice_handler.choice_handler import ChoiceHandler
from Modules.Management.buttons.edit_settings_view.option_list.option_list import SETTINGS_OPTIONS


class SettingSelector(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Select a setting to edit...",
            options=[
                discord.SelectOption(label=key.replace("_", " ").title(), value=key)
                for key in SETTINGS_OPTIONS.keys()
            ],
            min_values=1,
            max_values=1
        )

        self.choice_handler = ChoiceHandler()

    async def callback(self, interaction: discord.Interaction):
        selection = self.values[0]

        handler = SETTINGS_OPTIONS.get(selection)

        if handler:
            await self.choice_handler.choice_procedure(interaction, handler, selection)


class SettingSelectorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SettingSelector())
