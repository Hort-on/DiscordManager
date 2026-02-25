from enum import Enum, auto


class Route(str, Enum):
    MAIN_MENU = auto()
    ADMIN_MENU = auto()
    SETTINGS_MENU = auto()
    BIRTHDAY_MENU = auto()
    SUPERUSERS_MENU = auto()
    RANDOM_MENU = auto()
    ROLE_MANAGER_MENU = auto()
    HIDDEN_CHANNELS_MENU = auto()
    HIDDEN_ROLES_MENU = auto()
    SYSTEM_CHANNELS_MENU = auto()
