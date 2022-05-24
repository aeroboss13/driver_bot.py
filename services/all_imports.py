from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import config
import view.messages as messages
import view.keyboards as keyboards
import view.buttons as buttons
import database.db_work as database
import logging

bot = Bot(config.TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


logging.basicConfig(filename="log.log", level=logging.INFO)
log = logging.getLogger("bot")
