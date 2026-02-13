import discord

from collections import Counter

from general_services.other_services.get_member_by_name import get_member_by_name

from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed


class DeleteMessageService:

    @staticmethod
    async def delete_msg_process(
            interaction: discord.Interaction,
            channel: discord.TextChannel,
            amount: int
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        deleted = await channel.purge(limit=amount)

        if not deleted:
            embed = ErrorEmbed(
                description='No messages were found in the selected channel or from the selected users'
            )

            await interaction.followup.send(
                embed=embed,
                ephemeral=True
            )

            return

        success_embed = SuccessEmbed(
            description=f'{len(deleted)} messages were successfully deleted from the channel: {channel.name}'
        )

        await interaction.followup.send(
            embed=success_embed,
            ephemeral=True
        )


class DeleteMessageFromUserService:

    async def delete_msg_process(
            self,
            interaction: discord.Interaction,
            channel: discord.TextChannel,
            amount: int,
            users: str
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        user_names = self._get_users(
            interaction=interaction,
            users=users
        )

        result_msg = []

        users = set(user_names)

        def _check(m) -> bool:
            return m.author in users

        deleted = await channel.purge(
            limit=amount,
            check=_check
        )

        if not deleted:
            embed = ErrorEmbed(
                description='No messages were found in the selected channel or from the selected users'
            )

            await interaction.followup.send(
                embed=embed,
                ephemeral=True
            )

            return

        counter = Counter(msg.author.display_name for msg in deleted)
        for user_name, count in counter.items():
            result_msg.append(
                f'Successfully deleted {count} messages from user: {user_name}\n'
            )

        final_msg = ''.join(result_msg)

        success_embed = SuccessEmbed(
            description=final_msg
        )

        await interaction.followup.send(
            embed=success_embed,
            ephemeral=True
        )

    @staticmethod
    def _get_users(interaction: discord.Interaction, users: str) -> list[discord.Member]:
        user_list: list[discord.Member] = []

        usernames = [name.strip() for name in users.split(',')]

        for username in usernames:
            member = get_member_by_name(
                interaction=interaction,
                username=username
            )

            user_list.append(member)

        return user_list
