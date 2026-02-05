from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator
    from core.container import BotContainer

import discord

from core.container import AppContainer

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

from modules.buttons.for_admins.superusers_buttons.format_users_list import SuperusersFormatter

from services.embed_constructor.embed_constructor import SuccessEmbed, InfoEmbed, WarningEmbed
from services.factories.db_factory.db_scenario_factory import DBFactory
from services.other_services.get_member_by_name import get_member_by_name


# TODO: Подумати щодо оптимізації
class BaseSuperuserService:
    def __init__(self):
        container: BotContainer = AppContainer.get()
        self.settings: SettingsStorage = container.settings
        self.db_factory: DBFactory = container.db_factory


class AddSuperusersService(BaseSuperuserService):
    def __init__(self):
        super().__init__()

    async def superuser_proceed(
            self,
            interaction: discord.Interaction,
            superuser_names: str
    ) -> None:
        not_found_users: list[str] = []
        found_users: dict[int, str] = {}
        in_superusers: dict[int, str] = {}

        superusers = self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=interaction.guild_id
        )

        usernames = [name.strip() for name in superuser_names.split(',')]

        for username in usernames:
            member = get_member_by_name(
                interaction=interaction,
                username=username
            )

            if member is None:
                not_found_users.append(username)
                continue

            if member.id in superusers:
                in_superusers[member.id] = member.display_name
                continue

            found_users[member.id] = username

        await self._format_the_result(
            interaction=interaction,
            found_users=found_users,
            not_found_result=not_found_users,
            in_superusers=in_superusers
        )

    async def _format_the_result(
            self,
            interaction: discord.Interaction,
            found_users: dict[int, str],
            not_found_result: list[str],
            in_superusers: dict[int, str]
    ) -> None:
        success_embed = None
        warning_embed = None
        info_embed = None

        if found_users:
            added_users: list[str] = ['Added superusers:', f'{'-' * 20}']

            for user_id in found_users.keys():
                member = interaction.guild.get_member(user_id)
                name = member.display_name
                added_users.append(f'🔸 {name}')

            success_embed = SuccessEmbed(
                description='\n'.join(added_users)
            )

        if not_found_result:
            not_found_users: list[str] = ['Not found members:', f'{'-' * 22}',
                                          '\n'.join([f'❗ {name}' for name in not_found_result])]
            warning_embed = WarningEmbed(
                description='\n'.join(not_found_users)
            )

        if in_superusers:
            already_super: list[str] = ['These members are already superusers:', f'{'-' * 37}',
                                        '\n'.join([f'🔸 {name}' for name in in_superusers.values()])]
            info_embed = InfoEmbed(
                description='\n'.join(already_super)
            )

        await self._save(
            interaction=interaction,
            user_ids=set(u_id for u_id in found_users.keys()),
            embeds=[success_embed, warning_embed, info_embed],
            found=bool(found_users)
        )

    async def _save(
            self,
            interaction: discord.Interaction,
            user_ids: set[int],
            embeds: list[discord.Embed],
            found: bool
    ) -> None:
        if found:
            self.settings.set_storage.for_set_add(
                target=StorageTarget.SUPERUSERS,
                guild_id=interaction.guild_id,
                value=user_ids
            )

            scenario = self.db_factory.for_write_superuser(
                guild_id=interaction.guild_id,
                table_name='super_users',
                user_ids=user_ids
            )

            save_to_db_result = await scenario.db_proceed()
            if not save_to_db_result:
                warning_embed = WarningEmbed(
                    description='Something went wrong, please try again later.'
                )

                await interaction.response.edit_message(embed=warning_embed)
                return

        await interaction.response.edit_message(embeds=[e for e in embeds if e is not None])


class DeleteSuperuserService(BaseSuperuserService):
    def __init__(self, navigator: Navigator):
        super().__init__()
        container: BotContainer = AppContainer.get()
        self.settings: SettingsStorage = container.settings
        self.navigator = navigator
        self.not_found_users: set[int] = set()

    async def prepare_users(self, interaction: discord.Interaction):
        self.not_found_users.clear()
        user_list: dict[int, str] = {}

        superusers = self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=interaction.guild_id
        )

        for user in superusers:
            member = interaction.guild.get_member(user)

            if member is not None:
                display = member.display_name
                global_name = member.global_name or member.name
                label = f'{display} ({global_name})'
                user_list[user] = label
            else:
                self.not_found_users.add(user)

        if self.not_found_users:
            await self._cleanup_none_exists(
                guild_id=interaction.guild_id,
                not_found_users=self.not_found_users
            )

        return [
            discord.SelectOption(
                label=value,
                value=str(key)
            )
            for key, value in user_list.items()
        ]

    async def delete_superuser_callback(
            self,
            interaction: discord.Interaction,
            user_ids_str: list[str]
    ):
        user_ids_int = {int(user_id) for user_id in user_ids_str}

        scenario = self.db_factory.for_delete_superuser(
            interaction=interaction,
            user_ids=user_ids_int
        )

        deleted = await scenario.db_proceed()

        self.settings.set_storage.for_set_remove(
            target=StorageTarget.SUPERUSERS,
            guild_id=interaction.guild_id,
            value=user_ids_int
        )

        await self._processing_users(interaction=interaction, user_ids=user_ids_int, deleted=deleted)

    async def _processing_users(
            self,
            interaction: discord.Interaction,
            user_ids: set[int],
            deleted: bool
    ):
        deleted_usernames: list[str] = []

        if deleted:
            for user_id in user_ids:
                member = interaction.guild.get_member(user_id)
                if member:
                    user_name = member.display_name
                else:
                    user = await interaction.client.fetch_user(user_id)
                    user_name = user.global_name or user.name

                deleted_usernames.append(user_name)

        await self._build_and_send_embed(
            interaction=interaction,
            deleted_usernames=deleted_usernames,
        )

    async def _build_and_send_embed(
            self,
            interaction: discord.Interaction,
            deleted_usernames: list[str]
    ):
        formatter = SuperusersFormatter()
        current_s_users_embed = None
        success_embed = None
        if deleted_usernames:
            deleted: list[str] = ['Deleted users:', f'{'-' * 15}']
            for name in deleted_usernames:
                deleted.append(f'🔸{name}')

            current_s_users_embed = formatter.build_embed(interaction=interaction)

            success_embed = SuccessEmbed(
                description='\n'.join(deleted)
            )

        info_embed = None
        if self.not_found_users:
            not_found_usernames: list[str] = ['These users were not on this server and were deleted as well:',
                                              f'{'-' * 40}']
            for user_id in self.not_found_users:
                user = await interaction.client.fetch_user(user_id)
                user_name = user.global_name or user.name
                not_found_usernames.append(f'🔸{user_name}')

            info_embed = InfoEmbed(
                description='\n'.join(not_found_usernames)
            )

        embeds_to_send = [e for e in [success_embed, info_embed, current_s_users_embed] if e is not None]
        await interaction.response.edit_message(embeds=embeds_to_send)

    async def _cleanup_none_exists(self, guild_id: int, not_found_users: set[int]):
        scenario = self.db_factory.for_remove_user(
            guild_id=guild_id,
            user_ids=not_found_users
        )

        await scenario.db_proceed()

        for user in not_found_users:
            self.settings.dict_storage.for_dict_remove(
                target=StorageTarget.CHANNELS_TO_SEND,
                guild_id=guild_id,
                key=user
            )