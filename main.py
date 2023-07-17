#from DBManager import DBManager


def main():
    count = get_companies_and_vacancies_count()
    all_vacancies = get_all_vacancies()
    avg = get_avg_salary()
    high_salary = get_vacancies_with_higher_salary()
    with_key = get_vacancies_with_keyword()


if __name__ == "__main__":
    main()

