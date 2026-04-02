import discord


def get_member_by_name(guild: discord.Guild, username: str) -> discord.Member | None:
    member = discord.utils.find(
        lambda m: m.name.lower() == username.lower()
        or m.display_name.lower() == username.lower(),
        guild.members
    )

    return member or None
