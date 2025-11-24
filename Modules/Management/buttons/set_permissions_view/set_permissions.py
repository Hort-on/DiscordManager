import discord

from Modules.Management.getting_channel import ChannelTypeView


class SetPermissionButton(discord.ui.Button):
    def __init__(self, ctx):
        super().__init__(
            label='Set permissions',
            style=discord.ButtonStyle.blurple
        )
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        view = ChannelTypeView(self.ctx)

        await interaction.response.send_message(
            'Please select the type of channel:',
            view=view,
            ephemeral=True,
            delete_after=600
        )
