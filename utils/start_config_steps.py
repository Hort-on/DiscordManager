STEPS = [
    ('initial_msg', None, 'ChannelTypeView'),
    ('birthday_feature_msg', 'birthday_enabled', 'YesNoView'),
    ('congrats_feature_msg', 'congrats_enabled', 'YesNoView'),
    ('congrats_channel_msg', 'congrats_channel_id', 'ChannelTypeView'),
    ('verification_feature_msg', 'verification_enabled', 'YesNoView'),
    ('verification_channel_msg', 'verification_channel_id', 'ChannelTypeView'),
    ('system_channel_msg', 'system_channel_id', 'ChannelTypeView'),
    ('block_users_feature_msg', 'blocking_users_enabled', 'YesNoView'),
    ('invitation_check_feature_msg', 'invitation_checking_enabled', 'YesNoView'),
    ('spam_check_feature_msg', 'spam_checking_enabled', 'YesNoView'),
    ('member_left_feature_msg', 'member_left_enabled', 'YesNoView'),
    ('send_messages_feature_msg', 'send_messages_enabled', 'YesNoView'),
    ('audit_log_msg', 'write_audit_log_enabled', 'YesNoView'),
    ('role_management_msg', 'role_management_enabled', 'YesNoView'),
    ('superusers_msg', None, 'SuperUsers')
]

STEP_DEPENDENCIES = {
    'verification_channel_id': 'verification_enabled',
    'congrats_channel_id': 'congrats_enabled',
}
