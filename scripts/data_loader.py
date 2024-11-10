import requests
from datetime import datetime
from scripts.utils import format_price, format_date

# Функция для загрузки данных о компании
def load_data(company_code):
    # Здесь будет ваш код для загрузки данных с сайта
    # Для примера создаем фиктивные данные
    data = []

    # Замените на реальную логику для получения данных
    for i in range(5):  # Пример 5 дней
        date = datetime.today().strftime('%Y-%m-%d')
        price = 21500 + i * 100  # Пример цен
        formatted_price = format_price(price)
        formatted_date = format_date(date)

        data.append({
            'company_code': company_code,
            'date': formatted_date,
            'price': formatted_price
        })

    return data
