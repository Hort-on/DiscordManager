class ReactionHandler:
    def __init__(self, db):
        self.db = db

    async def check_if_verification(self, payload):
        result = await self.db.get_data(
            payload.guild_id,
            'settings',
            'verification',
            'verification_channel_id',
            'verification_msg_id'


        if not all(result.values()):
            return
