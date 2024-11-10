# test_script.py
import unittest
from scripts.database import insert_company, insert_stock_data
from scripts.web_scraper import scrape_companies

class TestDatabaseFunctions(unittest.TestCase):
    
    def test_insert_company(self):
        insert_company('ABC', 'Компания ABC')
        # Добавьте проверки, например, запрос в базу данных для проверки добавления
        
    def test_insert_stock_data(self):
        insert_stock_data('ABC', '2023-01-01', 100.5)
        # Проверьте, что данные добавлены в таблицу stock_data

if __name__ == '__main__':
    unittest.main()
