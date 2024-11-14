import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3
import requests
import pandas as pd
import os

# Настройки Selenium
driver = webdriver.Chrome()
driver.get("https://www.mse.mk/mk/reports")


# Функция для выбора месяца и года
def select_month_year(month, year):
    wait = WebDriverWait(driver, 10)

    # Выбор месяца
    select_month = Select(wait.until(EC.presence_of_element_located((By.ID, "cmbMonth"))))
    select_month.select_by_value(str(month))  # month - число от 1 до 12

    # Выбор года
    select_year = Select(wait.until(EC.presence_of_element_located((By.ID, "cmbYear"))))
    select_year.select_by_value(str(year))  # year - желаемый год

    # Нажать на кнопку "Прикажи"
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Прикажи']")))
    submit_button.click()


# Функция для сбора ссылок на каждый день
def collect_daily_reports():
    wait = WebDriverWait(driver, 10)

    # Ожидание появления контейнера со ссылками на дни
    daily_report_container = wait.until(EC.presence_of_element_located((By.ID, "Daily Report")))

    # Поиск всех ссылок на отчёты за каждый день
    day_links = daily_report_container.find_elements(By.TAG_NAME, "a")

    # Сбор ссылок и дат
    reports = []
    for link in day_links:
        date_text = link.text  # Текст с датой
        href = link.get_attribute("href")  # Ссылка на файл
        reports.append((date_text, href))

    return reports


# Функция для сохранения данных в базу данных
def save_reports_to_database(reports, month, year):
    conn = sqlite3.connect("reports.db")  # Создаём (или подключаемся к существующей) базе данных
    cursor = conn.cursor()

    # Создание таблицы, если она ещё не существует
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS daily_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            link TEXT,
            month INTEGER,
            year INTEGER
        )
    ''')

    # Вставка данных отчётов в таблицу
    for date_text, link in reports:
        cursor.execute('''
            INSERT INTO daily_reports (date, link, month, year) 
            VALUES (?, ?, ?, ?)
        ''', (date_text, link, month, year))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()
    print(f"Данные за {month}/{year} успешно сохранены в базу данных.")


# Функция для извлечения данных из базы по месяцу и году
def get_reports_by_month_year(month, year):
    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()

    # Получение ссылок для заданного месяца и года
    cursor.execute('''
        SELECT date, link FROM daily_reports
        WHERE month = ? AND year = ?
    ''', (month, year))

    reports = cursor.fetchall()
    conn.close()

    return reports


# Функция для скачивания файла
def download_xls_file(url, save_path):
    try:
        response = requests.get(url)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Файл успешно скачан: {save_path}")
        return save_path
    except Exception as e:
        messagebox.showerror("Грешка", f"Грешка при симнување на фајл: {e}")


# Функция для открытия и анализа xls файла
def open_and_analyze_xls(file_path, company_name):
    try:
        # Открываем xls файл с помощью pandas
        df = pd.read_excel(file_path)

        # Ищем компанию в данных
        company_data = df[df.apply(lambda row: row.astype(str).str.contains(company_name, case=False).any(), axis=1)]

        if not company_data.empty:
            print(f"Податоци за фирма {company_name}:")
            print(company_data)
        else:
            messagebox.showinfo("Информација", "Фирма не е пронајдена.")
    except Exception as e:
        messagebox.showerror("Грешка", f"Грешка при анализирање на фајл: {e}")


# Функция для обработки запроса на получение отчетов
def get_reports():
    try:
        # Запрашиваем у пользователя месяц и год
        month = int(month_entry.get())
        year = int(year_entry.get())

        # Выбор месяца и года и нажатие кнопки "Прикажи"
        select_month_year(month, year)

        # Небольшая пауза для загрузки данных
        time.sleep(2)

        # Сбор отчётов по дням
        reports = collect_daily_reports()

        # Сохранение отчётов в базу данных
        save_reports_to_database(reports, month, year)

        # Запрос на извлечение данных
        if messagebox.askyesno("Отвори извештај?", "дали сакате да се отвори извештај?"):
            reports = get_reports_by_month_year(month, year)
            result_text.delete(1.0, tk.END)
            for date, link in reports:
                result_text.insert(tk.END, f"Датум: {date}, Линк: {link}\n")

            # Запрашиваем день для скачивания и открытия
            selected_date = simpledialog.askstring("Избор на денот",
                                                   "Внесете датум (пример, 1.01.2024):")
            selected_link = next((link for date, link in reports if date == selected_date), None)

            if selected_link:
                # Скачиваем файл
                save_path = os.path.join(os.getcwd(), f"{selected_date}.xls")
                download_xls_file(selected_link, save_path)

                # Запрашиваем название компании для поиска в файле
                company_name = simpledialog.askstring("Пребарување на фирма",
                                                      "Внесете име на фирма за пребарување во извештај:")

                # Открываем и анализируем файл
                open_and_analyze_xls(save_path, company_name)
            else:
                messagebox.showinfo("Грешка", "Нема линк за изборен датум")

    except ValueError:
        messagebox.showerror("Грешка", "Внесете точен датум.")


# Основное окно
root = tk.Tk()
root.title("Извештај од веб-сајт")

# Ввод месяца и года для отчётов
month_label = tk.Label(root, text="Внеси Месец(1-12):")
month_label.pack(pady=5)

month_entry = tk.Entry(root, width=20)
month_entry.pack(pady=5)

year_label = tk.Label(root, text="Внеси година (например, 2024):")
year_label.pack(pady=5)

year_entry = tk.Entry(root, width=20)
year_entry.pack(pady=5)

# Кнопка для получения отчётов
get_reports_button = tk.Button(root, text="Извештаи", command=get_reports)
get_reports_button.pack(pady=10)

# Текстовое поле для вывода результатов
result_text = tk.Text(root, width=80, height=20)
result_text.pack(pady=10)

# Запуск приложения
root.mainloop()

# Закрытие браузера
driver.quit()
