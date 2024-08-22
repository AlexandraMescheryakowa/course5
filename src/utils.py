import psycopg2
from typing import Any


def create_database(name, params):
    """
    Создание базы данных и таблиц для сохранения данных о вакансиях и о работодателях
    """
    try:
        # Подключение к базе данных postgres
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS {name}")
            cur.execute(f"CREATE DATABASE {name}")
        conn.close()

        # Подключение к новой базе данных
        conn = psycopg2.connect(dbname=name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS company (
                    company_id INT PRIMARY KEY,
                    company_name VARCHAR,
                    company_url TEXT
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    vacancies_id SERIAL PRIMARY KEY,
                    company_id INT REFERENCES company(company_id),
                    company_name VARCHAR,
                    job_title TEXT,
                    vacancy_url TEXT,
                    salary_from INTEGER DEFAULT NULL,
                    salary_to INTEGER DEFAULT NULL,
                    currency TEXT DEFAULT NULL,
                    description TEXT,
                    requirement TEXT
                )
            """)
        conn.commit()
        conn.close()
        return "База данных и таблицы успешно созданы."
    except Exception as e:
        return f"Ошибка при создании базы данных: {e}"


def save_data_to_database(data: list[dict[str, Any]], data_company: list[dict[str, Any]], database, params: dict):
    """
    Сохранение данных о работодателях и вакансиях в базу данных
    """
    try:
        conn = psycopg2.connect(dbname=database, **params)
        with conn.cursor() as cur:
            for company in data_company:
                cur.execute("""
                INSERT INTO company (company_id, company_name, company_url)
                VALUES (%s, %s, %s)
                ON CONFLICT (company_id) DO NOTHING
                """, (company['id'], company['name'], company['url']))

            for vacancy in data:
                cur.execute("""
                INSERT INTO vacancies (company_id, company_name, job_title, vacancy_url, salary_from,
                salary_to, currency, description, requirement)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                            (vacancy['company_id'], vacancy['company_name'], vacancy['job_title'],
                             vacancy['link_to_vacancy'], vacancy['salary_from'], vacancy['salary_to'],
                             vacancy['currency'], vacancy['description'], vacancy['requirement'])
                            )
        conn.commit()
        conn.close()
        return "Таблицы успешно заполнены."
    except Exception as e:
        return f"Ошибка при сохранении данных в базу данных: {e}"
