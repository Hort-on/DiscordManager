import discord
from db.messages import CONFIGURATION_MESSAGES as CM

class SuperUserProcedure:
    def __init__(self, parent):
        self.parent = parent


    # ÏÎÒĞ²ÁÍÎ ÎÏÒÈÌ²ÇÓÂÀÒÈ ÒÀ ÏÅĞÅÏÈÑÀÒÈ
    async def super_user_procedure(self,  interaction: discord.Interaction):
        await interaction.response.send_message(
            CM.get('super_user_procedure_msg'),
            ephemeral=True
        )

        def _check(m):
            return (
                    m.author == self.parent.ctx.author and
                    m.channel == self.parent.ctx.channel
            )

        try:
            msg = await self.parent.ctx.bot.wait_for('message', check=_check, timeout=300.0)

            usernames = [name.strip() for name in msg.content.split(',')]

            for username in usernames:
                member = discord.utils.get(self.parent.ctx.guild.members, name=username)

                if member:
                    self.parent.found_users.append(member)

                if member is None:
                    member = discord.utils.get(self.parent.ctx.guild.members, display_name=username)

                    if member:
                        self.parent.found_users.append(member)
                    else:
                        self.parent.not_found_users.append(username)

                found_result = f"Added {len(self.parent.found_users)} superuser(s):\n"
                found_result += "\n".join([f"- {member.name}" for member in self.parent.found_users])

                not_found_result = ""
                if self.parent.not_found_users:
                    not_found_result = "\n\nNot found on this server, please check their names:\n"
                    not_found_result += "\n".join([f"- {name}" for name in self.parent.not_found_users])

                result_msg = f"```{found_result}{not_found_result}```"

                await self.parent.ctx.send(result_msg, delete_after=120)
            else:
                await self.parent.ctx.send(
                    "```None of the specified users were found on this server.```",
                    delete_after=120
                )

        except self.parent.TimeoutError:
            await self.parent.ctx.send("```Time expired. Skipping superusers setup.```", delete_after=60)

        await self.parent.next_step(interaction)
