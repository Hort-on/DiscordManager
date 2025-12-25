from database.db_factory.db_scenarios import(
    GetDataScenario,
    WriteDataScenario,
    FetchAllDataScenario,
    AddBirthdayScenario,
    DeleteBirthdayScenario,
    ExistBirthdayCheckScenario,
    GetTodayBirthdayScenario,
    UpdateLstCongratsScenario,
    ResetAllCongratsScenario
)


class DBScenarioFactory:

    @staticmethod
    def for_get_data(guild_id: int, table_name: str, *columns: str) -> GetDataScenario:
        return GetDataScenario(guild_id, table_name, columns)

    @staticmethod
    def for_write_data() -> WriteDataScenario:
        return WriteDataScenario()

    @staticmethod
    def for_fetch_all() -> FetchAllDataScenario:
        return FetchAllDataScenario()

    @staticmethod
    def for_add_birthday(guild_id: int, user_id: int, user_birthday: str) -> AddBirthdayScenario:
        return AddBirthdayScenario(guild_id, user_id, user_birthday)

    @staticmethod
    def for_delete_birthday(guild_id: int, user_id: int) -> DeleteBirthdayScenario:
        return DeleteBirthdayScenario(guild_id, user_id)

    @staticmethod
    def for_exists_birthday_check(guild_id: int, user_id: int,) -> ExistBirthdayCheckScenario:
        return ExistBirthdayCheckScenario(guild_id, user_id)

    @staticmethod
    def for_get_today_birthday(guild_id: int, today: str) -> GetTodayBirthdayScenario:
        return GetTodayBirthdayScenario(guild_id, today)

    @staticmethod
    def for_update_last_congrats(guild_id: int, user_id: int, today_str: str) -> UpdateLstCongratsScenario:
        return UpdateLstCongratsScenario(guild_id, user_id, today_str)

    @staticmethod
    def for_reset_congrats() -> ResetAllCongratsScenario:
        return ResetAllCongratsScenario()
