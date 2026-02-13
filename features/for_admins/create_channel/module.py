from .create_channel_service import CreateChannelService


def build(settings, db) -> CreateChannelService:
    create_channel_service = CreateChannelService()

    return CreateChannelService()
