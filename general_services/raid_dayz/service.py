import asyncio

import discord


class RaidService:
    CHANNEL_ID = 1491810952776257577
    WEBHOOK_ID = [
        1491811762943557695,
    ]
    ROLE_ID = 1491862896270118912
    LIMIT = 10

    def __init__(self):
        self.active = False
        self.task: asyncio.Task | None = None

    async def start_raid(self, guild: discord.Guild | None, webhook_id: int) -> None:
        if self.active:
            return

        self.active = True
        self.task = asyncio.create_task(self._raid_loop(guild=guild, webhook_id=webhook_id))

    async def stop_raid(self):
        self.active = False

        if self.task:
            self.task.cancel()
            self.task = None

    async def _raid_loop(self, guild: discord.Guild | None, webhook_id: int) -> None:
        count = 0
        if guild:
            try:
                while self.active and count < self.LIMIT:
                    await self._send_raid_notification(
                        guild=guild, webhook_id=webhook_id
                    )
                    count += 1
                    await asyncio.sleep(15)
            except asyncio.CancelledError:
                pass
            finally:
                self.active = False

    async def _send_raid_notification(self, guild, webhook_id: int) -> None:
        channel = guild.get_channel(self.CHANNEL_ID)
        if not isinstance(channel, discord.TextChannel):
            return

        role = guild.get_role(self.ROLE_ID)
        if not role:
            return

        server = "Лівонія!" if webhook_id == 1491811762943557695 else "Чернорусь!"

        await channel.send(f"{role.mention}" + server)
