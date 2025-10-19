from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def join_keyboard() -> InlineKeyboardMarkup:
    """Кнопка 'Вступить 🟢' для приватного чата с ботом."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Вступить 🟢", callback_data="join")]
        ]
    )

def courier_menu() -> InlineKeyboardMarkup:
    """Меню для роли courier."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Профиль", callback_data="m:profile")],
            [InlineKeyboardButton(text="Памятка", callback_data="m:help")],
            [InlineKeyboardButton(text="Связаться с супервайзером", callback_data="m:contact")],
        ]
    )

def supervisor_menu() -> InlineKeyboardMarkup:
    """Меню для роли supervisor."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Пользователи", callback_data="s:users")],
            [InlineKeyboardButton(text="Назначить роль", callback_data="s:set_role")],
            [InlineKeyboardButton(text="Снять роль", callback_data="s:unset_role")],
        ]
    )

def owner_menu() -> InlineKeyboardMarkup:
    """Меню для роли owner."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назначить роль", callback_data="o:set_role")],
            [InlineKeyboardButton(text="Снять роль", callback_data="o:unset_role")],
            [InlineKeyboardButton(text="Экспорт", callback_data="o:export")],
            [InlineKeyboardButton(text="Логи", callback_data="o:logs")],
        ]
    )
