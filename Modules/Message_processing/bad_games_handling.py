from Modules.Administration.user_auto_ban import block_user

bad_games_warnings = set()
EXCLUDED_CHANNEL = 1324119438202638337


async def handle_bad_games(message, nick):
    # Ранній вихід для виключеного каналу
    if message.channel.id == EXCLUDED_CHANNEL:
        return

    user_id = message.author.id
    is_repeat_offense = user_id in bad_games_warnings

    # Видалити повідомлення якщо дозволено
    await message.delete()

    if is_repeat_offense:
        # Блокувати за повторне порушення
        bad_games_warnings.discard(user_id)
        await block_user(message, 60, "Violation of the rule: 4.3", True)
    else:
        # Попередити (перше порушення або блокування вимкнено)
        bad_games_warnings.add(user_id)
        warning = f"```{nick}, discussion, mention, or advertisement of russian games is prohibited!```"
        await message.channel.send(warning)
