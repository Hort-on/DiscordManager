import discord

from modules.buttons.buttons_for_admins.edit_settings_button.service.choice_handler import ChoiceHandler
from utils.option_list import SETTINGS_OPTIONS


class SettingSelector(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Please select a setting to edit...",
            options=[
                discord.SelectOption(label=key.replace("_", " ").title(), value=key)
                for key in SETTINGS_OPTIONS.keys()
            ],
            min_values=1,
            max_values=1
        )

        self.choice_handler = ChoiceHandler()

    async def callback(self, interaction: discord.Interaction) -> None:
        config_key = self.values[0]

        option_type = SETTINGS_OPTIONS.get(config_key)

        if option_type:
            await self.choice_handler.choice_procedure(interaction, option_type, config_key)
        else:
            await interaction.edit_original_response(content='Oops something went wrong, please try again later.')


class SettingSelectorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SettingSelector())
