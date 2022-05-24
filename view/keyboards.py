from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import view.buttons as buttons

main_menu = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
main_menu.add(KeyboardButton(buttons.add_trip))
main_menu.add(KeyboardButton(buttons.get_excel))

back = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
back.add(KeyboardButton(buttons.back))


def get_order(trip_id: int):
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton(buttons.take_trip, callback_data=f"take_{trip_id}"),
        InlineKeyboardButton(buttons.deny_trip, callback_data=f"deny_{trip_id}")
    )
    return kb


def already_taken(trip_id: int):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(buttons.already_taken, callback_data=f"already_taken_{trip_id}"))
    return kb
