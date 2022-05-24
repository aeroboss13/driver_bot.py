import datetime
import sqlite3

import config

connection = sqlite3.connect("database/database.db", check_same_thread=False)


def get_step(manager_id: int) -> int:
    """
    Возвращает шаг работы с ботом для менеджера

    :param manager_id: Telegram ID менеджера
    """

    cursor = connection.cursor()

    request = "SELECT step FROM managers WHERE telegram_id=?"
    result = cursor.execute(request, (manager_id,)).fetchone()

    return result[0]


def set_step(manager_id: int, step: int):
    """
    Изменяет шаг работы с ботом для менеджера

    :param manager_id: Telegram ID менеджера
    :param step: Шаг работы с ботом
    """

    cursor = connection.cursor()

    request = "UPDATE managers SET step=? WHERE telegram_id=?"
    cursor.execute(request, (step, manager_id))
    connection.commit()


def add_user(manager_id: int):
    """
    Добавляет менеджера в базу данных

    :param manager_id: Telegram ID менеджера
    """

    cursor = connection.cursor()

    request = "INSERT INTO managers(telegram_id) VALUES (?)"
    cursor.execute(request, (manager_id,))
    connection.commit()


def delete_not_public_trip():
    """
    Удаляет непубличную поездку
    """

    cursor = connection.cursor()
    request = "DELETE FROM trips WHERE state=?"
    cursor.execute(request, (config.TripsStates.IN_PROCESS,))
    connection.commit()


def create_trip(departure_point: str):
    """
    Создает новую поездку

    :param departure_point: Точка отправления
    """

    creation_date = datetime.datetime.now()

    cursor = connection.cursor()
    request = "INSERT INTO trips(departure_point, creation_date, state) VALUES(?, ?, ?)"
    cursor.execute(request, (departure_point, creation_date, config.TripsStates.IN_PROCESS))
    connection.commit()


def get_not_public_trip():
    """
    Возвращает ID неопубликованной поездки
    """

    cursor = connection.cursor()
    request = "SELECT id FROM trips WHERE state=?"
    result = cursor.execute(request, (config.TripsStates.IN_PROCESS,)).fetchone()
    return result[0] if result else result


def set_arrival_point(trip_id: int, arrival_point: str):
    """
    Устанавливает точку прибытия

    :param trip_id: ID поездки
    :param arrival_point: Точка прибытия
    """

    cursor = connection.cursor()
    request = "UPDATE trips SET arrival_point=? WHERE id=?"
    cursor.execute(request, (arrival_point, trip_id))
    connection.commit()


def set_time_for_trip(trip_id: int, trip_time: str):
    """
    Устанавливает время поездки

    :param trip_id: ID поездки
    :param trip_time: Время поездки
    """

    cursor = connection.cursor()
    request = "UPDATE trips SET time=? WHERE id=?"
    cursor.execute(request, (trip_time, trip_id))
    connection.commit()


def set_price_for_trip(trip_id: int, trip_price: int):
    """
    Устанавливает стоимость поездки

    :param trip_id: ID поездки
    :param trip_price: Стоимость поездки
    """

    cursor = connection.cursor()
    request = "UPDATE trips SET price=? WHERE id=?"
    cursor.execute(request, (trip_price, trip_id))
    connection.commit()


def publish_trip(trip_id: int):
    """
    Публикует поездку

    :param trip_id: ID поездки
    """

    cursor = connection.cursor()
    request = "UPDATE trips SET state=? WHERE id=?"
    cursor.execute(request, (config.TripsStates.PUBLIC, trip_id))
    connection.commit()


def get_info_about_trip(trip_id: int):
    """
    Возвращает всю информацию о поездке

    :param trip_id: ID поездки
    """

    cursor = connection.cursor()
    request = "SELECT id, departure_point, arrival_point, time, price, creation_date, state, additional_info FROM trips WHERE id=?"
    result = cursor.execute(request, (trip_id,)).fetchone()
    return {
        "id": trip_id,
        "departure_point": result[1],
        "arrival_point": result[2],
        "time": result[3],
        "price": result[4],
        "creation_date": result[5],
        "state": result[6],
        "additional_info": result[7]
    }


def check_if_valid_trip_id(trip_id: int) -> bool:
    """
    Проверяет, есть ли ID такой поездки в базе данных

    :param trip_id: ID поездки
    """

    cursor = connection.cursor()
    request = "SELECT id FROM trips WHERE id=?"
    result = cursor.execute(request, (trip_id,)).fetchone()
    return True if result else False


def get_response_answer_for_trip(trip_id: int, driver_id: int):
    """
    Возвращает ответ водителя на заказ

    :param trip_id: ID заявки на поездку
    :param driver_id: Telegram ID водителя
    """

    cursor = connection.cursor()
    request = "SELECT response_type FROM responses WHERE trip_id=? AND driver_id=?"
    result = cursor.execute(request, (trip_id, driver_id)).fetchone()
    return result[0] if result else result


def create_trip_response(trip_id: int, driver_id: int, response_type: int):
    """
    Добавляет в базу данных ответ на поездку от водителя

    :param trip_id: ID поездки
    :param driver_id: Telegram ID водителя
    :param response_type: Тип ответа: принял или отклонил
    """

    cursor = connection.cursor()
    request = "INSERT INTO responses(trip_id, driver_id, response_type) VALUES(?, ? ,?)"
    cursor.execute(request, (trip_id, driver_id, response_type))
    connection.commit()


def set_trip_state(trip_id: int, state: int):
    """
    Устанавливает статус поездки

    :param trip_id: ID поездки
    :param state: Статус поездки
    """

    cursor = connection.cursor()
    request = "UPDATE trips SET state=? WHERE id=?"
    cursor.execute(request, (state, trip_id))
    connection.commit()


def set_additional_info(trip_id: int, additional_info: str):
    """
    Устанавливает дополнительную информацию о поездке

    :param trip_id: ID поездки
    :param additional_info: Дополнительная информация
    """

    cursor = connection.cursor()
    request = "UPDATE trips SET additional_info=? WHERE id=?"
    cursor.execute(request, (additional_info, trip_id))
    connection.commit()


def get_all_trips():
    """
    Возвращает все поездки
    """

    cursor = connection.cursor()
    request = "SELECT departure_point, arrival_point, time, price, additional_info, state FROM trips"
    result = cursor.execute(request).fetchall()
    return result


def check_if_driver(driver_id: int) -> bool:
    """
    Проверяет, есть ли водитель в базе данных

    :param driver_id: Telegram ID водителя
    """

    cursor = connection.cursor()
    request = "SELECT driver_id FROM drivers WHERE driver_id=?"
    result = cursor.execute(request, (driver_id,)).fetchone()
    return True if result else False


def add_driver(driver_id: int, driver_full_name: str):
    """
    Добавляет водителя в базу данных

    :param driver_id: Telegram ID водителя
    :param driver_full_name: Полное имя водителя
    """

    cursor = connection.cursor()
    request = "INSERT INTO drivers(driver_id, driver_full_name) VALUES(?, ?)"
    cursor.execute(request, (driver_id, driver_full_name))
    connection.commit()


def update_drivers_full_name(driver_id: int, driver_full_name: str):
    """
    Обновляет имя водителя

    :param driver_id: Telegram ID водителя
    :param driver_full_name: Полное имя водителя
    """

    cursor = connection.cursor()
    request = "UPDATE drivers SET driver_full_name=? WHERE driver_id=?"
    cursor.execute(request, (driver_full_name, driver_id))
    connection.commit()