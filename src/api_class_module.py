import requests
from abc import ABC, abstractmethod


class ApiHH(ABC):
    @abstractmethod
    def __init__(self):
        pass


class FindVacancyFromHHApi:
    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}

    def __get_vacancies(self, keyword: str):
        """Приватный метод получения списка вакансий"""
        self.__params["text"] = keyword
        vacancies = []
        try:
            while True:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                    except UnicodeDecodeError as e:
                        print(f"Ошибка кодировки: {e}")
                        return []
                    items = response_data.get("items", [])
                    vacancies.extend(items)
                    if len(items) < self.__params["per_page"]:
                        break
                    self.__params["page"] += 1
                else:
                    print(f"Ошибка запроса: {response.status_code}")
                    break
        except Exception as e:
            print(f"Ошибка при запросе вакансий: {e}")
        return vacancies


class FindEmployerFromHHApi(ApiHH):
    """
    Класс для получения данных по работодателям из API HeadHunter
    """
    def __init__(self):
        self.__url = "https://api.hh.ru/employers"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {
            "text": "",
            "page": 0,
            "per_page": 100,
            "sort_by": "by_vacancies_open",
        }

    def __get_employer_info(self, keyword=""):
        """Приватный метод получения информации о работодателях"""
        self.__params["text"] = keyword
        employers = []
        try:
            while True:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                if response.status_code == 200:
                    response_data = response.json()
                    items = response_data.get("items", [])
                    employers.extend(items)
                    if len(items) < self.__params["per_page"]:
                        break
                    self.__params["page"] += 1
                else:
                    print(f"Ошибка запроса: {response.status_code}")
                    break
        except Exception as e:
            print(f"Ошибка при запросе работодателей: {e}")
        return employers

    def get_employer_info(self, employers_count, keyword=""):
        employers = self.__get_employer_info(keyword)
        for employer in employers[:employers_count]:
            print(f"{employer.get('name')}, id: {employer.get('id')}")
        print("...")
        return employers
