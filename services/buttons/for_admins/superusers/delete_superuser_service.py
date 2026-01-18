import discord

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget

from services.drop_down_menu.drop_down_selector import DropMenuView
from services.embed_constructor.info import InfoEmbed
from services.embed_constructor.success import SuccessEmbed
from services.factories.db_factory.db_scenario_factory import DBFactory


class DeleteSuperuserService:
    def __init__(
            self,
            settings: SettingsStorage,
            db_factory: DBFactory
    ):

        self.settings = settings
        self.db_factory = db_factory
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
            options=options,
            placeholder='',
            callback=self._delete_superuser_callback
        )

        await interaction.edit_original_response(
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
        await interaction.edit_original_response(embeds=embeds_to_send)
