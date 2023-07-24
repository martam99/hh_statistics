import psycopg2
from config import config
from get_hh_api import hh_api
from pprint import pprint

PARAMS = config("config.ini", "postgresql")

data = hh_api()
try:
    for el in data:
        for values in el:
            vacancy_id = values['id']
            vacancy_name = values['name']
            published_date = values['published_at']
            salary_from = values['salary']['from']
            salary_to = values['salary']['to']
            url = values['url']
            requirement = values['snippet']['requirement']
            company_id = values['employer']['id']
            company_name = values['employer']['name']
except TypeError:
    salary_from = None
    salary_to = None


def create_database(database_name: str, params: dict):
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("""
                            CREATE TABLE IF NOT EXISTS company(
                                company_id int PRIMARY KEY,
                                company_name varchar(50)
                                )
                            """)
    cur.execute("""
                        CREATE TABLE IF NOT EXISTS vacancy(
                            vacancy_id int PRIMARY KEY,
                            vacancy_name varchar(50) NOT NULL,
                            published_date date,
                            salary_from int,
                            salary_to int,
                            url varchar(50),
                            requirement text,
                            company_id int REFERENCES company(company_id) ON UPDATE CASCADE
                            )
                        """)
    cur.execute('TRUNCATE vacancy, company RESTART IDENTITY')
    cur.execute("""
            INSERT INTO vacancy VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
                (vacancy_id, vacancy_name, published_date, salary_from, salary_to, url, requirement))
    cur.execute("""
            INSERT INTO company VALUES (%s, %s)
            """,
                (company_id, company_name))

    cur.close()
    conn.close()


create_database(database_name='vacancies', params=PARAMS)
