from database.data_base_model import DB

from database.db_factory.db_scenarios import(
    GetDataScenario,
    WriteDataScenario,
    WriteUserScenario,
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
