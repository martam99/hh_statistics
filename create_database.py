import psycopg2
from config import config
from get_hh_api import hh_api

PARAMS = config("config.ini", "postgresql")

data = hh_api()


def get_data():
    vacancy_data = []
    company_data = []

    for el in data:
        for values in el:
            vacancy_id = values['id']
            vacancy_name = values['name']
            published_date = values['published_at']
            salary_from = values['salary']['from'] if values['salary'] else None
            salary_to = values['salary']['to'] if values['salary'] else None
            url = values['url']
            requirement = values['snippet']['requirement']
            company_id = values['employer']['id']
            company_name = values['employer']['name']

            vacancy_data.append(
                (
                    vacancy_id,
                    vacancy_name,
                    published_date,
                    salary_from,
                    salary_to,
                    url,
                    requirement,
                    company_id
                )
            )

            company_data.append(
                (
                    company_id,
                    company_name
                )
            )

    return vacancy_data, company_data


def create_database(params: dict):
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("""
                        CREATE TABLE IF NOT EXISTS company(
                            company_id int PRIMARY KEY,
                            company_name varchar(100)
                                )
                        """)
    cur.execute("""
                        CREATE TABLE IF NOT EXISTS vacancy(
                            vacancy_id int PRIMARY KEY,
                            vacancy_name varchar(200) NOT NULL,
                            published_date date,
                            salary_from int,
                            salary_to int,
                            url varchar(100),
                            requirement text,
                            company_id int REFERENCES company(company_id) ON UPDATE CASCADE
                            )
                        """)

    cur.execute('TRUNCATE vacancy RESTART IDENTITY CASCADE')
    cur.execute('TRUNCATE company RESTART IDENTITY CASCADE')

    vacancy_data = get_data()[0]  # vacancy_data
    companies_data = get_data()[-1]  # company_data

    cur.executemany("""INSERT INTO company VALUES (%s, %s) ON CONFLICT (company_id) DO NOTHING;""", companies_data)
    cur.executemany("""
                    INSERT INTO vacancy VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (vacancy_id) DO NOTHING""",
                    vacancy_data
                    )

    cur.close()
    conn.close()


create_database(params=PARAMS)
