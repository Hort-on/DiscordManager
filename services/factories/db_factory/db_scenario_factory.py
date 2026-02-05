import discord

from database.data_base_model import DB

from services.factories.db_factory.scenarios.common import (
    GetData,
    WriteData,
    WriteSuperuser,
    DeleteSuperuser,
    WriteSet,
    DeleteSet,
    FetchAllData,
    InitGuild
)

from services.factories.db_factory.scenarios.birthday import (
    AddBirthdayScenario,
    DeleteBirthdayScenario,
    ExistBirthdayCheckScenario,
    GetTodayBirthdayScenario,
    UpdateLastCongratsScenario,
    ResetAllCongratsScenario
)

from services.factories.db_factory.scenarios.cleanup import (
    CleanupRemovedGuildScenario,
    CleanupRemovedUserScenario,
    CleanupRemovedChannelScenario,
    CleanupRemovedRoleScenario
)

from services.logger.logger import Logger


class DBFactory:
    def __init__(
            self,
            db_connect: DB,
            logger: Logger
    ):

        self.db_connect = db_connect
        self.logger = logger

    def for_get_data(self, guild_id: int, table_name: str, *columns: str) -> GetData:
        return GetData(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            table_name=table_name,
            *columns
        )

    def for_write_data(self, guild_id: int, table_name: str, data: dict[str, int]) -> WriteData:
        return WriteData(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            table_name=table_name,
            data=data
        )

    def for_write_set(self, guild_id: int, values: set[int], table_name: str, key: str) -> WriteSet:
        return WriteSet(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            values=values,
            table_name=table_name,
            key=key
        )

    def for_delete_set(self, guild_id: int, values: set[int], table_name: str, key: str) -> DeleteSet:
        return DeleteSet(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            values=values,
            table_name=table_name,
            key=key
        )

    def for_write_superuser(self, guild_id: int, table_name: str, user_ids: set[int]) -> WriteSuperuser:
        return WriteSuperuser(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            table_name=table_name,
            user_ids=user_ids
        )

    def for_delete_superuser(self, interaction: discord.Interaction, user_ids: set[int]) -> DeleteSuperuser:
        return DeleteSuperuser(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=interaction.guild_id,
            user_ids=user_ids
        )

    def for_fetch_all(self, guild_id: int, table_name: str) -> FetchAllData:
        return FetchAllData(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            table_name=table_name
        )

    def for_add_birthday(self, guild_id: int, user_id: int, user_birthday: str) -> AddBirthdayScenario:
        return AddBirthdayScenario(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            user_id=user_id,
            user_birthday=user_birthday
        )

    def for_delete_birthday(self, guild_id: int, user_id: int) -> DeleteBirthdayScenario:
        return DeleteBirthdayScenario(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            user_id=user_id
        )

    def for_exists_birthday_check(self, guild_id: int, user_id: int) -> ExistBirthdayCheckScenario:
        return ExistBirthdayCheckScenario(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            user_id=user_id
        )

    def for_get_today_birthday(self, guild_id: int, today: str) -> GetTodayBirthdayScenario:
        return GetTodayBirthdayScenario(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            today=today
        )

    def for_update_last_congrats(self, guild_id: int, user_id: int, today_str: str) -> UpdateLastCongratsScenario:
        return UpdateLastCongratsScenario(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            user_id=user_id,
            today_str=today_str,
        )

    def for_reset_congrats(self) -> ResetAllCongratsScenario:
        return ResetAllCongratsScenario(
            db_connect=self.db_connect,
            logger=self.logger,
        )

    def for_remove_guild(self, guild_id: int) -> CleanupRemovedGuildScenario:
        return CleanupRemovedGuildScenario(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
        )

    def for_remove_user(self, guild_id: int, user_ids: set[int]) -> CleanupRemovedUserScenario:
        return CleanupRemovedUserScenario(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            user_ids=user_ids
        )

    def for_remove_channel(self, guild_id: int, channel_ids: set[int]) -> CleanupRemovedChannelScenario:
        return CleanupRemovedChannelScenario(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            channel_ids=channel_ids
        )

    def for_remove_role(self, guild_id: int, role_ids: set[int]) -> CleanupRemovedRoleScenario:
        return CleanupRemovedRoleScenario(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            role_ids=role_ids
        )

    def for_init_guild(self, guild_id: int) -> InitGuild:
        return InitGuild(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
        )
