from database.db_factory.db_scenarios import(
    GetDataScenario,
    WriteDataScenario,
    FetchAllDataScenario,
    AddBirthdayScenario,
    DeleteBirthdayScenario,
    ExistBirthdayCheckScenario,
    GetTodayBirthdayScenario,
    UpdateLastCongratsScenario,
    ResetAllCongratsScenario
)
from modules.logger.logger import Logger


class DBScenarioFactory:

    @staticmethod
    def for_get_data(
            logger: Logger,
            guild_id: int,
            table_name: str,
            *columns: str
    ) -> GetDataScenario:

        return GetDataScenario(
            logger,
            guild_id,
            table_name,
            columns
        )

    @staticmethod
    def for_write_data(
            logger: Logger,
            guild_id: int,
            table_name: str,
            data: dict
    ) -> WriteDataScenario:

        return WriteDataScenario(
            logger,
            guild_id,
            table_name,
            data
        )

    @staticmethod
    def for_fetch_all(
            logger: Logger,
            guild_id: int,
            table_name: str
    ) -> FetchAllDataScenario:

        return FetchAllDataScenario(
            logger,
            guild_id,
            table_name
        )

    @staticmethod
    def for_add_birthday(
            logger: Logger,
            guild_id: int,
            user_id: int,
            user_birthday: str
    ) -> AddBirthdayScenario:

        return AddBirthdayScenario(
            logger,
            guild_id,
            user_id,
            user_birthday
        )

    @staticmethod
    def for_delete_birthday(
            logger: Logger,
            guild_id: int,
            user_id: int,
    ) -> DeleteBirthdayScenario:

        return DeleteBirthdayScenario(
            logger,
            guild_id,
            user_id
        )

    @staticmethod
    def for_exists_birthday_check(
            logger: Logger,
            guild_id: int,
            user_id: int
    ) -> ExistBirthdayCheckScenario:

        return ExistBirthdayCheckScenario(
            logger,
            guild_id,
            user_id
        )

    @staticmethod
    def for_get_today_birthday(
            logger: Logger,
            guild_id: int,
            today: str
    ) -> GetTodayBirthdayScenario:

        return GetTodayBirthdayScenario(
            logger,
            guild_id,
            today
        )

    @staticmethod
    def for_update_last_congrats(
            logger: Logger,
            guild_id: int,
            user_id: int,
            today_str: str
    ) -> UpdateLastCongratsScenario:

        return UpdateLastCongratsScenario(
            logger,
            guild_id,
            user_id,
            today_str,
        )

    @staticmethod
    def for_reset_congrats(
            logger: Logger
    ) -> ResetAllCongratsScenario:

        return ResetAllCongratsScenario(logger)
