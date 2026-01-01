CONFIG_MSGS = {
    'config_welcome_msg':
        "```👋 Welcome to the configuration!```",

    'initial_msg':
        "```❓ Would you like to start configuring the bot\'s capabilities?```",

    'canceled_msg':
        "``` ❌ configuration cancelled.\n "
        "To start the configuration process again,"
        " please use the command \"/start\".```",

    'sys_ch_msg':
        "```❗ Please select the channel where bot will send system messages.```",

    'congrats_permission_msg':
        "```❓ Would you like the bot to send birthday,"
        " new year congrats, etc.?\n"
        "You will need to choose or create a channel"
        " if you do not have one.```",

    'congrats_ch_msg':
        "```❗ Please select the channel where bot will send"
        " birthday and new year congrats.\n",

    'superusers_msg':
        "```❗ Please type names of trusted users who will be a superuser in your server.\n"
        "It is required for a proper bot service. PLEASE PROVIDE THEIR DISCORD NAMES,"
        "NOT NICKNAMES!```",

    'birthday_feature_msg':
        "```❓ Would you like to enable the birthday feature?\n"
        "The bot will congratulate users on their birthdays."
        " If you provide their names and birthday date.```",

    'verification_feature_msg':
        "```❓ Would you like to enable user verification?\n"
        "New members will need to agree with rules (which you need to write),"
        " before accessing the server.\n"
        "Also you need to create the channel if you don`t have one yet."
        " And typed some rules there.\n"
        "After you finished configuration,"
        " you will need to type \"/mg\" command and press the button"
        "(Set emoji) It will automatically set emoji on the latest message"
        " in the verification channel.```",

    'verification_channel_msg':
        "```❗ Please select the channel that will be used to verify new users.\n"
        "PLEASE NOTE you can change this channel later by typing \"/mg\", then press the button \"edit settings\"```",

    'message_management_feature_msg':
        "```❓ Would you like to enable message management?\n"
        "This allows sending and deleting messages through the bot.```",

    'invitation_check_feature_msg':
        "```❓ Would you like to enable invitation checking?\n"
        "If enabled, invitation messages will be deleted,"
        "if they were sent from users who is not a superuser.```",

    'spam_check_feature_msg':
        "```❓ Would you like to enable spam checking?\n"
        "If enabled, spam messages will be deleted,"
        " and the user who made spam, might be banned```",

    'member_left_feature_msg':
        "```❓ Would you like to enable sending a message into a system"
        " channel when user left the server?```",

    'block_users_feature_msg':
        "```❓ Would you like to allow the bot to block users if they violated the rules?```",

    'send_messages_permission_feature_msg':
        "```❓ Would you like to enable sending messages feature?```",

    'super_user_procedure_msg':
        "```❗ Please enter the usernames NOT NICKNAMES!"
        " of trusted superusers separated by commas e.g. user1, user2:```",

    'audit_log_msg':
        "```❓ Would you like to allow the bot write into audit logs?```",

    'role_management_msg':
        "```❓ Would you like to enable role management?"
        "This will allow users to independently delete or add roles for themselves."
        " You can also hide certain roles so that only administrators can manage them.```",

    'configuration_done_msg':
        "```✅ Congratulations the bot is ready for usage."
        "You can change this settings any time, just type \"/mg\", and press \"edit settings\" button.```",

    'no_configuration_msg':
        "```❌ Settings are not configured for this server yet!```",

    'configuration_exists_msg':
        "```⚠️ You have already configured the bot for this server.```"
}

EDIT_CONFIG_MSGS = {
    'editing_feature_msg':
        "```❓ Would you like to enable or disable {feature} feature?```",

    'congrats_feature_msg':
        "```❓ Would you like to enable or disable congrats feature?```",

    'congrats_channel_msg':
        "```❓ Would you like to change congrats channel?```",

    'system_channel_msg':
        "```❓ Would you like to change system channel?```",

    'verification_feature_msg':
        "```❓ Would you like to enable or disable verification feature?```",

    'verification_channel_msg':
        "```❓ Would you like to change verification channel?```",

    'invitation_check_feature_msg':
        "```❓ Would you like to enable or disable invitation checking?```",

    'spam_check_feature_msg':
        "```❓ Would you like to enable or disable spam checking?```",

    'member_left_feature_msg':
        "```❓ Would you like to enable or disable this feature that allows"
        " the bot to send a notification if any user left the server?```",

    'send_messages_feature_msg':
        "```❓ Would you like to enable or disable sending messages feature?```",

    'config_edit_msg':
        "```❗ Please select settings for editing:```",

    'success_edit_msg':
        "```✅ Changes successfully saved```",

    'failure_edit_msg':
        "```❌ Something went wrong data has not been saved, please try again later.```",
}

GENERAL_MSGS = {
    'ask_channel_msg':
        "```❗ Please select the channel:```",

    'ask_channel_type_msg':
        "```❗ Please select the type of channel:```",

    'user_not_found_msg':
        "```❌ User not found in this server.```",

    'invalid_date_msg':
        "```❌ Invalid date format. Use DD.MM```",

    'user_left_msg':
        "```⚠️ User: {member} has left the server.```",

    'superusers_not_found_msg':
        "```❌ Super users are not assigned for this server.```",

    'not_superuser_msg':
        "```⚠️ You do not have permission to use this feature!```",

    'ask_action_msg':
        "```❗ Please select an action:```"
}

BIRTHDAY_MSGS = {
    'congrats_msg':
        "```Today we celebrate a birthday! 🎉🎂```",

    'success_msg':
        "```✅ The birthday for {member} has been successfully added as {user_birthday}.```",

    'user_exists_msg':
        "```⚠️ For the user: {member}, birthday already set.```"
}

SYSTEM_MSGS = {
    'failure_msg':
        "```❌ Something went wrong, please try again.```",

    'user_blocked_msg':
        "```❌ {user} has been blocked for {duration_in_minutes} minutes because of: {reason}.",

    'permission_declined_msg':
        "```❌ You don't have permission to do this action```",

    'success_message_delete_msg':
        "```✅ Deleted {deleted} messages in {channel}```",

    'ask_private_channel_msg':
        "```❗ Please select the channel where the messages will be sent.:```",

    'ask_private_msg':
        "```❗ Please check your private messages to select a channel.```",

    'send_message_failure_msg':
        "```❗ Failed to send a message to your private messages. Please check your privacy settings.```"
}

ROLES_MSGS = {
    '':
        ""
}

DB_MSGS = {
    'delete_user_msg':
        "```✅ The user with the ID {user_id} successfully deleted from the DB.```",

    'user_not_found_msg':
        "```❌ The user with the ID {user_id} not found in the DB.```",

    'failure_read_msg':
        "❌ Failed to read data from DB",

    'failure_write_msg':
        "❌ Failed to write data into DB",

    'failure_create_table_msg':
        "❌ Failed to create table in the DB",

    'channel_successful_msg':
        "```✅ The channel successfully saved to the DB.```"
}
