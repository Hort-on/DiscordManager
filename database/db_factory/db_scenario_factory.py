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
    def for_get_data():
        return GetDataScenario()

    @staticmethod
    def for_write_data():
        return WriteDataScenario()

    @staticmethod
    def for_fetch_all():
        return FetchAllDataScenario()

    @staticmethod
    def for_add_birthday():
        return AddBirthdayScenario()

    @staticmethod
    def for_delete_birthday():
        return DeleteBirthdayScenario()

    @staticmethod
    def for_exists_birthday_check():
        return ExistBirthdayCheckScenario()

    @staticmethod
    def for_get_today_birthday():
        return  GetTodayBirthdayScenario()

    @staticmethod
    def for_update_last_congrats():
        return UpdateLstCongratsScenario()

    @staticmethod
    def for_reset_congrats():
        return ResetAllCongratsScenario()
