import psycopg2
from config import config
from get_hh_api import hh_api

PARAMS = config("config.ini", "postgresql")

data = hh_api()


# Значения для таблицы jobs и company


def create_database(params: dict):
    """Функция для создания таблиц"""
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancy(
                vacancy_id int,
                vacancy_name varchar(50) NOT NULL,
                published_date date,
                salary_from int,
                salary_to int,
                url varchar(50),
                requirement text
                )
            """)
    conn.commit()

    # conn = psycopg2.connect(**params)
    # cur = conn.cursor()
    # cur.execute("""
    #         CREATE TABLE IF NOT EXISTS company(
    #             company_id int PRIMARY KEY,
    #             vac_id int REFERENCES vacancy(vacancy_id),
    #             company_name varchar(50)
    #             )
    #         """)
    # conn.commit()
    # cur.close()
    # conn.close()

    # conn = psycopg2.connect(**params)
    # cur = conn.cursor()
    # for values in data:
    #     vacancy_id = values['id']
    #     vacancy_name = values['name']
    #     published_date = values['published_at']
    #     salary_from = values['salary']['from']
    #     salary_to = values['salary']['to']
    #     url = values['url']
    #     requirement = values['snippet']['requirement']
    #     company_id = values['employer']['id']
    #     company_name = values['employer']['name']
    #     cur.execute("INSERT INTO vacancy VALUES (%s, %s, %s, %s, %s, %s, %s)", (vacancy_id, vacancy_name, published_date, salary_from, salary_to, url, requirement))
    #     cur.execute("""
    #             INSERT INTO company VALUES (%s, %s, %s)
    #             """,
    #                 (company_id, vacancy_id, company_name))
    # conn.commit()
    # conn.close()
    # except KeyError:
    #     print("NULL")
    # except TypeError:
    #     print('NULL')


create_database(params=PARAMS)
