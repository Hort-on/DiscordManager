import asyncio

import discord


class DeleteMessageButton(discord.ui.Button):
    def __init__(self, ctx):
        super().__init__(
            label='Delete message',
            style=discord.ButtonStyle.blurple
        )
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        def check(m):
            return (
                m.author == self.ctx.author and
                m.channel == self.ctx.channel
            )

        await interaction.response.send_message(
            "```Please enter the amount of messages to delete:```",
            ephemeral=True
        )

        msg = await self.ctx.bot.wait_for("message", check=check)

        try:
            amount = int(msg.content)
            if amount <= 0:
                raise ValueError
        except ValueError:
            return await interaction.followup.send(
                "```Invalid number. Please enter a positive integer.```",
                ephemeral=True
            )

        deleted = 0
        async for message in self.ctx.channel.history(limit=amount):
            try:
                await message.delete()
                deleted += 1
            except discord.NotFound:
                pass
            await asyncio.sleep(0.5)

        await interaction.followup.send(
            f"```Deleted {deleted} messages.```",
            ephemeral=True
        )
