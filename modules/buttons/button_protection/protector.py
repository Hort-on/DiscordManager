import discord

from services.other_services.is_superuser import IsSuperuserService


class ButtonPermissionService:
    admin_service = IsSuperuserService()

    def has_access(
            self,
            interaction: discord.Interaction,
            scope: str
    ) -> bool:
        if scope == 'user':
            return True

        if scope == 'admin':
            return self.admin_service.is_superuser(
                guild_id=interaction.guild_id,
                user_id=interaction.user.id
            )

        return False
