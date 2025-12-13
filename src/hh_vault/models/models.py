from typing import Optional


class Company:
    def __init__(self, hh_id: int, name: str, url: str):
        self.hh_id = hh_id
        self.name = name
        self.url = url

    def __repr__(self):
        return f"<Company {self.name} ({self.hh_id})>"


    @classmethod
    def from_api(cls, data: dict) -> "Company":
        return cls(
            hh_id=int(data["id"]),
            name=data["name"],
            url=data.get("alternate_url", "")
        )


class Vacancy:
    def __init__(
        self,
        hh_id: int,
        title: str,
        url: str,
        salary_from: Optional[int],
        salary_to: Optional[int],
        currency: Optional[str],
        employer_id: int
    ):
        self.hh_id = hh_id
        self.title = title
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.employer_id = employer_id

    def __repr__(self):
        return f"<Vacancy {self.title} ({self.hh_id})>"


    @classmethod
    def from_api(cls, data: dict) -> "Vacancy":
        salary = data.get("salary") or {}

        return cls(
            hh_id=int(data["id"]),
            title=data["name"],
            url=data.get("alternate_url", ""),
            salary_from=salary.get("from"),
            salary_to=salary.get("to"),
            currency=salary.get("currency"),
            employer_id=int(data["employer"]["id"])
        )
