from __future__ import annotations

from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from features.for_admins.superusers.flow import SuperusersFlow


class AddSuperusersModal(discord.ui.Modal, title='Superuser names.'):
    def __init__(self, flow: SuperusersFlow):
        super().__init__()
        self.flow = flow

    superuser_names = discord.ui.TextInput(
        label='Please type superuser names',
        placeholder='user123, user456, user_, _user, etc.',
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.flow.save_members(
            interaction=interaction,
            user_names=self.superuser_names.value
        )
