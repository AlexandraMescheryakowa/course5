import requests


def get_company():
    """
    Получаем 15 работодателей с HH.ру
    """
    url_hh = 'https://api.hh.ru/vacancies'
    params = {'currency': 'RUR', 'host': 'hh.ru'}
    response = requests.get(url_hh, params=params)

    if response.status_code != 200:
        raise Exception(f"Ошибка при запросе к API: {response.status_code}")

    vacancies_hh = response.json()
    list_company = []
    for i in range(len(vacancies_hh['items'])):
        if len(list_company) == 15:
            break
        employer = vacancies_hh['items'][i]["employer"]
        company_info = {
            "id": employer['id'],
            'name': employer['name'],
            'url': employer['url']
        }
        if company_info not in list_company:
            list_company.append(company_info)

    return list_company


def get_vacancies(list_company):
    """
    Выгружаем все вакансии, опубликованные компанией
    """
    vacancies_info = []
    for company in list_company:
        company_id = company['id']
        url = f"https://api.hh.ru/vacancies?employer_id={company_id}"
        response = requests.get(url)
        if response.status_code == 200:
            vacancies = response.json().get('items', [])
            vacancies_info.extend(vacancies)
        else:
            print(f"Ошибка при запросе к API для компании {company['name']}: {response.status_code}")
    return vacancies_info


def get_vacancies_list(vacancies_info):
    """
    Получаем список словарей с данными для БД
    """
    vacancies_list = []
    for item in vacancies_info:
        company_id = item['employer']['id']
        company = item['employer']['name']
        company_url = item['employer']['url']
        job_title = item['name']
        link_to_vacancy = item['employer']['alternate_url']

        salary_from = item.get('salary', {}).get('from', 0)
        salary_to = item.get('salary', {}).get('to', 0)
        currency = item.get('salary', {}).get('currency', 'RUR')

        description = item['snippet'].get('responsibility', '')
        requirement = item['snippet'].get('requirement', '')

        vacancies_list.append({
            "company_id": company_id,
            "company_name": company,
            "company_url": company_url,
            "job_title": job_title,
            "link_to_vacancy": link_to_vacancy,
            "salary_from": salary_from,
            "salary_to": salary_to,
            "currency": currency,
            "description": description,
            "requirement": requirement
        })
    return vacancies_list
