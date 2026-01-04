import discord

from factories.delete_msg_factory.delete_msg_scenario_factory import DeleteMessageScenario


class DeleteUserMessagesModal(discord.ui.Modal, title="Delete messages from users"):
    def __init__(self, channel: discord.TextChannel):
        super().__init__()
        self.channel = channel
        self.delete_factory = DeleteMessageScenario()

    amount = discord.ui.TextInput(
        label='How many messages do you want to delete?',
        placeholder='Enter a number',
        required=True,
        max_length=3
    )

    user_names = discord.ui.TextInput(
        label='Type user names',
        placeholder='Please type general user names like: user123, user_2, user etc. separated by coma.',
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        service_delete_ser_msg = self.delete_factory.for_delete_user_msg(
            channel=self.channel,
            amount=int(self.amount.value),
            users=str(self.user_names.value)
        )
        await service_delete_ser_msg.delete_msg_process(interaction)
