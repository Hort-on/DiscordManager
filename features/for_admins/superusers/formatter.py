from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from .results import AddSuperusersResult, DeleteSuperusersResult

from database.settings_storage.settings_manager import StorageTarget

from ui.embed_constructor.embed_constructor import InfoEmbed, SuccessEmbed, WarningEmbed, ErrorEmbed

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage
    from general_services.translator.translator import Translator


class SuperusersFormatter:
    def __init__(self, settings: SettingsStorage, translator: Translator):
        self.settings = settings
        self.translator = translator

    def build_embed(self, guild: discord.Guild) -> discord.Embed:
        msg = self.translator.t(
            guild_id=guild.id,
            section='SUPERUSERS',
            key='current_superusers'
        )
        lines: list[str] = [msg, f'{'-' * 22}']

        users = self.settings.set_storage.for_set_get(
            target=StorageTarget.SUPERUSERS,
            guild_id=guild.id
        )

        if not users:
            not_found = self.translator.t(
                guild_id=guild.id,
                section='SUPERUSERS',
                key='no_superusers'
            )
            return WarningEmbed(
                description=not_found
            )
        else:
            for user_id in users:
                member = guild.get_member(user_id)
                name = member.display_name or member.global_name
                lines.append(f'🔸 {name}')

            return InfoEmbed(
                description='\n'.join(lines)
            )

    def build_add_result_embeds(self, result: AddSuperusersResult, guild_id: int) -> list[discord.Embed]:
        embeds: list[discord.Embed] = []

        if result.added_names:
            added_title = self.translator.t(
                guild_id=guild_id,
                section='SUPERUSERS',
                key='added_superusers'
            )
            embeds.append(
                SuccessEmbed(
                    description=self._format_block(
                        title=added_title,
                        items=result.added_names
                    )
                )
            )

        if result.not_found:
            not_found_title = self.translator.t(
                guild_id=guild_id,
                section='SUPERUSERS',
                key='not_found_for_addition'
            )
            embeds.append(
                ErrorEmbed(
                    description=self._format_block(
                        title=not_found_title,
                        items=result.not_found
                    )
                )
            )

        if result.already_super:
            already_superusers_title = self.translator.t(
                guild_id=guild_id,
                section='SUPERUSERS',
                key='already_superusers'
            )
            embeds.append(
                WarningEmbed(
                    description=self._format_block(
                        title=already_superusers_title,
                        items=result.already_super
                    )
                )
            )

        return embeds

    def build_delete_result_embeds(self, result: DeleteSuperusersResult, guild: discord.Guild) -> list[discord.Embed]:
        deleted_superusers_title = self.translator.t(
            guild_id=guild.id,
            section='SUPERUSERS',
            key='deleted_superusers'
        )

        embeds: list[discord.Embed] = [SuccessEmbed(
            description=self._format_block(
                title=deleted_superusers_title,
                items=result.deleted
            )
        )]

        if result.not_found_message:
            embeds.append(WarningEmbed(description=result.not_found_message))

        embeds.append(self.build_embed(guild=guild))

        return embeds

    @staticmethod
    def _format_block(title: str, items: set[str]) -> str:
        lines = [title, '-' * 30]

        if not items:
            lines.append('—')
        else:
            lines.extend(f'🔸 {item}' for item in items)

        return '\n'.join(lines)
