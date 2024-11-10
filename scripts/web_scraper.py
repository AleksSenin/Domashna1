import requests
from bs4 import BeautifulSoup

def scrape_companies():
    url = "https://www.mse.mk/mk/reports"  # Замените на актуальный URL для отчетов
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Парсим список компаний с сайта
    companies = []
    for option in soup.find_all('option'):
        company_code = option.get('value')
        if company_code.isalpha():  # Игнорируем компании с числовыми кодами
            companies.append(company_code)

    return companies
