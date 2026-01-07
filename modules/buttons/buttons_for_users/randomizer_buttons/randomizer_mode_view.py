import discord


class RandomizerModeView(discord.ui.View):
    # TODO: цю кнопку потрібно зробити максимально гнучкою і з modal
    @discord.ui.button(
        label='Regular random',
        style=discord.ButtonStyle.success
    )
    async def random_users(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ) -> None:
        await interaction.edit_original_response(
            content='Please',
        )

    @discord.ui.button(
        label="Random teams",
        style=discord.ButtonStyle.secondary
    )
    async def random_teams(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ) -> None:
        await interaction.edit_original_response(
            content="🎯 Random users selected",
        )
