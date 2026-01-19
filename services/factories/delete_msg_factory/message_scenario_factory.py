from services.factories.delete_msg_factory.message_scenario import DeleteMessageService, DeleteMessageFromUserService


class DeleteMessageScenario:

    @staticmethod
    def for_delete_msg(channel, amount: int) -> DeleteMessageService:
        return DeleteMessageService(channel, amount)

    @staticmethod
    def for_delete_user_msg(channel, amount: int, users: str) -> DeleteMessageFromUserService:
        return DeleteMessageFromUserService(channel, amount, users)
