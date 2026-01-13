import discord


def get_member_by_name(interaction: discord.Interaction, username: str) -> discord.Member:
    member = discord.utils.find(
        lambda m: m.name.lower() == username.lower()
        or m.display_name.lower() == username.lower(),
        interaction.guild.members
    )

    return member
