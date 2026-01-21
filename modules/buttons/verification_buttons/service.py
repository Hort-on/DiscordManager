import discord

from database.settings_storage.settings import SettingsStorage
from database.settings_storage.settings_manager import StorageTarget
from services.embed_constructor.embed_constructor import ErrorEmbed, SuccessEmbed


class AntiBotService:
    def __init__(self, settings: SettingsStorage):
        self.settings = settings
        self.users_count: dict[int, int] = {}

    async def check_the_word(self, interaction: discord.Interaction, word: str):
        if word.lower() != 'hello':
            fail_embed = ErrorEmbed(
                description='You wrote the word incorrectly.'
                            ' You have one more attempt.'
                            ' If you fail, you will be kicked off the server'
            )
            await interaction.response.send_message(
                embed=fail_embed,
                ephemeral=True
            )

            user_id = interaction.user.id

            self.users_count[user_id] = self.users_count.get(user_id, 0) + 1

            if self.users_count.get(user_id) >= 2:
                await interaction.user.kick(reason='has not passed verification')
                self.users_count.pop(user_id, None)

            return

        await self._assign_role(interaction=interaction)

    async def _assign_role(self, interaction: discord.Interaction):
        verification_role = self.settings.dict_storage.for_dict_get(
            target=StorageTarget.SETTINGS,
            guild_id=interaction.guild_id,
            key='verification_role_id'
        )

        if not verification_role:
            error_embed = ErrorEmbed(
                description='Verification role is not assigned yet, please contact with the admins of the server.'
            )
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return

        role = interaction.guild.get_role(verification_role)
        await interaction.user.add_roles(role)

        success_embed = SuccessEmbed(
            description='Congratulations! Welcome to our community. For additional info, please use "/help"'
        )

        self.users_count.pop(interaction.user.id, None)

        if interaction.response.is_done():
            await interaction.edit_original_response(
                embed=success_embed,
            )
            return

        await interaction.response.send_message(
            embed=success_embed,
            ephemeral=True
        )
