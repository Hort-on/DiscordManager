from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.navigator import Navigator

import discord

from modules.buttons.button_protection.admin_buttons_protection import FirewallButton

from modules.buttons.for_admins.delete_message_buttons.modals import (
    DeleteMessagesModal,
    DeleteUserMessagesModal
)

from general_services.factories.channel_factory.scenarios_factory import ChannelFactory
from general_services.other_services.get_channel import ChannelSelectorManager
from core.navigator_context import NavigationContext
from ui.drop_down_menu.drop_down_selector import DropMenuView
from ui.embed_constructor.embed_constructor import ErrorEmbed


class DeleteAnyMessageButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='🗑️Delete any messages',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        scenario = ChannelFactory.for_message_deletion(modal=DeleteMessagesModal)

        service = ChannelSelectorManager(
            navigator=self.navigator,
            scenario=scenario,
            text_only=True
        )

        options = await service.build_options(interaction=interaction)

        if not options:
            embed = ErrorEmbed(
                description=f'The guild does not have text channels.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the channel:',
            callback=service.proceed_channel
        )

        context = getattr(view, 'context', NavigationContext())

        context.push(target='delete_msg_menu', params={'guild_id': interaction.guild_id})

        view.context = context

        await interaction.response.edit_message(view=view)


class DeleteUserMessageButton(FirewallButton):
    scope = 'admin'

    def __init__(self, navigator: Navigator):
        super().__init__(
            label='🗑️👤Delete messages from users',
            style=discord.ButtonStyle.secondary
        )
        self.navigator = navigator

    async def on_click(self, interaction: discord.Interaction) -> None:
        scenario = ChannelFactory.for_message_deletion(modal=DeleteUserMessagesModal)

        service = ChannelSelectorManager(
            navigator=self.navigator,
            scenario=scenario,
            text_only=True
        )

        options = await service.build_options(interaction=interaction)

        if not options:
            embed = ErrorEmbed(
                description=f'The guild does not have text channels.'
            )
            await interaction.response.edit_message(embed=embed)
            return

        view = DropMenuView(
            navigator=self.navigator,
            options=options,
            placeholder='Please select the channel:',
            callback=service.proceed_channel
        )

        context = getattr(view, 'context', NavigationContext())

        context.push(target='delete_msg_menu', params={'guild_id': interaction.guild_id})

        view.context = context

        await interaction.response.edit_message(view=view)
