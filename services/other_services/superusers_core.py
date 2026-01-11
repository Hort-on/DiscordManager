import discord


class SuperUserService:
    def __init__(self):
        self.not_found_users = []
        self.found_users: dict[int, str] = {}

    async def superuser_proceed(
            self,
            interaction: discord.Interaction,
            superuser_names
    ) -> None:

        usernames = [name.strip() for name in superuser_names.split(',')]

        for username in usernames:
            member = (
                    discord.utils.get(
                        interaction.guild.members,
                        name=username.lower()
                    )

                    or discord.utils.get(
                        interaction.guild.members,
                        display_name=username.lower()
                    )
            )

            if member is None:
                self.not_found_users.append(username)
                continue

            self.found_users[member.id] = username

        self._format_the_result(interaction)

    def _format_the_result(
            self,
            interaction: discord.Interaction,
    ) -> None:

        found_result = f"Added {len(self.found_users)} superuser(s):\n"
        for user_id, user_name in self.found_users.items():
            member = interaction.guild.get_member(user_id)
            name = member.display_name if member else f"Original name not found. \nProvided name -> {user_name}"
            found_result += f"-> {name}\n"

        not_found_result = ""
        if self.not_found_users:
            not_found_result = "\n\nNot found on this server, please check their names:\n"
            not_found_result += "\n".join(
                [f"-> {name}" for name in self.not_found_users]
            )

        result_msg = f"```{found_result}{not_found_result}```"

        self._send_the_result(
            interaction,
            result_msg
        )

    @staticmethod
    async def _send_the_result(
            interaction: discord.Interaction,
            result_msg
    ) -> None:

        await interaction.edit_original_response(content=result_msg)
