from hh_vault.api.hh_api import HeadHunterAPI
from hh_vault.models.models import Company, Vacancy
from hh_vault.config.settings import COMPANY_IDS
from hh_vault.database.db import get_connection


def insert_companies(companies: list[Company]):
    conn = get_connection()
    cur = conn.cursor()

    for company in companies:
        cur.execute("""
            INSERT INTO companies (hh_id, name, url)
            VALUES (%s, %s, %s)
            ON CONFLICT (hh_id) DO NOTHING;
        """, (company.hh_id, company.name, company.url))

    conn.commit()
    cur.close()
    conn.close()


def insert_vacancies(vacancies: list[Vacancy]):
    conn = get_connection()
    cur = conn.cursor()

    for vacancy in vacancies:
        cur.execute("""
            INSERT INTO vacancies (
                hh_id, title, url, salary_from, salary_to, currency, employer_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (hh_id) DO NOTHING;
        """, (
            vacancy.hh_id,
            vacancy.title,
            vacancy.url,
            vacancy.salary_from,
            vacancy.salary_to,
            vacancy.currency,
            vacancy.employer_id
        ))

    conn.commit()
    cur.close()
    conn.close()


def run_etl():
    api = HeadHunterAPI()
    raw_data = api.get_all_data(COMPANY_IDS)

    companies = []
    all_vacancies = []

    for employer_id, entry in raw_data.items():
        company = Company.from_api(entry["company"])
        vacancies = [Vacancy.from_api(v) for v in entry["vacancies"]]

        companies.append(company)
        all_vacancies.extend(vacancies)

    insert_companies(companies)
    insert_vacancies(all_vacancies)

    print(f"🎉 Загружено: {len(companies)} компаний, {len(all_vacancies)} вакансий.")
