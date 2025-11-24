import time
from Modules.Administration.user_auto_ban import block_user

user_message_info = {}
user_warning_count = {}
user_warning_time = {}

user_spam_data = {}


async def handle_spam(message):
    user_id = message.author.id
    current_time = time.time()

    # Ініціалізувати дані користувача якщо потрібно
    if user_id not in user_spam_data:
        user_spam_data[user_id] = {'messages': [], 'warnings': 0}

    user_data = user_spam_data[user_id]

    # Додати повідомлення та очистити старі
    user_data['messages'].append(current_time)
    user_data['messages'] = [t for t in user_data['messages'] if current_time - t <= 3]

    msg_count = len(user_data['messages'])

    # Перевірити на спам
    if msg_count == 3:
        user_data['warnings'] += 1
        await warn_spam(message)
    elif msg_count >= 5 and user_data['warnings'] >= 1:
        await block_user(message, 5, 'Спам')
        user_data['warnings'] = 0
    elif msg_count >= 5:
        user_data['warnings'] += 1


async def warn_spam(message):
    await message.delete()
    await message.channel.send(f'```{message.author.nick}, Please stop spamming otherwise you will be banned!```',
                           delete_after=1200)
