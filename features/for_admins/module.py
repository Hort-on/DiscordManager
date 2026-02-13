from dataclasses import dataclass


@dataclass
class AdministrationModule:
    create_channel_service: CreateChannelService
    delete_msg_service: RoleManagerService
    audit_service: AuditService


def build(settings, db, logger) -> AdministrationModule:
    ...
