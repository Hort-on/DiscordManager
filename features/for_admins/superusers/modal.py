from __future__ import annotations

from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from features.for_admins.superusers.flow import SuperusersFlow
    from general_services.translator.translator import Translator


class AddSuperusersModal(discord.ui.Modal):
    def __init__(self, flow: SuperusersFlow, translator: Translator, guild_id: int):
        super().__init__(
            title=translator.t(
                guild_id=guild_id, section="SUPERUSERS", key="superuser_names"
            )
        )
        self.flow = flow

        self.superuser_names = discord.ui.TextInput(
            label=translator.t(
                guild_id=guild_id, section="SUPERUSERS", key="ask_s_users_names"
            ),
            placeholder="user123, user456, user_, _user, etc.",
            required=True,
        )

        self.add_item(self.superuser_names)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.flow.save_members(
            interaction=interaction, user_names=self.superuser_names.value
        )
