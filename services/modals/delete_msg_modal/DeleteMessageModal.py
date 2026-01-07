import discord

from services.factories.delete_msg_factory.delete_msg_scenario_factory import DeleteMessageScenario


class DeleteMessagesModal(discord.ui.Modal, title="Delete messages"):
    def __init__(self, channel: discord.TextChannel):
        super().__init__()
        self.channel = channel
        self.delete_factory = DeleteMessageScenario()

    amount = discord.ui.TextInput(
        label='How many messages do you want to delete?',
        placeholder='Please enter a number between 1 and 100',
        required=True,
        max_length=3
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        service_delete_msg = self.delete_factory.for_delete_msg(
            self.channel,
            int(self.amount.value)
        )
        await service_delete_msg.delete_msg_process(interaction)
