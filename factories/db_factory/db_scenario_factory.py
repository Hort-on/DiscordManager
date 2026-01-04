from database.data_base_model import DB

from factories.db_factory.scenarios.common_scenarios.common_scenarios import (
    GetDataScenario,
    WriteDataScenario,
    WriteUserScenario,
    FetchAllDataScenario,
    InitGuildScenario
)

from factories.db_factory.scenarios.birthday_scenarios.birthday_scenarios import (
    AddBirthdayScenario,
    DeleteBirthdayScenario,
    ExistBirthdayCheckScenario,
    GetTodayBirthdayScenario,
    UpdateLastCongratsScenario,
    ResetAllCongratsScenario
)

from factories.db_factory.scenarios.cleanup_scenarios.cleanup_scenarios import (
    CleanupRemovedGuildScenario,
    CleanupRemovedUserScenario,
    CleanupRemovedChannelScenario,
    CleanupRemovedRoleScenario
)

from modules.logger.logger import Logger


class DBScenarioFactory:
    def __init__(
            self,
            db_connect: DB,
            logger: Logger
    ):

        self.db_connect = db_connect
        self.logger = logger

    def for_get_data(
            self,
            guild_id: int,
            table_name: str,
            *columns: str
    ) -> GetDataScenario:

        return GetDataScenario(
            self.db_connect,
            self.logger,
            guild_id,
            table_name,
            columns
        )

    def for_write_data(
            self,
            guild_id: int,
            table_name: str,
            data: dict
    ) -> WriteDataScenario:

        return WriteDataScenario(
            self.db_connect,
            self.logger,
            guild_id,
            table_name,
            data
        )

    def for_write_user(
            self,
            guild_id: int,
            table_name: str,
            user_ids: list[int]
    ):

        return WriteUserScenario(
            self.db_connect,
            self.logger,
            guild_id,
            table_name,
            user_ids
        )

    def for_fetch_all(
            self,
            guild_id: int,
            table_name: str
    ) -> FetchAllDataScenario:

        return FetchAllDataScenario(
            self.db_connect,
            self.logger,
            guild_id,
            table_name
        )

    def for_add_birthday(
            self,
            guild_id: int,
            user_id: int,
            user_birthday: str
    ) -> AddBirthdayScenario:

        return AddBirthdayScenario(
            self.db_connect,
            self.logger,
            guild_id,
            user_id,
            user_birthday
        )

    def for_delete_birthday(
            self,
            guild_id: int,
            user_id: int,
    ) -> DeleteBirthdayScenario:

        return DeleteBirthdayScenario(
            self.db_connect,
            self.logger,
            guild_id,
            user_id
        )

    def for_exists_birthday_check(
            self,
            guild_id: int,
            user_id: int
    ) -> ExistBirthdayCheckScenario:

        return ExistBirthdayCheckScenario(
            self.db_connect,
            self.logger,
            guild_id,
            user_id
        )

    def for_get_today_birthday(
            self,
            guild_id: int,
            today: str
    ) -> GetTodayBirthdayScenario:

        return GetTodayBirthdayScenario(
            self.db_connect,
            self.logger,
            guild_id,
            today
        )

    def for_update_last_congrats(
            self,
            guild_id: int,
            user_id: int,
            today_str: str
    ) -> UpdateLastCongratsScenario:

        return UpdateLastCongratsScenario(
            self.db_connect,
            self.logger,
            guild_id,
            user_id,
            today_str,
        )

    def for_reset_congrats(
            self
    ) -> ResetAllCongratsScenario:

        return ResetAllCongratsScenario(
            self.db_connect,
            self.logger,
        )

    def for_remove_guild(
            self,
            guild_id: int,

    ) -> CleanupRemovedGuildScenario:

        return CleanupRemovedGuildScenario(
            self.db_connect,
            self.logger,
            guild_id,
        )

    def for_remove_user(
            self,
            guild_id: int,
            user_id: int

    ) -> CleanupRemovedUserScenario:

        return CleanupRemovedUserScenario(
            self.db_connect,
            self.logger,
            guild_id,
            user_id
        )

    def for_remove_channel(
            self,
            guild_id: int,
            channel_id: int

    ) -> CleanupRemovedChannelScenario:

        return CleanupRemovedChannelScenario(
            self.db_connect,
            self.logger,
            guild_id,
            channel_id
        )

    def for_remove_role(
            self,
            guild_id: int,
            role_id: int

    ) -> CleanupRemovedRoleScenario:

        return CleanupRemovedRoleScenario(
            self.db_connect,
            self.logger,
            guild_id,
            role_id
        )

    def for_init_guild(
            self,
            guild_id: int
    ) -> InitGuildScenario:

        return InitGuildScenario(
            self.db_connect,
            self.logger,
            guild_id
        )
