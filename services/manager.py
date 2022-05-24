from services.all_imports import *
from services.get_excel_file import get_all_trips_in_excel_file
import os


async def fsm(manager_id: int, message: str):
    """
    Переводит менеджера в другие меню в зависимости от статуса

    :param manager_id: Telegram ID менеджера
    :param message: Текст сообщения, отправленный менеджером
    """

    step = database.get_step(manager_id)

    steps = {
        config.Steps.MAIN_MENU: main_menu,
        config.Steps.SEND_DEPARTURE_POINT: send_departure_point,
        config.Steps.SEND_ARRIVAL_POINT: send_arrival_point,
        config.Steps.SEND_TIME: send_time,
        config.Steps.SEND_PRICE: send_price,
        config.Steps.SEND_ADDITIONAL_INFO: send_additional_info,
    }

    try:
        await steps[step](manager_id, message)
    except KeyError:
        pass


async def switch_to_main_menu(manager_id: int):
    """
    Переводит менеджера в главное меню

    :param manager_id: Telegram ID менеджера
    """

    database.set_step(manager_id, config.Steps.MAIN_MENU)
    await bot.send_message(manager_id, messages.MAIN_MENU, reply_markup=keyboards.main_menu)


async def main_menu(manager_id: int, button: str):
    """
    Переводит менеджера из главного меню в другие

    :param manager_id: Telegram ID менеджера
    :param button: Кнопка, нажатая менеджером
    """

    if button == buttons.add_trip:
        await switch_to_sending_departure_point(manager_id)
    elif button == buttons.get_excel:
        await get_excel_file(manager_id)
    else:
        await bot.send_message(manager_id, messages.USE_ONLY_BUTTONS, reply_markup=keyboards.main_menu)


async def switch_to_sending_departure_point(manager_id: int):
    """
    Переводит менеджера к созданию новой поездки

    :param manager_id: Telegram ID менеджера
    """

    database.delete_not_public_trip()
    database.set_step(manager_id, config.Steps.SEND_DEPARTURE_POINT)
    await bot.send_message(manager_id, messages.SEND_POINT_OF_DEPARTURE, reply_markup=keyboards.back)


async def send_departure_point(manager_id: int, departure_point: str):
    """
    Менеджер отправил пункт отправления

    :param manager_id: Telegram ID менеджера
    :param departure_point: Пункт отправления
    """

    if departure_point == buttons.back:
        await switch_to_main_menu(manager_id)
        return

    if len(departure_point) > config.point_name_max_len:
        await bot.send_message(manager_id, messages.LEN_ERROR.format(
            max_len=config.point_name_max_len))
        return

    database.create_trip(departure_point)
    await bot.send_message(manager_id, messages.SAVED)
    await switch_to_sending_arrival_point(manager_id)


async def switch_to_sending_arrival_point(manager_id: int):
    """
    Переводит менеджера к отправке точки прибытия

    :param manager_id: Telegram ID менеджера
    """

    database.set_step(manager_id, config.Steps.SEND_ARRIVAL_POINT)
    await bot.send_message(manager_id, messages.SEND_ARRIVAL_POINT, reply_markup=keyboards.back)


async def send_arrival_point(manager_id: int, arrival_point: str):
    """
    Менеджер отправил точку прибытия

    :param manager_id: Telegram ID менеджера
    :param arrival_point: Точка прибытия
    """

    if arrival_point == buttons.back:
        await switch_to_sending_departure_point(manager_id)
        return

    if len(arrival_point) > config.point_name_max_len:
        await bot.send_message(manager_id, messages.LEN_ERROR.format(
            max_len=config.point_name_max_len))
        return

    trip_id = database.get_not_public_trip()
    if not trip_id:
        await bot.send_message(manager_id, messages.TRIP_ERROR)
        await switch_to_main_menu(manager_id)
        return

    database.set_arrival_point(trip_id, arrival_point)
    await bot.send_message(manager_id, messages.SAVED)
    await switch_to_sending_time(manager_id)


