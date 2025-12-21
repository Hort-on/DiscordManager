class DeleteMessageService:
    @staticmethod
    async def process(interaction, amount: int, channel):
        if not channel.permissions_for(interaction.user).manage_messages: #TODO: треба дізнатись більше про це
            await interaction.response.send_message(
                "❌ You don't have permission to delete messages",
                ephemeral=True
            )
            return

        deleted = await channel.purge(limit=amount)

        await interaction.response.send_message(
            f"✅ Deleted {len(deleted)} messages in {channel.mention}",
            ephemeral=True
        )
