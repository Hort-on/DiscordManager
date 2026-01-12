import discord


class AddSuperusersService:
    @staticmethod
    def _build_embed(found_text: str, not_found_text: str) -> discord.Embed:
        embed = discord.Embed(
            title='Superusers addition',
            color=discord.Color.blurple()
        )

        if found_text:
            embed.add_field(
                name='✅ Added superusers:',
                value=found_text,
                inline=False
            )

        if not_found_text:
            embed.add_field(
                name='❌ Users that were not found:',
                value=not_found_text,
                inline=False
            )

        return embed

    async def superuser_proceed(
            self,
            interaction: discord.Interaction,
            superuser_names: str
    ) -> None:
        not_found_users: list[str] = []
        found_users: dict[int, str] = {}

        usernames = [name.strip() for name in superuser_names.split(',')]

        for username in usernames:
            member = (
                    discord.utils.get(interaction.guild.members, name=username.lower())
                    or discord.utils.get(interaction.guild.members, display_name=username.lower())
            )

            if member is None:
                not_found_users.append(username)
                continue

            found_users[member.id] = username

        await self._format_the_result(interaction, found_users, not_found_users)

    async def _format_the_result(
            self,
            interaction: discord.Interaction,
            found_users: dict[int, str],
            not_found_users: list[str]
    ) -> None:
        found_result = ""
        for user_id in found_users.keys():
            member = interaction.guild.get_member(user_id)
            name = member.display_name if member else found_users[user_id]
            found_result += f"-> {name}\n"

        not_found_result = ""
        if not_found_users:
            not_found_result = "\n".join([f"-> {name}" for name in not_found_users])

        embed = self._build_embed(found_result, not_found_result)
        await self._send_the_result(interaction, embed)

    @staticmethod
    async def _send_the_result(
            interaction: discord.Interaction,
            embed: discord.Embed
    ) -> None:
        await interaction.edit_original_response(embed=embed)
