import discord
from discord.ext import tasks
from config import bot

TARGET_USER_ID = 0 # Set the ID of the user you want the bot to rename
TARGET_NAME = '' # Insert the name you want the user to be renamed to

@tasks.loop(seconds=30)
async def check_nickname():
    for guild in bot.guilds:
        member = guild.get_member(TARGET_USER_ID)
        if member is None:
            continue

        if member.nick == TARGET_NAME:
            continue

        try:
            await member.edit(nick=TARGET_NAME)
        except discord.Forbidden:
            return
        except Exception as e:
            print(f"The error has been occurred: {e}")
