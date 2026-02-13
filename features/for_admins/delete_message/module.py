from dataclasses import dataclass

from .delete_msg_service import DeleteMessageService, DeleteMessageFromUserService


@dataclass
class DeleteMsgModule:
    delete_any_msg_service: DeleteMessageService
    delete_msg_from_user_service: DeleteMessageFromUserService


def build() -> DeleteMsgModule:
    delete_any_msg_service = DeleteMessageService()
    delete_msg_from_user_service = DeleteMessageFromUserService()

    return DeleteMsgModule(
        delete_any_msg_service=delete_any_msg_service,
        delete_msg_from_user_service=delete_msg_from_user_service
    )
