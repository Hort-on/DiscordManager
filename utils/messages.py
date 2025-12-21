CONFIG_MESSAGES = {
    'initial_msg':
        "```Would you like to start configuring the bot\'s capabilities?```",

    'canceled_msg':
        "```configuration cancelled.\n "
        "To start the configuration process again,"
        " please use the command (!start).```",

    'sys_ch_msg':
        "```Please select the channel where bot will send system messages.```",

    'congrats_permission_msg':
        "```Would you like the bot to send birthday,"
        " new year congrats, etc.?\n"
        "You will need to choose or create a channel"
        " if you do not have one.```",

    'congrats_ch_msg':
        "```Please select the channel where bot will send"
        " birthday and new year congrats.\n"
        "If you did not allow the bot to send the congrats messages, then just press skip"
        " (No button)```",

    'superusers_msg':
        "```Please type names of trusted users who will be a superuser in your server.\n"
        "It is required for a proper bot service. PLEASE PROVIDE THEIR DISCORD NAMES,"
        "NOT NICKNAMES!```",

    'birthday_feature_msg':
        "```Would you like to enable the birthday feature?\n"
        "The bot will congratulate users on their birthdays."
        " If you provide their names and birthday date.```",

    'verification_feature_msg':
        "```Would you like to enable user verification?\n"
        "New members will need to agree with rules (which you need to write),"
        " before accessing the server.\n"
        "Also you need to create the channel if you don`t have one yet."
        " And typed some rules there.\n"
        "After you finished configuration,"
        " you will need to type (!mg) command and press the button"
        "(Set emoji) It will automatically set emoji on the latest message"
        " in the verification channel.```",

    'message_management_feature_msg':
        "```Would you like to enable message management?\n"
        "This allows sending and deleting messages through the bot.```",

    'invitation_check_feature_msg':
        "```Would you like to enable invitation checking?\n"
        "If enabled, invitation messages will be deleted,"
        "if they were sent from users who is not a superuser.```",

    'spam_check_feature_msg':
        "```Would you like to enable spam checking?\n"
        "If enabled, spam messages will be deleted,"
        " and the user who made spam, might be banned```",

    'member_left_feature_msg':
        "```Would you like to enable sending a message into a system"
        " channel when user left the server?```",

    'block_users_feature_msg':
        "```Would you like to allow the bot to block users if they violated the rules?```",

    'send_messages_permission_feature_msg':
        "```Would you like to enable sending messages feature?```",

    'set_permissions_feature_msg':
        "```Would you like to enable setting permissions?```",

    'super_user_procedure_msg':
        "```Please enter the usernames NOT NICKNAMES!"
        " of trusted superusers separated by commas e.g. user1, user2:```"
}

EDIT_CONFIG_MESSAGES = {
    'editing_feature_msg':
        "Would you like to enable or disable {} feature?",

    'congrats_feature_msg':
        "Would you like to enable or disable congrats feature?",

    'congrats_channel_msg':
        "Would you like to change congrats channel?",

    'system_channel_msg':
        "Would you like to change system channel?",

    'verification_feature_msg':
        "Would you like to enable or disable verification feature?",

    'verification_channel_msg':
        "Would you like to change verification channel?",

    'invitation_check_feature_msg':
        "Would you like to enable or disable invitation checking?",

    'spam_checking_feature_msg':
        "Would you like to enable or disable spam checking?",

    'member_left_feature_msg':
        "Would you like to enable or disable this feature that allows"
        " the bot to send a notification if any user left the server?",

    'set_permissions_feature_msg':
        "Would you like to enable or disable this feature?",

    'sending_messages_feature_msg':
        "Would you like to enable or disable sending messages feature?",

    'config_editing_msg':
        "Please select settings for editing:",

    'success_editing_msg':
        "Changes successfully saved",

    'failed_editing_msg':
        "Something went wrong data has not been saved, please try again later.",
}

GENERAL_MESSAGES = {
    'ask_channel_msg':
        "Please select the channel:",

    'ask_channel_type_msg':
        "Please select the type of channel:",
}