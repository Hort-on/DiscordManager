from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.params_containers import GeneralParams
from core.navigator.routes import Route

from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed, WarningEmbed

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from core.navigator.navigator_context import NavigationContext
    from features.for_everyone.role_manager.services import RoleManagerService
    from general_services.translator.translator import Translator


class RoleManagerFlow:
    def __init__(
            self,
            navigator: Navigator,
            context: NavigationContext,
            service: RoleManagerService,
            translator: Translator
    ):

        self.navigator = navigator
        self.context = context
        self.service = service
        self.translator = translator

    async def start_for_add(self, interaction: discord.Interaction) -> None:
        options = await self._get_available_guild_roles(
            interaction=interaction
        )

        if not options:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=interaction.guild_id,
                    section='ROLE_MANAGER',
                    key='no_role_found'
                )
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            translator=self.translator,
            guild_id=interaction.guild_id,
            placeholder=self.translator.t(
                guild_id=interaction.guild_id,
                section='ROLE_MANAGER',
                key='ask_r_to_add'
            ),
            callback=self._add_roles_to_user,
            max_values=min(25, len(options))
        )

        view.context = self.context

        self.context.push(
            target=Route.ROLE_MANAGER_MENU,
            params=GeneralParams(guild_id=interaction.guild_id)
        )

        await interaction.response.edit_message(view=view)

    async def start_for_remove(self, interaction: discord.Interaction) -> None:
        options = await self._get_user_roles(
            interaction=interaction
        )

        if not options:
            error_embed = ErrorEmbed(
                description=self.translator.t(
                    guild_id=interaction.guild_id,
                    section='ROLE_MANAGER',
                    key='no_role_found'
                )
            )
            await interaction.response.edit_message(embed=error_embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            translator=self.translator,
            guild_id=interaction.guild_id,
            placeholder=self.translator.t(
                guild_id=interaction.guild_id,
                section='ROLE_MANAGER',
                key='ask_r_to_remove'
            ),
            callback=self._remove_roles_from_user,
            max_values=min(25, len(options))
        )

        view.context = self.context

        self.context.push(target=Route.ROLE_MANAGER_MENU)

        await interaction.response.edit_message(view=view)

    async def _add_roles_to_user(self, interaction: discord.Interaction, roles: list[str]):
        result = await self.service.add_roles_to_user(
            member=interaction.user,
            guild=interaction.guild,
            roles=roles
        )

        success_embed = None
        failure_embed = None

        if result.added_roles:
            msg = self.translator.t(
                guild_id=interaction.guild_id,
                section='ROLE_MANAGER',
                key='success_addition'
            )
            success_message = [msg]
            success_message.extend(f'🔸 {role.name}' for role in result.added_roles)
            success_embed = SuccessEmbed(
                description='\n'.join(success_message)
            )

        if result.not_added_roles:
            msg = self.translator.t(
                guild_id=interaction.guild_id,
                section='ROLE_MANAGER',
                key='failed_addition'
            )
            failure_message = [msg]
            failure_message.extend(f'🔸 {role.name}' for role in result.not_added_roles)
            failure_embed = WarningEmbed(
                description='\n'.join(failure_message)
            )

        embeds = [embed for embed in (success_embed, failure_embed) if embed]

        await interaction.response.edit_message(embeds=embeds)

    async def _remove_roles_from_user(self, interaction: discord.Interaction, roles: list[str]):
        result = await self.service.remove_roles_from_user(
            member=interaction.user,
            guild=interaction.guild,
            roles=roles
        )

        success_embed = None
        failure_embed = None

        if result.removed_roles:
            msg = self.translator.t(
                guild_id=interaction.guild_id,
                section='ROLE_MANAGER',
                key='success_removal'
            )
            success_message = [msg]
            success_message.extend(f'🔸 {role.name}' for role in result.removed_roles)
            success_embed = SuccessEmbed(
                description='\n'.join(success_message)
            )

        if result.not_removed_roles:
            msg = self.translator.t(
                guild_id=interaction.guild_id,
                section='ROLE_MANAGER',
                key='failed_removal'
            )
            failure_message = [msg]
            failure_message.extend(f'🔸 {role.name}' for role in result.not_removed_roles)
            failure_embed = WarningEmbed(
                description='\n'.join(failure_message)
            )

        embeds = [embed for embed in (success_embed, failure_embed) if embed]

        await interaction.response.edit_message(embeds=embeds)

    async def _get_available_guild_roles(self, interaction: discord.Interaction) -> list[discord.SelectOption]:
        hidden_roles: set[int] = self.service.get_hidden_roles(
            guild_id=interaction.guild_id
        )

        member_role_ids = {role.id for role in interaction.user.roles}
        guild_roles = interaction.guild.roles

        available_roles = {
            role.id: role.name
            for role in guild_roles
            if (
                role.id not in hidden_roles
                and role.id not in member_role_ids
                and role.is_assignable()
            )
        }

        return [
            discord.SelectOption(
                label=name,
                value=str(role_id)
            )
            for role_id, name in sorted(
                available_roles.items(),
                key=lambda item: item[1].lower()
            )
        ]

    async def _get_user_roles(self, interaction: discord.Interaction) -> list[discord.SelectOption]:
        hidden_roles: set[int] = self.service.get_hidden_roles(
            guild_id=interaction.guild_id
        )

        return [
            discord.SelectOption(
                label=role.name,
                value=str(role.id)
            )
            for role in sorted(interaction.user.roles) if role.id not in hidden_roles
        ]
