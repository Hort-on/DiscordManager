from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from services.drop_down_menu.drop_down_selector import DropMenuView

if TYPE_CHECKING:
    from core.container import BotContainer
    from services.factories.db_factory.db_scenario_factory import DBFactory
    from database.settings_storage.settings import SettingsStorage
    from services.buttons.navigator import Navigator

from core.container import AppContainer

from database.settings_storage.settings_manager import StorageTarget

from modules.buttons.for_admins.edit_settings_buttons.services.settings_formatter import SettingsFormatter

from services.embed_constructor.embed_constructor import SuccessEmbed, ErrorEmbed


class EditMainSettingsService:
    def __init__(self, navigator: Navigator):
        container: BotContainer = AppContainer.get()

        self.db_factory: DBFactory = container.db_factory
        self.settings: SettingsStorage = container.settings
        self.navigator = navigator
        self.formatter = SettingsFormatter()
        self.role_key = None

    def build_options(self, guild_id: int):
        settings = self.settings.dict_storage.for_dict_get_all(
            target=StorageTarget.SETTINGS,
            guild_id=guild_id
        )
        print(settings)
        return [
            discord.SelectOption(
                label=k.replace('_', ' ').title(),
                value=k
            )
            for k, v in sorted(settings.items(), key=lambda item: item[0])
        ]

    async def proceed_result(self, interaction: discord.Interaction, config_key: list[str]):
        if config_key[0] == 'verification_role_id':
            options = [
                discord.SelectOption(
                    label=role.name,
                    value=str(role.id)
                )
                for role in interaction.guild.roles
            ]

            view = DropMenuView(
                navigator=self.navigator,
                options=options,
                placeholder='Please select the role:',
                callback=self._save_verify_role
            )

            await interaction.response.edit_message(view=view)
        else:
            await self._save_data(interaction=interaction, config_key=config_key[0])

    async def _save_verify_role(self, interaction: discord.Interaction, config_key: list[str]):
        write = self.db_factory.for_write_data(
            guild_id=interaction.guild_id,
            table_name='settings',
            data={'verification_role_id': int(config_key[0])}
        )

        result = await write.db_proceed()
        if not result:
            embed = ErrorEmbed(
                description='Somethings went wrong, please try again later'
            )
            await interaction.response.edit_message(embed=embed)
            return

        self.settings.dict_storage.for_dict_set(
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id,
            key='verification_role_id',
            value=int(config_key[0])
        )

        role = interaction.guild.get_role(int(config_key[0]))

        success_embed = SuccessEmbed(
            description=f'verification role is successfully assigned to: {role.name}'
        )

        settings_embed = self.formatter.format_current_main_settings(interaction)

        await interaction.response.edit_message(
            embeds=[settings_embed, success_embed]
        )

    async def _save_data(self, interaction: discord.Interaction, config_key: str):
        current_value = self.settings.dict_storage.for_dict_get(
            config_key,
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id,
        )

        current = current_value.get(config_key, False)
        new_value = not current

        write = self.db_factory.for_write_data(
            guild_id=interaction.guild_id,
            table_name='settings',
            data={config_key: new_value}
        )

        db_result = await write.db_proceed()
        if not db_result:
            embed = ErrorEmbed(
                description='Somethings went wrong, please try again later'
            )
            await interaction.response.edit_message(embed=embed)
            return

        self.settings.dict_storage.for_dict_set(
                target=StorageTarget.SETTINGS,
                guild_id=interaction.guild_id,
                key=config_key,
                value=new_value
        )

        success_embed = SuccessEmbed(
            description=f'{config_key} is successfully {'enabled' if new_value else 'disabled'}'
        )

        settings_embed = self.formatter.format_current_main_settings(interaction)

        await interaction.response.edit_message(
            embeds=[settings_embed, success_embed]
        )
