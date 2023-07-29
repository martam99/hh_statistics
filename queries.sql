-- SQL-команды для создания таблиц


CREATE TABLE IF NOT EXISTS company(
                            company_id int PRIMARY KEY,
                            company_name varchar(100)
                                )


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