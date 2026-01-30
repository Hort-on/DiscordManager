import discord


class BaseScenario:
    async def yes_no_proceed(self, interaction: discord.Interaction, value: bool):
        raise NotImplementedError


class ForBirthdayScenario(BaseScenario):
    async def yes_no_proceed(
            self,
            interaction: discord.Interaction,
            value: bool
    ) -> None:
        if not value:
            return

        await interaction.response.send_modal()
