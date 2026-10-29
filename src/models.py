"""데이터 모델 정의"""
import re
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


def _parse_entry_date(value) -> datetime | None:
    """진행사항 날짜를 datetime으로 변환. 해석 불가하면 None"""
    if isinstance(value, datetime):
        return value
    m = re.match(r'^(\d{2,4})[.\-/](\d{1,2})[.\-/](\d{1,2})', str(value or "").strip())
    if not m:
        return None
    year = int(m.group(1))
    if year < 100:
        year += 2000
    try:
        return datetime(year, int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def sort_progress(entries: list["ProgressEntry"]):
    """진행사항을 날짜 최신순으로 제자리 정렬. 같은 날짜는 등록 순서 유지.
    날짜를 해석할 수 없는 항목('→', '11.27~28' 등)은 직전 항목의 날짜를 따른다."""
    keys = {}
    prev = datetime.min
    for e in reversed(entries):  # 오래된 등록순으로 순회
        prev = _parse_entry_date(e.date) or prev
        keys[id(e)] = prev
    entries.sort(key=lambda e: keys[id(e)], reverse=True)


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
