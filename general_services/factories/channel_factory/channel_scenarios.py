from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory

import discord

from modules.buttons.for_users.randomizer.modals import RandomTeamByChannelModal

from general_services.utils.messages import DB_MSGS, SYSTEM_MSGS


class ChannelScenario:
    async def on_selected_channel(self, interaction: discord.Interaction, channel):
        raise NotImplementedError


class SaveChannelToDBForMessageScenario(ChannelScenario):
    def __init__(self, db_factory: DBFactory):
        self.db_factory = db_factory

    async def on_selected_channel(
        self,
        interaction: discord.Interaction,
        channel
    ) -> None:

        write = self.db_factory.for_write_data(
            guild_id=interaction.guild.id,
            table_name='channels',
            data={
                'guild_id': interaction.guild.id,
                'user_id': interaction.user.id,
                'channel_id': channel.id
            }
        )

        result = await write.db_proceed()

        if result:
            await interaction.response.edit_message(
                content=DB_MSGS.get('channel_successful_msg')
            )

            await self._send_dm_to_user(interaction)
            return

        await interaction.response.edit_message(
            content=SYSTEM_MSGS.get('failure_msg')
        )

    @staticmethod
    async def _send_dm_to_user(interaction: discord.Interaction):
        try:
            dm = await interaction.user.create_dm()
            await dm.send(
                content=''
            )
        except discord.Forbidden:
            pass


class SaveChannelToDBScenario(ChannelScenario):
    def __init__(
            self,
            db_factory: DBFactory,
            config_key: str
    ):

        self.db_factory = db_factory
        self.config_key = config_key

    async def on_selected_channel(
            self,
            interaction: discord.Interaction,
            channel
    ) -> None:

        write = self.db_factory.for_write_data(
            guild_id=interaction.guild.id,
            table_name='settings',
            data={
                f'{self.config_key}_id': channel.id
            }
        )

        result = await write.db_proceed()
        if result:
            await interaction.response.edit_message(
                content=DB_MSGS.get('channel_successful_msg')
            )
            return

        await interaction.response.edit_message(
            content=SYSTEM_MSGS.get('failure_msg')
        )


class DeleteMessagesScenario(ChannelScenario):
    def __init__(self, modal):
        self.modal = modal

    async def on_selected_channel(
            self,
            interaction: discord.Interaction,
            channel
    ) -> None:
        await interaction.response.send_modal(
            self.modal(channel=channel)
        )


class RandomSelection(ChannelScenario):
    async def on_selected_channel(
            self,
            interaction: discord.Interaction,
            channel
    ) -> None:
        await interaction.response.send_modal(
            RandomTeamByChannelModal(channel=channel)
        )
