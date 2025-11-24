import discord
from Modules.Birthdays.birthday import Birthday


class AddBirthdayButton(discord.ui.Button):
    def __init__(self, ctx):
        super().__init__(
            label='Add birthday',
            style=discord.ButtonStyle.blurple
        )
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        def check(m):
            return (
                    m.author == interaction.user and
                    m.channel == self.ctx.channel
            )

        await interaction.response.send_message(
            "```Please enter the user's Discord username (e.g., user123).```",
            ephemeral=True
        )

        msg = await self.ctx.bot.wait_for("message", check=check)

        username = msg.content

        member: discord.Member = discord.utils.get(self.ctx.guild.members, name=username)

        if member is None:
            member = discord.utils.get(self.ctx.guild.members, display_name=username)

        if member is None:
            await interaction.followup.send(
                "```User not found. Please check the username and try again.```",
                ephemeral=True
            )
            return

        user_id = member.id

        await interaction.followup.send("```Enter birthday in DD.MM format:```", ephemeral=True)

        msg = await self.ctx.bot.wait_for("message", check=check)
        birthday = msg.content

        b_day = Birthday()
        response = await b_day.add_new_birthday(
            user_id,
            self.ctx.guild.id,
            birthday
        )

        await interaction.followup.send(response, ephemeral=True)
