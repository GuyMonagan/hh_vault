from hh_vault.database.db import get_connection


class DBManager:

    def __init__(self):
        self.conn = get_connection()
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """Список всех компаний и количество вакансий у каждой."""
        self.cur.execute("""
            SELECT companies.name, COUNT(vacancies.id)
            FROM companies
            LEFT JOIN vacancies ON companies.hh_id = vacancies.employer_id
            GROUP BY companies.name;
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self) -> list[tuple]:
        """Все вакансии: название компании, вакансия, зарплата, ссылка."""
        self.cur.execute("""
            SELECT companies.name, vacancies.title,
                   COALESCE(vacancies.salary_from, 0),
                   COALESCE(vacancies.salary_to, 0),
                   vacancies.url
            FROM vacancies
            JOIN companies ON companies.hh_id = vacancies.employer_id;
        """)
        return self.cur.fetchall()

    def get_avg_salary(self) -> float:
        """Средняя зарплата (по salary_from)."""
        self.cur.execute("""
            SELECT AVG(salary_from)
            FROM vacancies
            WHERE salary_from IS NOT NULL;
        """)
        result = self.cur.fetchone()
        return result[0] if result else 0

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """Вакансии с зарплатой выше средней (по salary_from)."""
        avg_salary = self.get_avg_salary()
        self.cur.execute("""
            SELECT title, salary_from, url
            FROM vacancies
            WHERE salary_from > %s;
        """, (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """Вакансии, в названии которых есть ключевое слово."""
        pattern = f"%{keyword.lower()}%"
        self.cur.execute("""
            SELECT title, url
            FROM vacancies
            WHERE LOWER(title) LIKE %s;
        """, (pattern,))
        return self.cur.fetchall()
