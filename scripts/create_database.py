import os
import sqlite3

def create_database():
    # Проверка и создание директории 'data', если она не существует
    if not os.path.exists('data'):
        os.makedirs('data')

    # Подключаемся к базе данных (или создаем её)
    conn = sqlite3.connect('data/stock_data.db')
    cursor = conn.cursor()

    # Создаем таблицу, если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS companies
                      (id INTEGER PRIMARY KEY, name TEXT, code TEXT)''')

    conn.commit()
    conn.close()
