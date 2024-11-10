from scripts.database import create_database, save_data
from scripts.web_scraper import scrape_companies
from scripts.data_loader import load_data

def main():
    # Создаем базу данных и таблицы
    create_database()

    # Получаем список компаний
    companies = scrape_companies()

    # Загружаем данные для каждой компании
    for company in companies:
        data = load_data(company)

        # Сохраняем данные в базе данных
        save_data(data)

    print("Data sucsefully updated!")

if __name__ == "__main__":
    main()
