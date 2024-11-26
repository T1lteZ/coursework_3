from src.api_class_module import (FindEmployerFromHHApi,
                                  FindVacancyFromHHApi)
from src.DBCreate_module import DBConnection
from src.utils import (filter_vacancies, get_top_vacancies,
                       get_vacancies_by_salary, sort_vacancies)
from src.vacancy_class import Vacancy
from src.DBManager_module import DBManager


def get_valid_input(prompt, type_func, condition_func=None, error_message="Неверный ввод"):
    """Общая функция для получения и валидации ввода пользователя"""
    while True:
        try:
            user_input = type_func(input(prompt))
            if condition_func and not condition_func(user_input):
                raise ValueError
            return user_input
        except ValueError:
            print(error_message)


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    search_query = input("Введите поисковый запрос: ")
    hh_vacancies = FindVacancyFromHHApi().get_vacancies(search_query)
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

    top_n = get_valid_input(
        "Введите количество вакансий для вывода N самых оплачиваемых: ",
        int,
        lambda x: x > 0,
        "Введите положительное число."
    )

    filter_words = list(input("Введите ключевые слова для фильтрации вакансий: ").split())
    salary_range_from = get_valid_input(
        "Введите диапазон зарплат от: ",
        int,
        lambda x: x >= 0,
        "Введите число, большее или равное нулю."
    )
    salary_range_to = get_valid_input(
        "Введите диапазон зарплат до: ",
        int,
        lambda x: x >= salary_range_from,
        f"Введите число, большее или равное {salary_range_from}."
    )

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range_from, salary_range_to)
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # Красивый вывод
    print(f"\nТоп {top_n} самых оплачиваемых вакансий:")
    for vacancy in top_vacancies:
        print(f"{vacancy['title']} - {vacancy['salary_min']} - {vacancy['salary_max']} {vacancy['salary_currency']}")
        print(f"Ссылка: {vacancy['url']}\n")


def user_interaction_with_db():
    """Функция для создания, заполнения и взаимодействия пользователя с базой данных вакансий"""
    employer_word = input("Введите слово по которому хотите найти работодателя или оставьте поле пустым:\n")
    employers_count = get_valid_input(
        "Введите топ N (число до 50) ваканский для просмотра:\n",
        int,
        lambda x: 0 < x <= 50,
        "Введите число от 1 до 50."
    )

    employer_obj = FindEmployerFromHHApi()
    employers = employer_obj.get_employer_info(employers_count, keyword=employer_word)
    DBConnection().create_db()
    db_connect = DBConnection()
    db_connect.db_creating_employers()

    employers_id_list = list(input("Введите через запятую id не менее 10 компаний для отслеживания:\n").split(", "))

    if len(employers_id_list) < 10:
        print("Минимум 10 компаний должно быть введено.")
        return

    db_connect.db_filling_columns_for_emps(employers_id_list, employers)
    db_connect.db_creating_vacancies()

    for emp_id in employers_id_list:
        vacancy_list = FindVacancyFromHHApi().get_vacancies_by_employer_id(emp_id)
        db_connect.db_filling_vacancies(vacancy_list)

    searching_keyword = input('Введите слово для поиска по имеющимся вакансиям ...')
    query_manager = DBManager(db_params={'dbname': 'your_db', 'user': 'your_user', 'password': 'your_password'})

    print("\nСписок компаний и количество вакансий:")
    companies_and_vacancies = query_manager.get_companies_and_vacancies_count()
    for company, count in companies_and_vacancies:
        print(f"{company}: {count} вакансий")

    print("\nВсе вакансии:")
    all_vacancies = query_manager.get_all_vacancies()
    for vacancy in all_vacancies:
        print(
            f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]} - {vacancy[3]} {vacancy[4]}, Ссылка: {vacancy[5]}")

    print(f"\nСредняя зарплата по вакансиям: {query_manager.get_avg_salary()}")

    print("\nВакансии с зарплатой выше средней:")
    higher_salary_vacancies = query_manager.get_vacancies_with_higher_salary()
    for vacancy in higher_salary_vacancies:
        print(
            f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]} - {vacancy[3]} {vacancy[4]}, Ссылка: {vacancy[5]}")

    print(f"\nВакансии с ключевым словом '{searching_keyword}':")
    keyword_vacancies = query_manager.get_vacancies_with_keyword(searching_keyword)
    for vacancy in keyword_vacancies:
        print(
            f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]} - {vacancy[3]} {vacancy[4]}, Ссылка: {vacancy[5]}")


if __name__ == "__main__":
    user_interaction_with_db()
