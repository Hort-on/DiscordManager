import discord

from Modules.Management.getting_channel import ChannelTypeView


class SendMessageButton(discord.ui.Button):
    def __init__(self, ctx):
        super().__init__(
            label='Send message',
            style=discord.ButtonStyle.blurple
        )
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        try:
            view = ChannelTypeView(self.ctx, text_only=True)
            await interaction.user.send('```Please select the channel where the messages will be sent.:```',
                                        view=view)

            await interaction.response.send_message('```Please check your private messages to select a channel.```',
                                                    ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                '```Failed to send a message to your private messages. Please check your privacy settings.```',
                ephemeral=True)
