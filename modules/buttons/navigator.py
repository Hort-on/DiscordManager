from __future__ import annotations

import discord

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.container import BotContainer


class Navigator:
    def __init__(self, container: BotContainer = None):
        self.container = container

    async def go(
        self,
        target: str,
        interaction: discord.Interaction,
        ephemeral: bool = True,
    ):
        if not self.container:
            raise RuntimeError("Navigator: container is not initialized.")

        view = None
        guild_id = interaction.guild_id
        user_id = interaction.user.id

        match target:
            case 'main_menu':
                from modules.buttons.main_button_view import MainMenuView
                view = MainMenuView(
                    settings=self.container.settings,
                    navigator=self,
                    guild_id=guild_id,
                    user_id=user_id
                )

            case 'admin_menu':
                from modules.buttons.for_admins.admin_menu_view import AdminMenuView
                view = AdminMenuView(
                    settings=self.container.settings,
                    navigator=self,
                    guild_id=guild_id
                )

            case 'birthday_menu':
                from modules.buttons.for_admins.birthday_buttons.menu_view import BirthdayMenuView
                view = BirthdayMenuView(
                    navigator=self
                )

            case 'delete_msg_menu':
                from modules.buttons.for_admins.delete_message_buttons.menu_view import DeleteMsgMenuView
                view = DeleteMsgMenuView(
                    navigator=self
                )

            case 'superusers_menu':
                from modules.buttons.for_admins.superusers_buttons.menu_view import SuperusersMenuView
                view = SuperusersMenuView(
                    navigator=self
                )

            case 'random_menu':
                from modules.buttons.for_users.randomizer.menu_view import RandomModeView
                view = RandomModeView(
                    navigator=self
                )

            case 'role_manager_menu':
                from modules.buttons.for_users.role_manager.menu_view import RoleManagerView
                view = RoleManagerView(
                    navigator=self
                )

            case 'edit_settings':
                from modules.buttons.for_admins.edit_settings_buttons.services import (
                    SettingsFormatter,
                    SettingSelectorView
                )

                formatter = SettingsFormatter()
                summary = await formatter.format_settings(interaction)

                view = SettingSelectorView(navigator=self)

                await interaction.edit_original_response(
                    content=summary,
                    view=view
                )
                return

        if not interaction.response.is_done():
            await interaction.response.send_message(
                view=view,
                ephemeral=ephemeral
            )
        else:
            await interaction.edit_original_response(view=view)
