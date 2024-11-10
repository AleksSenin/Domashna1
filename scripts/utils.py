from datetime import datetime

# Функция для форматирования цен
def format_price(price):
    return "{:,.2f}".format(price)

# Функция для форматирования дат
def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%d.%m.%Y")
