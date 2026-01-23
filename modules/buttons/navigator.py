from __future__ import annotations

import discord

from typing import TYPE_CHECKING

from database.settings_storage.settings_manager import StorageTarget

if TYPE_CHECKING:
    from core.container import BotContainer


class Navigator:
    def __init__(self, container: BotContainer = None):
        self.container = container

    async def go(
        self,
        target: str,
        interaction: discord.Interaction,
    ):
        if not self.container:
            raise RuntimeError('Navigator: container is not initialized.')

        print('ми в навігаторі')

        view = None

        guild_id = interaction.guild_id
        user_id = interaction.user.id

        print('ми перед матч кейсами')
        match target:
            case 'main_menu':
                try:
                    print('--- Спроба імпорту MainMenuView ---')
                    from modules.buttons.main_button_view import MainMenuView
                    print('--- Імпорт успішний ---')
                except Exception as e:
                    import traceback
                    print("ПОМИЛКА ПРИ ІМПОРТІ:")
                    traceback.print_exc()
                    return

                superusers = self.container.settings.set_storage.for_set_get(
                    target=StorageTarget.SUPERUSERS,
                    guild_id=guild_id
                )

                print('Ми у головному меню')
                view = MainMenuView(
                    superusers=superusers,
                    navigator=self,
                    guild=interaction.guild,
                    user_id=user_id
                )

            case 'admin_menu':
                try:
                    print('--- Спроба імпорту AdminMenuView ---')
                    from modules.buttons.for_admins.admin_menu_view import AdminMenuView
                    print('--- Імпорт успішний ---')
                except Exception as e:
                    import traceback
                    print("ПОМИЛКА ПРИ ІМПОРТІ:")
                    traceback.print_exc()
                    return
                print('Ми у адмін меню')
                config = self.container.settings.dict_storage.for_dict_get_all(
                    target=StorageTarget.SETTINGS,
                    guild_id=guild_id
                )

                view = AdminMenuView(
                    navigator=self,
                    config=config
                )

            case 'birthday_menu':
                try:
                    print('--- Спроба імпорту BirthdayMenuView ---')
                    from modules.buttons.for_admins.birthday_buttons.menu_view import BirthdayMenuView
                    print('--- Імпорт успішний ---')
                except Exception as e:
                    import traceback
                    print("ПОМИЛКА ПРИ ІМПОРТІ:")
                    traceback.print_exc()
                    return
                print('Ми у дні народженні меню')
                view = BirthdayMenuView(
                    navigator=self
                )

            case 'delete_msg_menu':
                try:
                    print('--- Спроба імпорту BirthdayMenuView ---')
                    from modules.buttons.for_admins.delete_message_buttons.menu_view import DeleteMsgMenuView
                    print('--- Імпорт успішний ---')
                except Exception as e:
                    import traceback
                    print("ПОМИЛКА ПРИ ІМПОРТІ:")
                    traceback.print_exc()
                    return
                print('Ми у видалення повідомлень меню')
                view = DeleteMsgMenuView(
                    navigator=self
                )

            case 'superusers_menu':
                try:
                    print('--- Спроба імпорту BirthdayMenuView ---')
                    from modules.buttons.for_admins.superusers_buttons.menu_view import SuperusersMenuView
                    print('--- Імпорт успішний ---')
                except Exception as e:
                    import traceback
                    print("ПОМИЛКА ПРИ ІМПОРТІ:")
                    traceback.print_exc()
                    return
                print('Ми у суперкористувач меню')
                view = SuperusersMenuView(
                    navigator=self
                )

            case 'random_menu':
                try:
                    print('--- Спроба імпорту BirthdayMenuView ---')
                    from modules.buttons.for_users.randomizer.menu_view import RandomModeView
                    print('--- Імпорт успішний ---')
                except Exception as e:
                    import traceback
                    print("ПОМИЛКА ПРИ ІМПОРТІ:")
                    traceback.print_exc()
                    return
                print('Ми у рандомайзер меню')
                view = RandomModeView(
                    navigator=self
                )

            case 'role_manager_menu':
                try:
                    print('--- Спроба імпорту BirthdayMenuView ---')
                    from modules.buttons.for_users.role_manager.menu_view import RoleManagerView
                    print('--- Імпорт успішний ---')
                except Exception as e:
                    import traceback
                    print("ПОМИЛКА ПРИ ІМПОРТІ:")
                    traceback.print_exc()
                    return
                print('Ми у рол менеджер меню')
                view = RoleManagerView(
                    navigator=self
                )

            case 'edit_settings':
                from modules.buttons.for_admins.edit_settings_buttons.services import (
                    SettingsFormatter,
                    SettingSelectorView
                )
                print('Ми у редагуванні повідомлень меню')

                formatter = SettingsFormatter()
                embed = await formatter.format_settings(interaction)

                view = SettingSelectorView(
                    navigator=self,
                    db_factory=self.container.db_factory,
                    yes_no_factory=self.container.yes_no_factory
                )

                await interaction.edit_original_response(
                    embed=embed,
                    view=view
                )
                return

        print('пройшли матч кейси')

        try:
            if view is None:
                print(f'Помилка: View для target "{target}" не була створена!')
                return

            await interaction.edit_original_response(
                content='Оберіть розділ:',
                view=view
            )
        except discord.NotFound as e:
            print(f'Вебхук застарів (404), пробуємо followup... Деталі: {e}')
            try:
                await interaction.followup.send(
                    content='⚠️ Сесія оновлена, виберіть дію ще раз:',
                    view=view,
                    ephemeral=True
                )
                print('Followup успішно надіслано')
            except Exception as followup_error:
                print(f'НАВІТЬ FOLLOWUP НЕ СПРАЦЮВАВ: {followup_error}')
        except Exception as e:
            print(f'КРИТИЧНА ПОМИЛКА НАВІГАЦІЇ: {e}')
            import traceback
            traceback.print_exc()
