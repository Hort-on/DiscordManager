EDIT_CONFIG_MSGS = {
    'editing_feature_msg':
        "```❓ Would you like to enable or disable {feature} feature?```",

    'congrats_feature_msg':
        "```❓ Would you like to enable or disable congrats feature?```",

    'congrats_channel_msg':
        "```❓ Would you like to change congrats channel?```",

    'notification_channel_msg':
        "```❓ Would you like to change notification channel?```",

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
        "```❗ Please select an action:```",

    'no_msg_found':
        "⚠️ No message was found in this channel {channel}"
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
