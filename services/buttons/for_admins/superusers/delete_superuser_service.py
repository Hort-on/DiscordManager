import discord
from dependency_injector.wiring import inject, Provide

from core.bot_container import BotContainer
from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget
from services.drop_down_menu.drop_down_selector import DropMenuView
from services.factories.db_factory.db_scenario_factory import DBScenarioFactory


class DeleteSuperuserService:
    @inject
    def __init__(
            self,
            settings: SettingsStorage = Provide[BotContainer.settings],
            db_factory: DBScenarioFactory = Provide[BotContainer.db_factory]
    ):

        self.settings = settings
        self.db_factory = db_factory

    async def prepare_users(self, interaction: discord.Interaction):
        user_list: dict[int, str] = {}
        not_found_users: set[int] = set()

        superusers = self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=interaction.guild_id
        )

        for user in superusers:
            member = interaction.guild.get_member(user)

            if member:
                display = member.display_name
                global_name = member.global_name or member.name
                label = f'{display} ({global_name})'
            else:
                label = f'Unknown user ({user})'
                not_found_users.add(user)

            user_list[user] = label

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

        if not_found_users:
            await self._cleanup_none_exists(
                guild_id=interaction.guild_id,
                not_found_users=not_found_users
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
            user_ids: list[str]
    ):
        user_ids_int = {int(user_id) for user_id in user_ids}

        scenario = self.db_factory.for_delete_superuser(
            interaction=interaction,
            user_ids=user_ids_int
        )

        deleted = await scenario.db_proceed()

        if deleted > 0:
            await interaction.edit_original_response(
                content=f'✅ {deleted}'
            )

            self.settings.set_storage.for_set_remove(
                target=StorageTarget.SUPERUSERS,
                guild_id=interaction.guild_id,
                value=user_ids_int
            )
        else:
            await interaction.edit_original_response(
                content=''
            )
