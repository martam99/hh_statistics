import psycopg2
from config import config
from get_hh_api import hh_api

PARAMS = config("config.ini", "postgresql")

data = hh_api()
# Значения для таблицы jobs и company
try:
    for values in data:
        vacancy_id = values['id']
        vacancy_name = values['name']
        published_date = values['published_at']
        salary_from = values['salary']['from']
        salary_to = values['salary']['to']
        url = values['url']
        requirement = values['snippet']['requirement']
        company_id = values['employer']['id']
        company_name = values['employer']['name']
except KeyError:
    print("NULL")
except TypeError:
    print('NULL')


def create_database(database_name: str, params: dict):
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE {database_name}")
    cur.execute("""
            CREATE TABLE IF NOT EXISTS jobs(
                vacancy_id int PRIMARY KEY,
                vacancy_name varchar(50) NOT NULL,
                published_date date,
                salary_to int,
                salary_from int,
                url varchar(50),
                requirement text
                )
            """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS company(
                company_id int PRIMARY KEY,
                vacancy_id int REFERENCES vacancy(vacancy_id),
                company_name varchar(50)
                )
            """)
    cur.execute("""
            INSERT INTO jobs VALUES (%s, %s, %s, %s, %s, %s)
            """,
                (vacancy_id, vacancy_name, published_date, url, requirement))
    cur.execute("""
            INSERT INTO company VALUES (%s, %s, %s)
            """,
                (company_id, vacancy_id, company_name))
    cur.close()
    conn.close()


create_database(database_name='vacancies', params=PARAMS)
