import discord
from utils.messages import CONFIGURATION_MESSAGES as CM

class SuperUserProcedure:
    def __init__(self, parent):
        self.parent = parent


    # ÏÎÒĞ²ÁÍÎ ÎÏÒÈÌ²ÇÓÂÀÒÈ ÒÀ ÏÅĞÅÏÈÑÀÒÈ
    async def super_user_procedure(self,  interaction: discord.Interaction):
        await interaction.edit_original_response(content=CM.get('super_user_procedure_msg'))

        def _check(m):
            return (
                    m.author == interaction.user and
                    m.channel == interaction.channel
            )

        try:
            msg = await interaction.client.wait_for('message', check=_check, timeout=300.0)

            usernames = [name.strip() for name in msg.content.split(',')]

            for username in usernames:
                member = discord.utils.get(interaction.guild.members, name=username)

                if member:
                    self.parent.found_users.append(member)

                if member is None:
                    member = discord.utils.get(interaction.guild.members, display_name=username)

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

                await interaction.edit_original_response(content=result_msg)
            else:
                #TODO: äîáàâèòè öå ïîâ³äîìëåííÿ ó çàãàëüíèé ñïèñîê messages
                await interaction.edit_original_response(
                    content="```None of the specified users were found on this server.```"
                )

        except self.parent.TimeoutError:
            await interaction.edit_original_response(content="```Time expired. Skipping superusers setup.```")

        await self.parent.next_step(interaction)
