from __future__ import annotations

from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from features.auto_moderation.verification.flow import VerificationFlow


class AgreeButton(discord.ui.Button):
    def __init__(self, flow: VerificationFlow):
        super().__init__(
            label='Agree',
            style=discord.ButtonStyle.green,
            custom_id='verify_agree'
        )

        self.flow = flow

    async def callback(self, interaction: discord.Interaction) -> None:
        await self.flow.agreement_start(interaction=interaction)


class DisagreeButton(discord.ui.Button):
    def __init__(self, flow: VerificationFlow):
        super().__init__(
            label='Disagree',
            style=discord.ButtonStyle.red,
            custom_id='verify_disagree'
        )

        self.flow = flow

    async def callback(self, interaction: discord.Interaction):
        await self.flow.disagreement_start(interaction=interaction)
