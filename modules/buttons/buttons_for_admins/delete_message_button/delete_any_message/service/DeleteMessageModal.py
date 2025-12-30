import discord

from modules.buttons.buttons_for_admins.delete_message_button.delete_any_message.service.DeleteMessageService import \
    DeleteMessageService


class DeleteMessagesModal(discord.ui.Modal, title="Delete messages"):
    def __init__(self, channel: discord.TextChannel):
        super().__init__()
        self.channel = channel
        self.delete_msg_service = DeleteMessageService()

    amount = discord.ui.TextInput(
        label='How many messages do you want to delete?',
        placeholder='Enter a number',
        required=True,
        max_length=3
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.delete_msg_service.process(
            interaction=interaction,
            amount=int(self.amount.value),
            channel=self.channel
        )

