import discord
from discord.ext import tasks

from Modules.Birthdays.birthday import Birthday
from Modules.Message_processing.bad_words.bad_words import invitation_pattern, blacklist_word_pattern, \
    blacklist_games_pattern
from Modules.Logging.logging import Logger
from Modules.Fun.joke import check_nickname
from Modules.Administration.verification import VerificationHandler
from Modules.Message_processing.bad_games_handling import handle_bad_games
from Modules.Message_processing.bad_words_handling import BadWordsHandler
from Modules.Message_processing.caps_checking import is_caps
from Modules.Message_processing.invitation_checking import invitation_check
from Modules.Message_processing.spam_handling import handle_spam

from config import TOKEN, bot, SUPERUSERS


logger = Logger()
birthday = Birthday()
bad_words = BadWordsHandler()


# runs the birthday check every 12 hours
@tasks.loop(hours=12)
async def daily_birthday_check():
    await birthday.check_birthday()


@bot.event
async def on_ready():
    if not daily_birthday_check.is_running():
        daily_birthday_check.start()

    check_nickname.start()

    await bot.load_extension('Modules.Management.management')
    await bot.load_extension('Modules.Configuration.starting_cog')

    channel = bot.get_channel(CHANNEL_ID)
    message = await channel.fetch_message(MESSAGE_ID)
    await message.add_reaction('✅')
    await message.add_reaction('❌')

    # allows the bot to send messages
    await send_message()

    print(f'Connected as: {bot.user}.')


# allows the bot to interact with messages
@bot.event
async def on_message(message):
    # It is a function that allows you to send messages on behalf of the bot
    if message.guild is None and message.author.id in SUPERUSERS:
        if hasattr(bot, 'selected_channel') and bot.selected_channel:
            await bot.selected_channel.send(message.content)
        else:
            await message.author.send('```First select the channel for sending messages.```')
        return

    if message.author.bot:
        return

    # gets the name of message's author
    if message.guild:
        nick = message.author.nick if message.author.nick else message.author.name

        # checking if there is an invitation if enabled
        if invitation_pattern.search(message.content):
            await invitation_check(nick, message)

        # cleans the message from various characters for correct analysis
        cleaned_message = bad_words.remove_punctuation(message.content.lower())
        original_message = cleaned_message
        cleaned_message = bad_words.replace_similar_chars(cleaned_message)

        # bad words checking if enabled
        if blacklist_word_pattern.search(cleaned_message):
            await bad_words.check_for_bad_words(message, nick)
        elif blacklist_word_pattern.search(original_message):
            await bad_words.check_for_bad_words(message, nick)

        # bad games checking if enabled
        if blacklist_games_pattern.search(cleaned_message):
            await handle_bad_games(message, nick)
        elif blacklist_games_pattern.search(original_message):
            await handle_bad_games(message, nick)

        # caps checking if enabled
        if len(message.content) > 4 and is_caps(message.content):
            await message.delete()
            await message.channel.send(f"```{nick}, please stop using the caps.```")
            return

        # spam handling if enabled
        await handle_spam(message)

    await bot.process_commands(message)


# allows the bot to react on users reactions if enabled
@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if payload.user_id == bot.user.id:
        return

    # you need to put yours ID
    ukr_message_id = 0
    eng_message_id = 0
    channel_id = 0

    if payload.channel_id == channel_id:
        channel = bot.get_channel(payload.channel_id)

        # logs events if enabled
        if channel is None:
            await logger.error(f"Channel with ID {payload.channel_id} not found.")
            return

        guild = bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)

        # logs events if enabled
        if user is None:
            await logger.error(f"User with ID {payload.user_id} not found.")
            return

        message = await channel.fetch_message(payload.message_id)
        handler = VerificationHandler()

        # checks the ID of the message to which the reaction was added
        if payload.message_id == eng_message_id:
            user_eu = False
        elif payload.message_id == ukr_message_id:
            user_eu = True
        else:
            return

        await handler.handle_verification_reaction(guild, user, user_eu, message, payload.emoji)


# If someone leave your server this function will catch that and will write a log
@bot.event
async def on_member_remove(member: discord.Member):
    logger = Logger()

    await logger.info(f"User: {member} has left the server.")
    channel_id = 0  # The ID of the channel where the message will be sent if someone will leave
    channel = bot.get_channel(int(channel_id))

    if channel is not None:
        await channel.send(f"User: {member} has left the server.")
    else:
        await logger.error(f"Channel with the ID {channel} not found.")
        return


# The command to view all available commands
@bot.command(help='Command to view all available commands.', hidden=True)
async def help(ctx):
    help_message = """
    ```
    List of commands:
            *****For admins ONLY*****

    !mg     - Opens management menu.
    ```
    """
    await ctx.send(help_message)


bot.run(TOKEN)
