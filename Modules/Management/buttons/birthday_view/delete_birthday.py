import discord

from Modules.Birthdays.birthday import Birthday


class DeleteBirthdayButton(discord.ui.Button):
    def __init__(self, ctx):
        super().__init__(
            label='Delete birthday',
            style=discord.ButtonStyle.blurple
        )
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        def check(m):
            return (
                    m.author == self.ctx.author and
                    m.channel == self.ctx.channel
            )

        await interaction.response.send_message('```Please enter the user\'s discord name:```', ephemeral=True)

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

        b_day = Birthday()
        response = b_day.delete_birthday(
            user_id,
            self.ctx.guild.id
        )

        await interaction.followup.send(response, ephemeral=True)
