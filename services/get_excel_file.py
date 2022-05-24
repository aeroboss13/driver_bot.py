import xlsxwriter

import config


def get_all_trips_in_excel_file(trips):
    workbook = xlsxwriter.Workbook(config.trips_excel_file_name)
    worksheet = workbook.add_worksheet()

    # Заголовки
    headlines = ("Пункт отправления", "Пункт прибытия", "Время", "Цена поездки", "Дополнительная информация", "Статус")
    for column, headline in enumerate(headlines):
        worksheet.write(0, column, headline)

    for row, trip in enumerate(trips):
        for column, item in enumerate(trip):
            # Проверяем, сейчас идет по списку статус или нет
            if column == 5:
                state = {config.TripsStates.IN_PROCESS: "Неопубликованная", config.TripsStates.PUBLIC: "Активная",
                         config.TripsStates.TAKEN: "Взята"}[item]
                worksheet.write(row, column, state)
            else:
                worksheet.write(row, column, item)

    workbook.close()
