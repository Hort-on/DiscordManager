from database.data_base_model import DB
from database.db_factory.scenarios.birthday import (
    AddBirthdayScenario,
    DeleteBirthdayScenario,
    ExistBirthdayCheckScenario,
    GetTodayBirthdayScenario,
    ResetAllCongratsScenario,
    UpdateLastCongratsScenario,
)
from database.db_factory.scenarios.cleanup import (
    CleanupGuild,
    CleanupSystemChannels,
    CleanupUser,
    CleanUpVerificationRole,
)
from database.db_factory.scenarios.common import (
    DeleteSet,
    FetchAllData,
    GetData,
    InitGuild,
    InsertSet,
    WriteData,
)
from general_services.logger.logger import Logger


class DBFactory:
    def __init__(self, db_connect: DB, logger: Logger):

        self.db_connect = db_connect
        self.logger = logger

    def for_get_data(self, guild_id: int, table_name: str, *columns: str) -> GetData:
        return GetData(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            table_name=table_name,
            *columns,
        )

    def for_write_data(
        self, guild_id: int, table_name: str, data: dict[str, int | str]
    ) -> WriteData:
        return WriteData(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            table_name=table_name,
            data=data,
        )

    def for_insert_set(
        self, guild_id: int, values: set[int], table_name: str, key: str
    ) -> InsertSet:
        return InsertSet(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            values=values,
            table_name=table_name,
            key=key,
        )

    def for_delete_set(
        self, guild_id: int, values: set[int], table_name: str, key: str
    ) -> DeleteSet:
        return DeleteSet(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            values=values,
            table_name=table_name,
            key=key,
        )

    def for_fetch_all(self, guild_id: int, table_name: str) -> FetchAllData:
        return FetchAllData(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            table_name=table_name,
        )

    def for_add_birthday(
        self, guild_id: int, user_id: int, user_birthday: str
    ) -> AddBirthdayScenario:
        return AddBirthdayScenario(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            user_id=user_id,
            user_birthday=user_birthday,
        )

    def for_delete_birthday(
        self, guild_id: int, user_id: int
    ) -> DeleteBirthdayScenario:
        return DeleteBirthdayScenario(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            user_id=user_id,
        )

    def for_exists_birthday_check(
        self, guild_id: int, user_id: int
    ) -> ExistBirthdayCheckScenario:
        return ExistBirthdayCheckScenario(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            user_id=user_id,
        )

    def for_get_today_birthday(
        self, guild_id: int, today: str
    ) -> GetTodayBirthdayScenario:
        return GetTodayBirthdayScenario(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            today=today,
        )

    def for_update_last_congrats(
        self, guild_id: int, user_id: int, today_str: str
    ) -> UpdateLastCongratsScenario:
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

    def for_cleanup_guild(self, guild_id: int) -> CleanupGuild:
        return CleanupGuild(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
        )

    def for_cleanup_user(self, guild_id: int, user_ids: set[int]) -> CleanupUser:
        return CleanupUser(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            user_ids=user_ids,
        )

    def for_cleanup_system_channel(
        self, guild_id: int, channels: list[str]
    ) -> CleanupSystemChannels:
        return CleanupSystemChannels(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
            channels=channels,
        )

    def for_init_guild(self, guild_id: int) -> InitGuild:
        return InitGuild(
            db_connect=self.db_connect,
            logger=self.logger,
            guild_id=guild_id,
        )

    def for_cleanup_role_delete(self, guild_id: int) -> CleanUpVerificationRole:
        return CleanUpVerificationRole(
            db_connect=self.db_connect, logger=self.logger, guild_id=guild_id
        )
