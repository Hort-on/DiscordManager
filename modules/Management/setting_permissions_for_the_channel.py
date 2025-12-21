import discord

from utils.channels_permissions import *


class SetPermissions:
    """
        A class to manage setting permissions on a Discord channel for a specific role.

        Attributes:
            channel (discord.abc.GuildChannel): The channel on which permissions will be set.
            role (discord.Role | None): The role to assign permissions to.

        Methods:
            set_permissions_for_channel(interaction: discord.Interaction) -> None:
                Prompts the user to input a role via message, then sets permissions based on channel type.
            send_the_result(interaction: discord.Interaction) -> None:
                Sends a confirmation message that permissions were set successfully.
        """
    def __init__(self, channel):
        self.channel = channel
        self.role = None

    async def set_permissions_for_channel(self, interaction: discord.Interaction) -> None:

        def check(msg):
            return (
                    msg.author == interaction.user
                    and msg.channel == interaction.channel
            )

        channel_type = self.channel.type

        await interaction.response.send_message('```Please type the role: @role```', ephemeral=True)

        message = await interaction.client.wait_for("message", check=check)

        role_mention = message.content

        try:
            role_id = int(role_mention.strip('<@&>'))
            self.role = discord.utils.get(interaction.guild.roles, id=role_id)
        except ValueError:
            await interaction.edit_original_response(content='```The role not found```')
            return

        if channel_type == discord.ChannelType.text:
            await self.channel.set_permissions(self.role, **text_channel_permissions)
            await self.send_the_result(interaction)

        elif channel_type == discord.ChannelType.voice:
            await self.channel.set_permissions(self.role, **voice_channel_permissions)
            await self.send_the_result(interaction)

        else:
            await interaction.edit_original_response(content='```Unexpected channel type.```')
            return

    async def send_the_result(self, interaction: discord.Interaction) -> None:
        await interaction.edit_original_response(
            content=f'```Permissions successfully set for the selected channel: {self.channel},'
            f' and the role: {self.role}```'
        )
        return
