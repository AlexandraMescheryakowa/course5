from src.DB_class import DBManager


def main_func(dbname, params):
    """
    Взаимодействие с пользователем
    """
    user_input = int(input("""Привет! Загрузили для тебя информацию по последним новеньким работодателям на HH!
Давай посмотрим, что они могут нам предложить? Выбери вариант нужного ответа:
1 - посмотреть список всех компаний и количество вакансий у каждой компании.
2 - посмотреть список всех вакансий с указанием с полной информацией.
3 - посмотреть среднюю зарплату по вакансиям.
4 - посмотреть список всех вакансий, у которых зарплата выше средней по всем вакансиям.
5 - посмотреть список всех вакансий по ключевому слову.
"""))

    program = DBManager(dbname, params)

    if user_input == 1:
        answer = program.get_companies_and_vacancies_count()
        print("Список всех компаний и количество вакансий у каждой компании:")
        for key, value in answer.items():
            print(f"{key} - {value}")
    elif user_input == 2:
        answer = program.get_all_vacancies()
        print("Список всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки на вакансию:")
        for i in answer:
            print(i)
    elif user_input == 3:
        print("Средняя зарплата по вакансиям (учитывается только зарплата в рублях):")
        answer = program.get_avg_salary()
        print(round(answer))
    elif user_input == 4:
        print(
            "Список всех вакансий, у которых зарплата выше средней по всем вакансиям. Компания, должность, зарплата от, зарплата до, ссылка на вакансию (учитывается только зарплата в рублях):")
        answer = program.get_vacancies_with_higher_salary()
        for i in answer:
            print(i)
    elif user_input == 5:
        keyword = input("Введите ключевое слово: ")
        answer = program.get_vacancies_with_keyword(keyword)
        for i in answer:
            print(i)
    else:
        print("Попробуй ещё раз! В качестве ответа принимаем цифры от 1 до 5")

    program.close()
