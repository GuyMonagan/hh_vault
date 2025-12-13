from hh_vault.database.db_manager import DBManager
from hh_vault.database.schema import create_tables
from hh_vault.database.data_loader import run_etl


def main():
    create_tables()

    should_update = input("🔄 Загрузить вакансии с hh.ru заново? (y/n): ").strip().lower()
    if should_update == "y":
        run_etl()
    else:
        print("⏩ Пропускаем загрузку данных.")

    db = DBManager()


    while True:
        print("\nВыберите действие:")
        print("1 — Показать компании и количество вакансий")
        print("2 — Показать все вакансии")
        print("3 — Показать среднюю зарплату")
        print("4 — Показать вакансии с зарплатой выше средней")
        print("5 — Поиск вакансий по ключевому слову")
        print("0 — Выход")

        choice = input(">>> ")

        if choice == "1":
            for row in db.get_companies_and_vacancies_count():
                print(f"{row[0]} — {row[1]} вакансий")

        elif choice == "2":
            for row in db.get_all_vacancies():
                company, title, salary_from, salary_to, url = row
                print(f"{company} | {title} | {salary_from}-{salary_to} | {url}")

        elif choice == "3":
            avg_salary = db.get_avg_salary()
            print(f"Средняя зарплата: {round(avg_salary)}")

        elif choice == "4":
            for row in db.get_vacancies_with_higher_salary():
                title, salary, url = row
                print(f"{title} | {salary} | {url}")

        elif choice == "5":
            keyword = input("Введите ключевое слово: ").strip()
            results = db.get_vacancies_with_keyword(keyword)
            if results:
                for row in results:
                    print(f"{row[0]} | {row[1]}")
            else:
                print("Вакансии не найдены.")

        elif choice == "0":
            print("Пока.")
            db.close()
            break

        else:
            print("Неверный ввод. Попробуй ещё раз.")


if __name__ == "__main__":
    main()
