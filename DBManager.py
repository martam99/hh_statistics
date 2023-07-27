from pprint import pprint

import psycopg2
from config import config

PARAMS = config("config.ini", "postgresql")
conn = psycopg2.connect(**PARAMS)
conn.autocommit = True
cur = conn.cursor()


class DBManager:
    """Класс для подключения к базе данных"""

    def __init__(self):
        self.cursor = cur

    def get_companies_and_vacancies_count(self):
        """Метод, который получает список всех компаний и количество вакансий"""
        self.cursor.execute("""
        SELECT company_name , COUNT(*) AS vacancy_count FROM company
        LEFT JOIN vacancy USING(company_id)
        GROUP BY company_name
        """)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        """Метод, который получает все вакансии с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        self.cursor.execute("""	     		
        SELECT vacancy_name, salary_from, salary_to, url, company_name FROM	vacancy
        FULL JOIN company USING(company_id)	
        """)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        """Метод, который получает среднюю зарплату по вакансиям."""
        self.cursor.execute("""
        SELECT AVG(salary_from), AVG(salary_to) FROM vacancy
        WHERE salary_from>0 and salary_to>0
        """)
        return self.cursor.fetchall()

    def get_vacancies_with_higher_salary(self):
        """Метод получает список всех вакансий у которых зарплата выше средней"""
        self.cursor.execute("""
        SELECT * FROM vacancy 
        WHERE salary_from>(SELECT AVG(salary_from) FROM vacancy) 
        OR salary_to>(SELECT AVG(salary_to) FROM vacancy)
        """)
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, user_input):
        """Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        self.cursor.execute(f"""
        SELECT * FROM vacancy 
        WHERE vacancy_name LIKE '%{user_input}%'
        """)
        return self.cursor.fetchall()

