import discord


class BaseEmbed(discord.Embed):
    def __init__(self, *, title=None, description=None, color=None):
        super().__init__(
            title=title,
            description=description,
            color=color
        )
        # self.set_footer(text='Assistant')
