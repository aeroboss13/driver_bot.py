import aiogram.utils.exceptions

from services.all_imports import *


async def callback_handler(driver_id: int, driver_full_name: str, data: str, message_id: int,
                           callback_query_id: int):
    """
    Реагирует на нажатие водителем инлайн кнопки

    :param driver_id: Telegram ID водителя
    :param driver_full_name: Полное имя водителя
    :param data: Данные из инлайн кнопки
    :param message_id: ID сообщения, с которого нажата инлайн кнопка
    :param callback_query_id: ID колбек очереди, по которой бот будет отвечать водителю
    """

    if "take" in data or "deny" in data:
        trip_id = int(data.split("_")[-1])
        state = config.ResponseTypes.ACCEPT if "take" in data else config.ResponseTypes.DENY
        message = messages.YOU_ACCEPTED_TRIP if "take" in data else messages.YOU_DENIED_TRIP
        await answer_to_trip_snippet(
            driver_id=driver_id,
            driver_full_name=driver_full_name,
            trip_id=trip_id,
            message_id=message_id,
            callback_query_id=callback_query_id,
            message=message,
            state=state
        )


async def answer_to_trip_snippet(driver_id: int, driver_full_name: str, trip_id: int, message_id: int,
                                 callback_query_id: int, message: str,
                                 state: int):
    """
    Сниппет кода для ответа водителя на заказ

    :param driver_id: Telegram ID водителя
    :param driver_full_name: Полное имя водителя
    :param trip_id: ID поездки
    :param message_id: ID сообщения, с которого нажата инлайн кнопка
    :param callback_query_id: ID колбек очереди, по которой бот будет отвечать водителю
    :param message: Сообщение, которое необходимо посылать
    :param state: Статус, заявки, который необходимо ставить
    """

    # Если нет ID такой заявки в базе данных, то что-то пошло не так, удаляем сообщение
    if not database.check_if_valid_trip_id(trip_id):
        try:
            await bot.delete_message(config.CHANNEL_ID, message_id)
        except aiogram.exceptions.MessageCantBeDeleted:
            pass
        return

    # Мы можем принять запрос от водителя только на заявку, которая еще никем не взята
    if database.get_info_about_trip(trip_id)["state"] != config.TripsStates.PUBLIC:
        await already_taken_trip(trip_id, message_id)
        return

    driver_answer = database.get_response_answer_for_trip(trip_id, driver_id)
    # Если этот водитель еще не отвечал на заказ
    if not driver_answer:
        database.create_trip_response(trip_id, driver_id, state)

        # Если статус ответа - принятие заявки, то закрываем эту заявку
        if state == config.ResponseTypes.ACCEPT:
            database.set_trip_state(trip_id, config.TripsStates.TAKEN)
            await save_driver_full_name(driver_id, driver_full_name)
            await already_taken_trip(trip_id, message_id)
            await send_response_to_manager(trip_id, driver_full_name)

        await bot.answer_callback_query(callback_query_id, message)
        return

    # Если водитель уже отвечал на заказ
    message_for_driver = {
        config.ResponseTypes.ACCEPT: messages.ALREADY_ACCEPTED_TRIP,
        config.ResponseTypes.DENY: messages.ALREADY_DENIED_TRIP}[driver_answer]

    await bot.answer_callback_query(callback_query_id, message_for_driver)


async def already_taken_trip(trip_id: int, message_id: int):
    """
    Изменяет клавиатуру у сообщения с заказом, на который нашелся водитель

    :param trip_id: ID поездки
    :param message_id: ID сообщения, с которого нажата инлайн кнопка
    """

    try:
        await bot.edit_message_reply_markup(
            chat_id=config.CHANNEL_ID,
            message_id=message_id,
            reply_markup=keyboards.already_taken(trip_id))
    except aiogram.utils.exceptions.MessageNotModified:
        pass


async def save_driver_full_name(driver_id: int, driver_full_name: str):
    """
    Сохраняет полное имя водителя в базу данных

    :param driver_id: Telegram ID водителя
    :param driver_full_name: Полное имя водителя
    """

    if not database.check_if_driver(driver_id):
        database.add_driver(driver_id, driver_full_name)
        return

    database.update_drivers_full_name(driver_id, driver_full_name)


async def send_response_to_manager(trip_id: int, driver_full_name: str):
    """
    Отправляет сообщение об отклике менеджеру

    :param trip_id: ID поездки
    :param driver_full_name: Полное имя водителя
    """

    trip_info = database.get_info_about_trip(trip_id)

    await bot.send_message(
        chat_id=config.MANAGER_ID,
        text=messages.TRIP_ACCEPTED.format(
            full_name=driver_full_name,
            departure_point=trip_info["departure_point"],
            arrival_point=trip_info["arrival_point"],
            time=trip_info["time"],
            price=trip_info["price"],
            additional_info=trip_info["additional_info"]))
