import discord


class BaseEmbed(discord.Embed):
    def __init__(self, *, title=None, description=None, color=None):
        super().__init__(
            title=title,
            description=description,
            color=color
        )


class SuccessEmbed(BaseEmbed):
    def __init__(self, description: str):
        super().__init__(
            title='✅ Success',
            description=description,
            color=discord.Color.green()
        )


class ErrorEmbed(BaseEmbed):
    def __init__(self, description: str):
        super().__init__(
            title='❌ Error',
            description=description,
            color=discord.Color.red()
        )


class WarningEmbed(BaseEmbed):
    def __init__(self, description: str):
        super().__init__(
            title='⚠️ Warning',
            description=description,
            color=discord.Color.gold()
        )


class InfoEmbed(BaseEmbed):
    def __init__(self, description: str):
        super().__init__(
            title='ℹ️ Info',
            description=description,
            color=discord.Color.blurple()
        )
