import sqlite3

import aiogram.utils.exceptions
from aiogram import types
from aiogram.utils import executor

import services.driver as driver
import services.manager as manager
from services.all_imports import *
from services.global_functions import error_except


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    """
    Пользователь отправил команду /start, переводим его в главное меню

    :param message: Объект сообщения
    """

    manager_id = message.from_user.id

    if manager_id != config.MANAGER_ID:
        return

    try:
        database.add_user(manager_id)
        await manager.switch_to_main_menu(manager_id)
    except sqlite3.IntegrityError:
        await manager.switch_to_main_menu(manager_id)
    except Exception as error:
        await error_except(manager_id, error)


@dp.message_handler(content_types=["text"])
async def all_messages(message: types.Message):
    """
    Пользователь отправил текстовое сообщение

    :param message: Объект сообщения
    """
    manager_id = message.from_user.id

    if manager_id != config.MANAGER_ID:
        return

    text = message.text
    try:
        await manager.fsm(manager_id, text)
    except Exception as error:
        await error_except(manager_id, error)


@dp.callback_query_handler()
async def callback_query_handler(query: types.CallbackQuery):
    user_id = query.from_user.id
    user_full_name = query.from_user.full_name
    data = query.data
    message_id = query.message.message_id
    callback_query_id = query.id

    try:
        await driver.callback_handler(
            driver_id=user_id,
            driver_full_name=user_full_name,
            data=data,
            message_id=message_id,
            callback_query_id=callback_query_id)
    except aiogram.utils.exceptions.InvalidQueryID:
        pass
    except aiogram.utils.exceptions.MessageToEditNotFound:
        pass
    except Exception as error:
        await error_except(user_id, error)


if __name__ == '__main__':
    executor.start_polling(dp)
