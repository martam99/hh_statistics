import requests
from pprint import pprint
import json

URL = "https://api.hh.ru/vacancies?employer_id="
PARAMS = {"pages": 100, "per_page": 10, "only_with_vacancies": True}
companies = {"sokolov": "1038532",
             "teremok": "27879",
             "labirint": "17488",
             "abcp": "561525",
             "simplex": "1250899",
             "writers_way": "2175093",
             "tolyati": "9139449",
             "ozon": "2180",
             "fix_price": "196621",
             "start_job": "4811615"}


def hh_api():
    """Функция для подключения к api hh.ru"""
    data_list = []
    for company in companies.values():
        response = requests.get(f"{URL}{company}", params=PARAMS)
        if response.status_code != 200:
            pprint(f"Connection error with code {response.status_code}")
        else:
            data_list.append(response.json()['items'])

    return data_list


hh_api()
