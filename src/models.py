"""데이터 모델 정의"""
from dataclasses import dataclass, field
from datetime import datetime

# 전역 날짜 형식 설정
_date_format = "yy.mm.dd"

DATE_FORMAT_MAP = {
    "yy.mm.dd": "%y.%m.%d",
    "yyyy-mm-dd": "%Y-%m-%d",
    "yyyy.mm.dd": "%Y.%m.%d",
    "mm/dd": "%m/%d",
}


def set_date_format(fmt: str):
    global _date_format
    _date_format = fmt


def get_date_format() -> str:
    return _date_format


def format_date(dt: datetime) -> str:
    py_fmt = DATE_FORMAT_MAP.get(_date_format, "%y.%m.%d")
    return dt.strftime(py_fmt)


@dataclass
class ProgressEntry:
    """진행사항 항목"""
    date: datetime | str | None
    content: str

    @property
    def date_str(self) -> str:
        if isinstance(self.date, datetime):
            return format_date(self.date)
        return str(self.date) if self.date else ""


@dataclass
class Customer:
    """고객사 정보"""
    sheet_name: str
    company_name: str = ""
    address_or_country: str = ""
    ceo: str = ""
    business_number: str = ""
    contact_person: str = ""
    phone: str = ""
    email: str = ""
    customer_code: str = ""
    progress: list[ProgressEntry] = field(default_factory=list)

    @property
    def display_name(self) -> str:
        name = self.company_name or self.sheet_name
        return name.replace("\n", " ").replace("\r", "")

    @property
    def last_activity_date(self) -> str:
        if self.progress:
            return self.progress[0].date_str
        return ""
