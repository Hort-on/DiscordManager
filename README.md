# DiscordManager

DiscordManager is a modular Discord server-management bot built with
`discord.py`. It provides an interactive `/mg` management menu for admins and
regular users, with tools for moderation, verification, roles, birthdays,
randomization, and server settings.

The project is organized as a feature-based Python application. Most user
actions are handled through Discord UI components such as buttons, dropdown
menus, modals, and embeds.

## Key Features

- Interactive `/mg` slash command that opens the main bot menu.
- Separate menu flows for regular users, admins, server owners, and superusers.
- Auto moderation for flood spam, repeated links, image spam, and Discord invite
  links.
- Optional timeout or ban actions for detected spam/raid behavior.
- Verification system with persistent Agree/Disagree buttons and role
  assignment.
- Role manager that allows users to add or remove available server roles.
- Hidden roles and hidden channels that are excluded from normal user controls.
- Birthday system with user/admin birthday management and daily congratulations.
- Randomizer tools for random numbers, random words, and random team generation.
- Admin tools for sending messages and server rules through the bot.
- Superuser management for trusted bot managers.
- Message cleanup tools for deleting selected user/channel messages.
- Member leave notifications.
- Server settings stored in an async SQLite database.
- Translation service structure for multi-language bot messages.

## Project Structure

```text
DiscordManager/
+-- cogs/                  # Discord cog entry points
+-- core/                  # Bot setup, controller, navigation, shared containers
+-- database/              # SQLite models, settings storage, database scenarios
+-- event_services/        # Discord event-related services
+-- features/
|   +-- auto_moderation/   # Verification and message moderation
|   +-- for_admins/        # Admin-only modules and flows
|   +-- for_everyone/      # User-facing modules and flows
+-- general_services/      # Logger, translator, cleanup, helper services
+-- ui/                    # Shared Discord UI components
+-- main.py                # Application entry point
+-- requirements.txt       # Python dependencies
```

## Requirements

- Python 3.13 or newer
- A Discord bot token
- Discord bot permissions for moderation, messages, members, roles, and slash
  commands

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
TOKEN=your_discord_bot_token_here
```

## Running the Bot

Start the bot with:

```bash
python main.py
```

When the bot is online, use this slash command in a Discord server:

```text
/mg
```

This opens the interactive management menu.

## Discord Intents

The bot currently enables these intents in `core/bot_config.py`:

- guilds
- members
- messages
- direct messages
- message content
- moderation

Make sure the required privileged intents are also enabled in the Discord
Developer Portal for your bot application.

## Database

The bot uses SQLite through `aiosqlite`. The database file is created at:

```text
database/DATA/assistant_data.sqlite
```

Tables are initialized automatically on startup. Stored data includes guild
settings, system channels, superusers, birthdays, hidden roles, hidden channels,
temporary channels, and groups.

## Current Status

This project is an active Discord bot prototype/application. Many major systems
are already implemented, including moderation, verification, birthdays, role
management, admin menus, and database storage.

Some planned features are still listed in `TODO.md`, such as improved help
documentation, user/server statistics, ticket systems, giveaways, temporary
channels, and group administration.

## Tech Stack

- Python
- discord.py
- aiosqlite
- python-dotenv
- Pillow
- Ruff

## Notes

- The main command is `/mg`.
- Admin-only actions are protected through button protection and superuser
  checks.
- Settings are loaded into memory and synchronized with the SQLite database.
- The codebase follows a modular feature structure, which makes it easier to add
  new bot modules later.
