import discord

from services.factories.delete_msg_factory.message_scenario_factory import DeleteMessageScenario


class DeleteMessagesModal(discord.ui.Modal, title="Delete messages"):
    def __init__(self, channel: discord.TextChannel):
        super().__init__()
        self.channel = channel

    amount = discord.ui.TextInput(
        label='How many messages do you want to delete?',
        placeholder='Please enter a number between 1 and 100',
        required=True,
        max_length=3
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        delete_msg_scenario = DeleteMessageScenario.for_delete_msg(
            self.channel,
            int(self.amount.value)
        )
        await delete_msg_scenario.delete_msg_process(interaction)


class DeleteUserMessagesModal(discord.ui.Modal, title="Delete messages from users"):
    def __init__(self, channel: discord.TextChannel):
        super().__init__()
        self.channel = channel

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
        delete_msg_scenario = DeleteMessageScenario.for_delete_user_msg(
            channel=self.channel,
            amount=int(self.amount.value),
            users=str(self.user_names.value)
        )
        await delete_msg_scenario.delete_msg_process(interaction)
