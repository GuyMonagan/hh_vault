import requests
from typing import List, Dict, Any
import time
from hh_vault.models.models import Company
from hh_vault.models.models import Vacancy
from hh_vault.config.settings import COMPANY_IDS, HH_API_URL


class HeadHunterAPI:
    BASE_URL = "https://api.hh.ru"


    def get_employer_info(self, employer_id: int) -> Dict[str, Any]:
        """Получить информацию о работодателе по ID."""
        url = f"{self.BASE_URL}/employers/{employer_id}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"[!] Ошибка получения работодателя {employer_id}: {response.status_code}")
            return {}

        return response.json()


    def get_vacancies_by_employer(self, employer_id: int, per_page: int = 100) -> List[Dict[str, Any]]:
        """Получить список вакансий работодателя с пагинацией."""
        vacancies = []
        page = 0

        while True:
            url = f"{self.BASE_URL}/vacancies"
            params = {
                "employer_id": employer_id,
                "per_page": per_page,
                "page": page
            }

            response = requests.get(url, params=params)

            if response.status_code != 200:
                print(f"[!] Ошибка загрузки вакансий {employer_id}, страница {page}")
                break

            data = response.json()
            vacancies.extend(data.get("items", []))

            if page >= data.get("pages", 0) - 1:
                break

            page += 1
            time.sleep(0.2)  # не спамим API

        return vacancies


    def get_all_data(self, employer_ids: List[int]) -> Dict[str, List[Dict[str, Any]]]:
        """Возвращает словарь {employer_id: [вакансии]}"""
        result = {}

        for employer_id in employer_ids:
            print(f"🔍 Обрабатываем работодателя {employer_id}")
            employer_info = self.get_employer_info(employer_id)
            if not employer_info:
                continue
            vacancies = self.get_vacancies_by_employer(employer_id)
            result[employer_id] = {
                "company": employer_info,
                "vacancies": vacancies
            }

        return result
