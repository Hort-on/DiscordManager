import discord

from collections import Counter

from utils.messages import SYSTEM_MSGS as SM


class DeleteMessageBaseService:
    def __init__(
            self,
            channel,
            amount: int
    ):
        self.channel = channel
        self.amount = amount

    async def delete_msg_process(self, interaction: discord.Interaction) -> None:
        raise NotImplementedError


class DeleteMessageService(DeleteMessageBaseService):
    def __init__(
            self,
            channel,
            amount: int
    ):
        super().__init__(channel, amount)

    async def delete_msg_process(self, interaction: discord.Interaction) -> None:
        deleted = await self.channel.purge(limit=self.amount)

        if not deleted:
            await interaction.edit_original_response(
                content=SM.get('no_msg_found').format(
                    channel=self.channel.name
                )
            )
            return

        await interaction.edit_original_response(
            content=SM.get('success_message_delete_msg').format(
                deleted=len(deleted),
                channel=self.channel.name
            )
        )


class DeleteMessageFromUserService(DeleteMessageBaseService):
    def __init__(
            self,
            channel,
            amount: int,
            users: str
    ):
        super().__init__(channel, amount)
        self.users = users
        self.user_list: list[discord.Member] = []
        self.not_found_users = []

    async def delete_msg_process(self, interaction: discord.Interaction) -> None:
        self._get_users(interaction)

        result_msg = []

        users = set(self.user_list)

        def _check(m) -> bool:
            return m.author in users

        deleted = await self.channel.purge(
            limit=self.amount,
            check=_check
        )

        if not deleted:
            await interaction.edit_original_response(
                content=SM.get('no_msg_found').format(
                    channel=self.channel.name
                )
            )
            return

        counter = Counter(msg.author.name for msg in deleted)
        for user_name, count in counter.items():
            result_msg.append(
                f'Successfully deleted {count} messages from user: {user_name}\n'
            )

        await self._send_result(interaction, result_msg)

    def _get_users(
            self,
            interaction: discord.Interaction
    ) -> None:

        usernames = [name.strip() for name in self.users.split(',')]

        for username in usernames:
            member = discord.utils.find(
                lambda m: m.name == username or m.display_name == username,
                interaction.guild.members
            )

            if member is None:
                self.not_found_users.append(username)
                continue

            self.user_list.append(member)

    async def _send_result(
            self,
            interaction: discord.Interaction,
            result_msg: list[str]
    ) -> None:

        final_msg = ''.join(result_msg)

        if self.not_found_users:
            final_msg += "\n\nNot found users:\n"
            final_msg += "\n".join(f"-> {member}" for member in self.not_found_users)

        await interaction.edit_original_response(
            content=f'```{final_msg}```'
        )
