from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.buttons.navigator import Navigator

import asyncio

import discord

from typing import Optional, TYPE_CHECKING

from core.container import AppContainer

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

from services.drop_down_menu.drop_down_selector import DropMenuView
from services.embed_constructor.embed_constructor import SuccessEmbed, InfoEmbed
from services.factories.db_factory.db_scenario_factory import DBFactory
from services.other_services.get_member_by_name import get_member_by_name


if TYPE_CHECKING:
    from core.container import BotContainer


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
                in_superusers[member.id] = username
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
        added_users = ''
        for user_id in found_users.keys():
            member = interaction.guild.get_member(user_id)
            name = member.display_name if member else found_users[user_id]
            added_users += f'-> {name}\n'

        not_found_users = ''
        if not_found_result:
            not_found_users = '\n'.join([f'-> {name}' for name in not_found_result])

        already_super = ''
        if in_superusers:
            already_super = '\n'.join([f'-> {name}' for name in in_superusers])

        embed = self._build_embed(
            added_users=added_users,
            not_found_users=not_found_users,
            already_super=already_super
        )

        await self._save(
            interaction=interaction,
            user_ids=set(u_id for u_id in found_users.keys()),
            embed=embed
        )

    async def _save(
            self,
            interaction: discord.Interaction,
            user_ids: set[int],
            embed: discord.Embed
    ) -> None:
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
        if save_to_db_result:
            await self._send_the_result(interaction=interaction, embed=embed)

    @staticmethod
    async def _send_the_result(
            interaction: discord.Interaction,
            embed: discord.Embed
    ) -> None:
        await interaction.response.edit_message(embed=embed)

    # TODO: переробити через конструткор
    @staticmethod
    def _build_embed(added_users: str, not_found_users: str, already_super: str) -> discord.Embed:  # TODO: Використовувати загальний шаблон
        embed = discord.Embed(
            title='Superusers addition',
            color=discord.Color.blurple()
        )

        if added_users:
            embed.add_field(
                name='✅ Added superusers:',
                value=added_users,
                inline=False
            )

        if not_found_users:
            embed.add_field(
                name='❌ Users that were not found:',
                value=not_found_users,
                inline=False
            )

        if already_super:
            embed.add_field(
                name='⚠️ Already is superuser:',
                value=already_super,
                inline=False
            )

        return embed


class DeleteSuperuserService(BaseSuperuserService):
    def __init__(self, navigator: Navigator):
        super().__init__()
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

        options = [
            discord.SelectOption(
                label=value,
                value=str(key)
            )
            for key, value in user_list.items()
        ]

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='',
            callback=self._delete_superuser_callback
        )

        await interaction.response.edit_message(
            content='',
            view=view
        )

        if self.not_found_users:
            await self._cleanup_none_exists(
                guild_id=interaction.guild_id,
                not_found_users=self.not_found_users
            )

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

    async def _delete_superuser_callback(
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

        await self._processing_users(interaction=interaction, user_ids=user_ids_int, deleted=deleted)

    async def _processing_users(
            self,
            interaction: discord.Interaction,
            user_ids: set[int],
            deleted
    ):

        deleted_usernames: list[str] = []
        not_found_usernames: list[str] = ['**These users were not on this server and were deleted as well:**']

        if deleted:
            for user_id in user_ids:
                member = interaction.guild.get_member(user_id)
                if member:
                    user_name = member.display_name
                else:
                    user = await interaction.client.fetch_user(user_id)
                    user_name = user.global_name or user.name

                deleted_usernames.append(user_name)

        if self.not_found_users:
            for user_id in self.not_found_users:
                user = await interaction.client.fetch_user(user_id)
                user_name = user.global_name or user.name
                not_found_usernames.append(user_name)

        await self._build_and_send_embed(
            interaction=interaction,
            deleted_usernames=deleted_usernames,
            not_found_usernames=not_found_usernames
        )

    @staticmethod
    async def _build_and_send_embed(
            interaction: discord.Interaction,
            deleted_usernames: list[str],
            not_found_usernames: list[str]
    ):

        success_embed = None
        if deleted_usernames:
            success_embed = SuccessEmbed(
                description='**Deleted users:**'
                            + '\n'.join(f'-> {name}' for name in deleted_usernames)
            )

        info_embed = None
        if not_found_usernames:
            info_embed = InfoEmbed(
                description='**These users were not on this server and were deleted as well:**'
                            + '\n'.join(f'-> {name}' for name in not_found_usernames)
            )

        embeds_to_send = [embed for embed in [success_embed, info_embed] if embed is not None]
        await interaction.response.edit_message(embeds=embeds_to_send)


class GetSuperusersList(BaseSuperuserService):
    def __init__(self):
        super().__init__()

    def get_display(self, guild: discord.Guild) -> Optional[str]:
        user_ids = self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=guild.id
        )

        if not user_ids:
            return None

        return self._format_members(guild=guild, user_ids=user_ids)

    def _format_members(
        self,
        guild: discord.Guild,
        user_ids: set[int]
    ) -> str:
        names = ['The list of current users:']
        not_found_users: set[int] = set()

        for user_id in user_ids:
            member = guild.get_member(user_id)

            if not member:
                not_found_users.add(user_id)
                continue

            names.append(member.display_name)

        if not_found_users:
            asyncio.create_task(self._clean_up_not_found(
                guild_id=guild.id,
                not_found_users=not_found_users)
            )

        return '\n-> '.join(names)

    async def _clean_up_not_found(self, guild_id: int, not_found_users: set[int]):
        self.settings.set_storage.for_set_remove(
            target=StorageTarget.SUPERUSERS,
            guild_id=guild_id,
            value=not_found_users
        )

        cleanup_scenario = self.db_factory.for_remove_user(
            guild_id=guild_id,
            user_ids=not_found_users
        )

        await cleanup_scenario.db_proceed()

        lines.append('')
                lines.append('Superusers:')
                users = self.settings.set_storage.for_set_get(
                    target=StorageTarget.SUPERUSERS,
                    guild_id=interaction.guild_id
                )

                if not users:
                    lines.append('❌ NOT ASSIGNED')
                else:
                    for user_id in users:
                        member = interaction.guild.get_member(user_id)
                        name = member.display_name if member else f'Unknown ({user_id})'
                        lines.append(f'🔸 {name}')