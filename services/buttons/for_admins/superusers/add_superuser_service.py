import discord

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

from services.factories.db_factory.db_scenario_factory import DBFactory
from services.other_services.get_member_by_name import get_member_by_name


class AddSuperusersService:
    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBFactory
    ):
        self.settings = settings
        self.db_factory = db_factory

    @staticmethod
    def _build_embed(added_users: str, not_found_users: str, already_super: str) -> discord.Embed:
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
        await interaction.edit_original_response(embed=embed)
