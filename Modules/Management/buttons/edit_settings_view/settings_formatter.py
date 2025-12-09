import discord
from db.data_base_setup import DB


class SettingsFormatter:
    def __init__(self):
        self.db = DB()

    async def format_settings(self, interaction: discord.Interaction) -> str:
        settings = self.db.get_data(
            interaction.guild_id,
            'settings'
        )

        congrats_channel = interaction.client.get_channel(settings.get('congrats_channel_id'))
        system_channel = interaction.client.get_channel(settings.get('system_channel_id'))
        verification_channel = interaction.client.get_channel(settings.get('verification_channel_id'))

        message = None
        if verification_channel and settings.get('verification_msg_id'):
            try:
                message = await verification_channel.fetch_message(settings.get('verification_msg_id'))
            except discord.NotFound:
                message = None

        return (
            "```Current configuration:```\n\n"
            f"🔹 Birthday: {'Enabled' if settings.get('birthday') else 'Disabled'}\n"
            f"🔹 Congrats: {'Enabled' if settings.get('congrats') else 'Disabled'}\n"
            f"🔹 Congrats channel: {congrats_channel.name if congrats_channel else 'Not set'}\n"
            f"🔹 System channel: {system_channel.name if system_channel else 'Not set'}\n"
            f"🔹 Verification: {'Enabled' if settings.get('verification') else 'Disabled'}\n"
            f"🔹 Verification channel: {verification_channel.name if verification_channel else 'Not set'}\n"
            f"🔹 Verification message: {message if message else 'Not set'}\n"
            f"🔹 Blocking users: {'Enabled' if settings.get('block_users') else 'Disabled'}\n"
            f"🔹 Message management: {'Enabled' if settings.get('message_management') else 'Disabled'}\n"
            f"🔹 Invitation checking: {'Enabled' if settings.get('invitation_checking') else 'Disabled'}\n"
            f"🔹 Spam checking: {'Enabled' if settings.get('spam_checking') else 'Disabled'}\n"
            f"🔹 Member left notification: {'Enabled' if settings.get('member_left') else 'Disabled'}\n"
            f"🔹 Setting permissions for channels: {'Enabled' if settings.get('set_permissions') else 'Disabled'}\n"
            f"🔹 Sending messages: {'Enabled' if settings.get('sending_messages') else 'Disabled'}\n"
        )
