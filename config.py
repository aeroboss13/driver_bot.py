TOKEN = "1919399657:AAEkY_fUcLYpfzwF6qYQ9IfsQZBjjdQIMRQ"

point_name_max_len = 350
time_max_len = 100
additional_info_max_len = 1000

DEV_ID = 598428747
CHANNEL_ID = -1001531059313

MANAGER_ID = 1508494039


class Steps:
    MAIN_MENU = 0
    SEND_DEPARTURE_POINT = 1
    SEND_ARRIVAL_POINT = 2
    SEND_TIME = 3
    SEND_PRICE = 4
    SEND_ADDITIONAL_INFO = 5


class TripsStates:
    IN_PROCESS = 0
    PUBLIC = 1
    TAKEN = 2


class ResponseTypes:
    ACCEPT = 1
    DENY = 2


trips_excel_file_name = "Поездки.xlsx"
