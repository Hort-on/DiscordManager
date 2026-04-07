from __future__ import annotations

from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from features.for_everyone.birthdays.flow import BirthdayFlow
    from general_services.translator.translator import Translator


class AddBirthdayModal(discord.ui.Modal):
    def __init__(self, flow: BirthdayFlow, translator: Translator, guild_id: int):
        super().__init__(
            title=translator.t(
                guild_id=guild_id, section="BIRTHDAYS", key="ask_birthday"
            )
        )
        self.flow = flow

        self.birthday_input = discord.ui.TextInput(
            label=translator.t(
                guild_id=guild_id, section="BIRTHDAYS", key="modal_label"
            ),
            placeholder="31.12",
            required=True,
            min_length=5,
            max_length=5,
        )

        self.add_item(self.birthday_input)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.flow.save_birthday(
            interaction=interaction, user_birthday=self.birthday_input.value
        )


class AddAdminBirthdayModal(discord.ui.Modal):
    def __init__(self, flow: BirthdayFlow, translator: Translator, guild_id: int):
        super().__init__(
            title=translator.t(
                guild_id=guild_id, section="BIRTHDAYS", key="ask_birthday"
            )
        )
        self.flow = flow

        self.user_name = discord.ui.TextInput(
            label=translator.t(
                guild_id=guild_id, section="BIRTHDAYS", key="user_name_modal_label"
            ),
            placeholder="user, user1, user123, etc.",
            required=True,
        )

        self.birthday_input = discord.ui.TextInput(
            label=translator.t(
                guild_id=guild_id, section="BIRTHDAYS", key="modal_label"
            ),
            placeholder="31.12",
            required=True,
            min_length=5,
            max_length=5,
        )

        self.add_item(self.user_name)
        self.add_item(self.birthday_input)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.flow.admin_for_add(
            interaction=interaction,
            user_name=self.user_name.value,
            user_birthday=self.birthday_input.value,
        )


class DeleteAdminBirthdayModal(discord.ui.Modal):
    def __init__(self, flow: BirthdayFlow, translator: Translator, guild_id: int):
        super().__init__(
            title=translator.t(
                guild_id=guild_id, section="BIRTHDAYS", key="user_name_modal_label"
            )
        )
        self.flow = flow

        self.user_name = discord.ui.TextInput(
            label=translator.t(
                guild_id=guild_id, section="BIRTHDAYS", key="user_name_modal_label"
            ),
            placeholder="user, user1, user123, etc.",
            required=True,
        )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.flow.add_for_admin(interaction=interaction)
