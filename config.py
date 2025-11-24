from discord.ext import commands
import discord
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

SUPERUSERS = [] # Insert your superusers' IDs here

HIDDEN_CHANNELS = [] # Insert IDs of channels you want to hide from selection in management

MODERATOR_CHANNEL = int(os.getenv('MODERATOR_CHANNEL')) # Replace with the ID of your moderation channel

intents = discord.Intents.all()

# Modules configuration
MODULES = {

    # Message processing
    'spam_handling': True, # Spam protection
    'bad_words_handling': True, # Checks if user uses bad words
    'bad_games_handling': True, # Checks if user mentioned prohibited games
    'invitation_checking': True, # Blocks all the invitation from every one but superusers
    'caps_handling': True, # Caps protection
    'putting_reactions': False, # Puts reaction on selected messages (using only for verification)

    # Birthday day
    'birthdays': True,

    # Logging
    'logging': True, # Allows the bot to log events
    'member_left': True, # Allows the bot logging if someone left your server
}


bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
