from utils.messages import SYSTEM_MSGS as SM

class DeleteMessageService:
    @staticmethod
    async def process(interaction, amount: int, channel):
        if not channel.permissions_for(interaction.user).manage_messages:
            await interaction.edit_original_response(
                content=SM.get('permission_declined_msg'),
                ephemeral=True
            )
            return

        deleted = await channel.purge(limit=amount)

        await interaction.edit_original_response(
            content=SM.get('success_message_delete_msg').format(
                deleted=len(deleted),
                channel=channel.name
            ),
            ephemeral=True
        )
