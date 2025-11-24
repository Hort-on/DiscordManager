STEPS = [
    ('initial_msg', None, 'ChannelTypeView'),
    ('sys_ch_msg', 'system_channel_id', 'ChannelTypeView'),
    ('congrats_permission_msg', 'congrats_enabled', 'YesNoView'),
    ('congrats_ch_msg', 'congrats_channel_id', 'ChannelTypeView'),
    ('birthday_feature_msg', 'birthday_enabled', 'YesNoView'),
    ('verification_feature_msg', 'verification_enabled', 'YesNoView'),
    ('invitation_check_feature_msg', 'invitation_checking_enabled', 'YesNoView'),
    ('spam_check_feature_msg', 'spam_checking_enabled', 'YesNoView'),
    ('member_left_feature_msg', 'member_left_enabled', 'YesNoView'),
    ('block_users_feature_msg', 'blocking_users_enabled', 'YesNoView'),
    ('send_messages_permission_feature_msg', 'sending_messages_enabled', 'YesNoView'),
    ('set_permissions_feature_msg', 'set_permissions_enabled', 'YesNoView'),
    ('superusers_msg', None, 'SuperUsers')
]