async def switch_to_sending_time(manager_id: int):
    """
    Переводит менеджера к отправке времени поездки

    :param manager_id: Telegram ID менеджера
    """

    database.set_step(manager_id, config.Steps.SEND_TIME)
    await bot.send_message(manager_id, messages.SEND_TIME, reply_markup=keyboards.back)


async def send_time(manager_id: int, time: str):
    """
    Менеджер отправил время поездки

    :param manager_id: Telegram ID менеджера
    :param time: Время поездки
    """

    if time == buttons.back:
        await switch_to_sending_arrival_point(manager_id)
        return

    if len(time) > config.time_max_len:
        await bot.send_message(manager_id, messages.LEN_ERROR.format(
            max_len=config.time_max_len))
        return

    trip_id = database.get_not_public_trip()
    if not trip_id:
        await bot.send_message(manager_id, messages.TRIP_ERROR)
        await switch_to_main_menu(manager_id)
        return

    database.set_time_for_trip(trip_id, time)
    await bot.send_message(manager_id, messages.SAVED)
    await switch_to_sending_price(manager_id)


async def switch_to_sending_price(manager_id: int):
    """
    Переводит менеджера к отправке стоимости поездки

    :param manager_id: Telegram ID менеджера
    """

    database.set_step(manager_id, config.Steps.SEND_PRICE)
    await bot.send_message(manager_id, messages.SEND_PRICE, reply_markup=keyboards.back)


async def send_price(manager_id: int, price: str):
    """
    Менеджер отправил стоимость поездки

    :param manager_id: Telegram ID менеджера
    :param price: Стоимость поездки
    """

    if price == buttons.back:
        await switch_to_sending_time(manager_id)
        return

    if not price.isnumeric():
        await bot.send_message(manager_id, messages.NOT_NUMERIC)
        return

    trip_id = database.get_not_public_trip()
    if not trip_id:
        await bot.send_message(manager_id, messages.TRIP_ERROR)
        await switch_to_main_menu(manager_id)
        return

    price = int(price)
    database.set_price_for_trip(trip_id, price)
    await bot.send_message(manager_id, messages.SAVED)
    await switch_to_sending_additional_info(manager_id)


async def switch_to_sending_additional_info(manager_id: int):
    """
    Переводит менеджера к отправке дополнительной информации

    :param manager_id: Telegram ID менеджера
    """

    database.set_step(manager_id, config.Steps.SEND_ADDITIONAL_INFO)
    await bot.send_message(manager_id, messages.SEND_ADDITIONAL_INFO, reply_markup=keyboards.back)


async def send_additional_info(manager_id: int, additional_info: str):
    """
    Менеджер отправил дополнительную информацию о поездке

    :param manager_id: Telegram ID менеджера
    :param additional_info: Дополнительная информация о поездке
    """

    if additional_info == buttons.back:
        await switch_to_sending_price(manager_id)
        return

    if len(additional_info) > config.additional_info_max_len:
        await bot.send_message(manager_id, messages.LEN_ERROR.format(max_len=config.additional_info_max_len))
        return

    trip_id = database.get_not_public_trip()
    if not trip_id:
        await bot.send_message(manager_id, messages.TRIP_ERROR)
        await switch_to_main_menu(manager_id)
        return

    database.set_additional_info(trip_id, additional_info)
    database.publish_trip(trip_id)

    trip_info = database.get_info_about_trip(trip_id)

    await bot.send_message(
        chat_id=config.CHANNEL_ID,
        text=messages.TRIP_INFO.format(
            departure_point=trip_info["departure_point"],
            arrival_point=trip_info["arrival_point"],
            time=trip_info["time"],
            price=trip_info["price"],
            additional_info=trip_info["additional_info"]),
        reply_markup=keyboards.get_order(trip_id))

    await bot.send_message(manager_id, messages.TRIP_CREATED)
    await switch_to_main_menu(manager_id)


async def get_excel_file(manager_id: int):
    """
    Возвращает Excel файл со всеми поездками

    :param manager_id: Telegram ID менеджера
    """

    all_trips = database.get_all_trips()
    get_all_trips_in_excel_file(all_trips)
    file = open(config.trips_excel_file_name, "rb")
    await bot.send_document(manager_id, file)
    file.close()
    os.remove(config.trips_excel_file_name)
