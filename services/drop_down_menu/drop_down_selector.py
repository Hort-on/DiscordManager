import discord


class UniversalSelect(discord.ui.Select):
    def __init__(
        self,
        *,
        placeholder: str,
        options: list[discord.SelectOption],
        min_values: int = 1,
        max_values: int = 1,
        on_select: callable
    ):
        super().__init__(
            placeholder=placeholder,
            options=options,
            min_values=min_values,
            max_values=max_values
        )
        self._on_select = on_select

    async def callback(self, interaction: discord.Interaction):
        await self._on_select(interaction, self.values)
