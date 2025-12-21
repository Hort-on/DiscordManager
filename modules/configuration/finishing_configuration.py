import discord
from database.data_base_model import DB


class FinishingConfiguration:
    def __init__(self, parent):
        self.parent = parent
        self.db = DB()

    async def finishing_configuration(self, interaction: discord.Interaction) -> None:
        try:
            await self.db.write_data(
                interaction.guild.id,
                'settings',
                {key.replace('_enabled', ''): value for key, value in self.parent.config.items()}
            )
        except Exception as e:
            print(f"[DB ERROR] Failed to write config to the db: {e}")

        if self.parent.found_users:
            await self.users_procedure(interaction)
        else:
            await self.send_the_result(interaction)

    async def users_procedure(self, interaction) -> None:
        for member in self.parent.found_users:
            try:
               await self.db.write_data(
                    interaction.guild.id,
                    "super_users",
                    {"user_id": member.id
                     })
            except Exception as e:
                print(f"[DB ERROR] Failed to write user to the db: {e}")

        await self.send_the_result(interaction)

    async def send_the_result(self, interaction: discord.Interaction) -> None:
        system_channel_id = self.parent.config.get('system_channel_id')
        congrats_channel_id = self.parent.config.get('congrats_channel_id')

        system_channel = interaction.client.get_channel(system_channel_id) if system_channel_id else None
        congrats_channel = interaction.client.get_channel(congrats_channel_id) if congrats_channel_id else None

        summary = (
            "configuration completed!\n\n"
            f"🔹 Congrats: {'✅ Enabled' if self.parent.config.get('congrats_enabled') else '❌ Disabled'}\n"
            f"🔹 Birthday feature: {'✅ Enabled' if self.parent.config.get('birthday_enabled') else '❌ Disabled'}\n"
            f"🔹 Verification: {'✅ Enabled' if self.parent.config.get('verification_enabled') else '❌ Disabled'}\n"
            f"🔹 Invitation checking: {'✅ Enabled' if self.parent.config.get('invitation_checking_enabled')
            else '❌ Disabled'}\n"
            f"🔹 Spam handling: {'✅ Enabled' if self.parent.config.get('spam_checking_enabled') else '❌ Disabled'}\n"
            f"🔹 Member left notification: {'✅ Enabled' if self.parent.config.get('member_left_enabled')
            else '❌ Disabled'}\n"
            f"🔹 Blocking users: {'✅ Enabled' if self.parent.config.get('block_users_enabled') else '❌ Disabled'}\n"
            f"🔹 System channel: {system_channel.name if system_channel else '❌ Not selected'}\n"
            f"🔹 Congrats channel: {congrats_channel.name if congrats_channel else '❌ Not selected'}\n"
            f"🔹 Superusers: {'✅ Assigned' if self.parent.found_users else '❌ Not assigned'}\n"
        )

        await interaction.edit_original_response(
            content=f'```Congratulations the bot is ready for usage.```\n\n{summary}',
        )
