from src.config import config
from src.func import main_func
from src.get_vacancy import get_company, get_vacancies, get_vacancies_list
from src.utils import create_database, save_data_to_database

if __name__ == '__main__':
    params = config()
    company_list = get_company()
    data = get_vacancies(company_list)
    vacancies = get_vacancies_list(data)
    create_database("vacancy", params)
    save_data_to_database(vacancies, company_list, "vacancy", params)
    main_func("vacancy", params)
