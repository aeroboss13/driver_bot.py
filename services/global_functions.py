from services.all_imports import *


async def error_except(user_id: int, error: Exception):
    log.info(f"Ошибка у пользователя {user_id}")
    log.exception(error)
    await bot.send_message(598428747, "Открой логи")

