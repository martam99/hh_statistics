from pprint import pprint

from DBManager import DBManager


def main():
    jobs = DBManager()
    pprint(jobs.get_companies_and_vacancies_count())
    print('')
    print('')
    pprint(jobs.get_all_vacancies())
    print('')
    print('')
    pprint(jobs.get_avg_salary())
    print('')
    print('')
    pprint(jobs.get_vacancies_with_higher_salary())
    print('')
    print('')
    pprint(jobs.get_vacancies_with_keyword(user_input=input().title()))


if __name__ == "__main__":
    main()
