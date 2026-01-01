import discord


class SuperUserService:

    async def superuser_proceed(
            self,
            interaction: discord.Interaction,
            parent,
            superuser_names
    ) -> None:

        usernames = [name.strip() for name in superuser_names.split(',')]

        for username in usernames:
            member = (
                    discord.utils.get(
                        interaction.guild.members,
                        name=username
                    )

                    or discord.utils.get(
                        interaction.guild.members,
                        display_name=username
                    )
            )

            if member is None:
                parent.not_found_users.append(username)
                continue

            parent.found_users[member.id] = username

        self._format_the_result(interaction, parent)

    def _format_the_result(
            self,
            interaction: discord.Interaction,
            parent
    ) -> None:

        found_result = f"Added {len(parent.found_users)} superuser(s):\n"
        for user_id, user_name in parent.found_user_ids.items():
            member = interaction.guild.get_member(user_id)
            name = member.display_name if member else f"Original name not found. \nProvided name -> {user_name}"
            found_result += f"-> {name}\n"

        not_found_result = ""
        if parent.not_found_users:
            not_found_result = "\n\nNot found on this server, please check their names:\n"
            not_found_result += "\n".join(
                [f"-> {name}" for name in parent.not_found_users]
            )

        result_msg = f"```{found_result}{not_found_result}```"

        self._send_the_result(
            interaction,
            parent,
            result_msg
        )

    @staticmethod
    async def _send_the_result(
            interaction: discord.Interaction,
            parent,
            result_msg
    ) -> None:

        await interaction.edit_original_response(content=result_msg)
        await parent.next_step(interaction)
