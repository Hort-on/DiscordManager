from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from database.db_base_service import DBBaseService
from features.for_everyone.randomizer.modals import RandomTeamByChannelModal

from general_services.utils.messages import DB_MSGS, SYSTEM_MSGS

if TYPE_CHECKING:
    from database.db_factory.db_scenario_factory import DBFactory


class ChannelScenario:
    async def on_selected_channel(self, interaction: discord.Interaction, channel):
        raise NotImplementedError


class SaveChannelToDBScenario(ChannelScenario, DBBaseService):
    def __init__(self, db_factory: DBFactory, config_key: str):
        super().__init__()

        self.db_factory = db_factory
        self.config_key = config_key

    async def on_selected_channel(
            self,
            interaction: discord.Interaction,
            channel
    ) -> None:

        write_scenario = self.db_factory.for_write_data(
            guild_id=interaction.guild.id,
            table_name='settings',
            data={
                f'{self.config_key}_id': channel.id
            }
        )

        result = await self.update_db_and_cache(
            scenario=write_scenario,
            guild_id=interaction.guild_id
        )

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
