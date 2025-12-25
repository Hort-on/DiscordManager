def get_channel_name(interaction, channel_id):
    if not channel_id:
        return '❌ Not selected'

    channel = interaction.client.get_channel(channel_id)
    return channel.name if channel else '❌ Not accessible'
