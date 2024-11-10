import sqlite3
from datetime import datetime

# Функция для создания базы данных и таблиц
def create_database():
    conn = sqlite3.connect('data/stock_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_data (
            company_code TEXT,
            date TEXT,
            price REAL
        )
    ''')

    conn.commit()
    conn.close()

# Функция для сохранения данных в базу
def save_data(data):
    conn = sqlite3.connect('data/stock_data.db')
    cursor = conn.cursor()

    for record in data:
        cursor.execute('''
            INSERT INTO stock_data (company_code, date, price)
            VALUES (?, ?, ?)
        ''', (record['company_code'], record['date'], record['price']))

    conn.commit()
    conn.close()
