import discord
from discord import app_commands

from database.settings_storage.settings_manager import StorageTarget


# TODO: поки не використовується
def is_superuser(settings):
    async def predicate(interaction: discord.Interaction) -> bool:
        storage = interaction.client.settings_storage

        superusers = storage.set_storage.get_for_set(
            StorageTarget.SUPERUSERS,
            interaction.guild_id
        )

        if interaction.user.id not in superusers:
            await interaction.edit_original_response(
                content=''
            )
            return False

        return True

    return app_commands.check(predicate)
