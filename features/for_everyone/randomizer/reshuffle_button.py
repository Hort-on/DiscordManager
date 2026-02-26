import discord


class ReshuffleView(discord.ui.View):
    def __init__(self, *args, callback, **kwargs):
        super().__init__(timeout=None)
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    @discord.ui.button(
        label='Reshuffle',
        style=discord.ButtonStyle.secondary,
    )
    async def reshuffle(self, interaction: discord.Interaction, _):
        await self.callback(interaction, *self.args, **self.kwargs)
