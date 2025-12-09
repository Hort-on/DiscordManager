import discord
from discord import ui

from Modules.Management.setting_permissions_for_the_channel import SetPermissions
from db.data_base_setup import DB
from db.messages import EDIT_CONFIG_MESSAGES, GENERAL_MESSAGES


class ChannelTypeView(ui.View):
    """View channel type selection"""
    def __init__(
            self,
            text_only=False,
            write_data_to_db=None,
            parent=None,
            config_key=None,
            permissions=None,
            send_the_result=None
    ):
        super().__init__(timeout=60)
        self.text_only = text_only
        self.parent = parent
        self.config_key = config_key
        self.write_data_to_db = write_data_to_db
        self.permissions = permissions
        self.send_the_result = send_the_result

        options = [
            discord.SelectOption(
                label='Text channel',
                value='text',
                emoji='?'
            )
        ]

        if not text_only:
            options.append(
                discord.SelectOption(
                    label='Voice channel',
                    value='voice',
                    emoji='?'
                )
            )

        select = ui.Select(
            placeholder=GENERAL_MESSAGES.get('ask_channel_type_msg'),
            options=options
        )

        select.callback = self.select_channel_type
        self.add_item(select)

    async def select_channel_type(self, interaction: discord.Interaction) -> None:
        """Callback for selecting channel type"""
        select = self.children[0]
        channel_type = select.values[0]

        if channel_type == 'text':
            channels = [
                channel for channel in interaction.guild.channels
                if isinstance(channel, discord.TextChannel)
            ]
        else:
            channels = [
                channel for channel in interaction.guild.channels
                if isinstance(channel, discord.VoiceChannel)
            ]

        if not channels:
            await interaction.response.edit_message(
                content='No channels of this type found!',
                view=None
            )
            return

        view = ChannelListView(
            channels,
            channel_type,
            self.write_data_to_db,
            self.parent,
            self.config_key,
            self.permissions,
            self.send_the_result
        )
        await interaction.response.edit_message(
            content=f"Please select {'text' if channel_type == 'text' else 'voice'} channel:",
            view=view
        )


class ChannelListView(ui.View):
    """View to select a specific channel from the list"""

    def __init__(
            self,
            channels: list,
            channel_type: str,
            write_data_to_db=None,
            parent=None,
            config_key=None,
            permissions=None,
            send_the_result=None
    ):
        super().__init__(timeout=60)
        self.channel_type = channel_type
        self.parent = parent
        self.config_key = config_key
        self.write_data_to_db = write_data_to_db
        self.permissions = permissions
        self.send_the_result = send_the_result

        options = []
        for channel in channels:
            options.append(
                discord.SelectOption(
                    label=channel.name,
                    value=str(channel.id),
                    description=f'Name: {channel.name}'
                )
            )

        select = ui.Select(
            placeholder=GENERAL_MESSAGES.get('ask_channel_msg'),
            options=options
        )
        select.callback = self.select_channel_callback
        self.add_item(select)

    async def select_channel_callback(self, interaction: discord.Interaction) -> None:
        select = self.children[0]
        channel_id = int(select.values[0])
        selected_channel = interaction.client.get_channel(channel_id)

        if selected_channel:
            if self.parent and self.config_key:
                self.parent.config[self.config_key] = selected_channel.id
                await self.parent.next_step(interaction)

            if self.permissions:
                permissions_handler = SetPermissions(selected_channel)
                await permissions_handler.set_permissions_for_channel(interaction)

            await interaction.response.edit_message(
                content=f'```Selected channel: {selected_channel.name}```',
                view=None
            )
        else:
            await interaction.response.edit_message(
                content='Error: Channel not found!',
                view=None
            )

        if self.write_data_to_db:
            success = await self.write_to_db(interaction, selected_channel)
            if self.send_the_result:
                await interaction.followup.send(
                    EDIT_CONFIG_MESSAGES.get('success_editing_msg' if success else 'failed_editing_msg'),
                    ephemeral=True)


    @staticmethod
    async def write_to_db(interaction, selected_channel) -> None:
        db = DB()
        await db.write_data(interaction.guild.id, "channels", {
            "user_id": interaction.user.id,
            "channel_id": selected_channel.id
        })
