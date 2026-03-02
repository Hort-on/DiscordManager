from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.navigator.navigator_context import NavigationContext
from core.navigator.routes import Route

from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed, WarningEmbed

if TYPE_CHECKING:
    from core.navigator.navigator import Navigator
    from features.for_everyone.role_manager.services import RoleManagerService


class RoleManagerFlow:
    def __init__(self, navigator: Navigator, service: RoleManagerService):
        self.navigator = navigator
        self.service = service

    async def start_for_add(self, interaction: discord.Interaction) -> None:
        options = await self._get_available_guild_roles(
            interaction=interaction
        )

        if not options:
            embed = ErrorEmbed(
                description='No available roles were found.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please choose the roles you want to add:',
            callback=self._add_roles_to_user,
            max_values=min(25, len(options))
        )

        context = getattr(view, 'context', None)

        if context is None:
            context = NavigationContext()
            view.context = context

        context.push(target=Route.ROLE_MANAGER_MENU)

        await interaction.response.edit_message(view=view)

    async def start_for_remove(self, interaction: discord.Interaction) -> None:
        options = await self._get_user_roles(
            interaction=interaction
        )

        if not options:
            embed = ErrorEmbed(
                description='No available roles were found.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please choose the roles you want to remove:',
            callback=self._remove_roles_from_user,
            max_values=min(25, len(options))
        )

        context = getattr(view, 'context', None)
        if context is None:
            context = NavigationContext()
            view.context = context

        context.push(target=Route.ROLE_MANAGER_MENU)

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
            success_message = ['The following roles have been successfully added:']
            success_message.extend(f'🔸 {role.name}' for role in result.added_roles)
            success_embed = SuccessEmbed(
                description='\n'.join(success_message)
            )

        if result.not_added_roles:
            failure_message = ['Some of the roles were not added']
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
            success_message = ['The following roles have been successfully removed:']
            success_message.extend(f'🔸 {role.name}' for role in result.removed_roles)
            success_embed = SuccessEmbed(
                description='\n'.join(success_message)
            )

        if result.not_removed_roles:
            failure_message = ['Some of the roles were not removed']
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

    @staticmethod
    async def _build_and_send_result(
            interaction: discord.Interaction,
            role_ids: set[int],
            addition: bool
    ) -> None:
        added_roles_message = 'The following roles have been successfully added:'
        removed_roles_message = 'The following roles have been successfully removed:'

        embed = None
        role_names: list[str] = [added_roles_message if addition else removed_roles_message]
        for role_id in role_ids:
            role = interaction.guild.get_role(role_id)
            role_names.append(f'🔸{role.name}')

            embed = SuccessEmbed(
                description='\n'.join(role_names)
            )

        await interaction.response.edit_message(embed=embed)
