from __future__ import annotations

from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from features.for_everyone.birthdays.flow import BirthdayFlow


class AddBirthdayModal(discord.ui.Modal, title='Please enter a birthday:'):
    def __init__(self, flow: BirthdayFlow):
        super().__init__()
        self.flow = flow

    birthday_input = discord.ui.TextInput(
        label='Birthday (DD.MM)',
        placeholder='31.12',
        required=True,
        min_length=5,
        max_length=5
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.flow.add_birthday(
            interaction=interaction,
            user_birthday=self.birthday_input.value
        )
