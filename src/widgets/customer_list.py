"""좌측 고객사 리스트 패널"""
import unicodedata
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QScrollArea, QLabel, QFrame
)
from PyQt6.QtCore import pyqtSignal, Qt

from src.models import Customer
from src.widgets.customer_card import CustomerCard


# 한글 초성 테이블
CHOSUNG_LIST = [
    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ',
    'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]
# 쌍자음은 단자음 그룹으로 합침
CHOSUNG_GROUP = {
    'ㄱ': 'ㄱ', 'ㄲ': 'ㄱ', 'ㄴ': 'ㄴ', 'ㄷ': 'ㄷ', 'ㄸ': 'ㄷ',
    'ㄹ': 'ㄹ', 'ㅁ': 'ㅁ', 'ㅂ': 'ㅂ', 'ㅃ': 'ㅂ', 'ㅅ': 'ㅅ',
    'ㅆ': 'ㅅ', 'ㅇ': 'ㅇ', 'ㅈ': 'ㅈ', 'ㅉ': 'ㅈ', 'ㅊ': 'ㅊ',
    'ㅋ': 'ㅋ', 'ㅌ': 'ㅌ', 'ㅍ': 'ㅍ', 'ㅎ': 'ㅎ'
}
# 정렬 순서: ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ A~Z 기타
CHOSUNG_ORDER = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']


def get_initial(name: str) -> str:
    """이름의 첫 글자에서 초성/알파벳 그룹 키를 반환"""
    if not name:
        return "#"
    # 괄호, 특수문자 건너뛰고 첫 유효 문자 찾기
    for ch in name:
        if '\uAC00' <= ch <= '\uD7A3':
            # 한글 음절 → 초성 추출
            idx = (ord(ch) - 0xAC00) // (21 * 28)
            chosung = CHOSUNG_LIST[idx]
            return CHOSUNG_GROUP.get(chosung, chosung)
        elif ch.isalpha():
            return ch.upper()
    return "#"


def sort_key(customer: Customer) -> tuple:
    """초성/알파벳 기반 정렬 키"""
    initial = get_initial(customer.display_name)
    # 한글 초성 → 0~13, 영문 → 14+, 기타 → 99
    if initial in CHOSUNG_ORDER:
        group = CHOSUNG_ORDER.index(initial)
    elif initial.isalpha():
        group = 14 + ord(initial) - ord('A')
    else:
        group = 99
    return (group, customer.display_name.lower())


class SectionHeader(QWidget):
    """초성/알파벳 그룹 헤더"""
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.setObjectName("sectionHeader")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 4)
        layout.setSpacing(8)

        label = QLabel(text)
        label.setObjectName("sectionHeaderLabel")
        layout.addWidget(label)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setObjectName("sectionLine")
        layout.addWidget(line, 1)


class CustomerListPanel(QWidget):
    """좌측 고객사 리스트 패널"""
    customer_selected = pyqtSignal(object)  # Customer
    register_requested = pyqtSignal()

    def __init__(self, file_type: str = "korean", parent=None):
        super().__init__(parent)
        self.setObjectName("leftPanel")
        self.setFixedWidth(330)
        self._file_type = file_type
        self._cards: list[CustomerCard] = []
        self._section_headers: list[SectionHeader] = []
        self._all_customers: list[Customer] = []
        self._current_card: CustomerCard | None = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # 검색창
        self._search = QLineEdit()
        self._search.setObjectName("searchInput")
        self._search.setPlaceholderText("고객사, 담당자 검색...")
        self._search.textChanged.connect(self._filter_list)
        layout.addWidget(self._search)

        # 필터 탭
        filter_row = QHBoxLayout()
        filter_row.setSpacing(4)
        self._filter_buttons = {}
        for label in ["전체", "진행중", "완료"]:
            btn = QPushButton(label)
            btn.setObjectName("filterButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setProperty("active", label == "전체")
            btn.clicked.connect(lambda checked, l=label: self._on_filter(l))
            filter_row.addWidget(btn)
            self._filter_buttons[label] = btn
        filter_row.addStretch()
        layout.addLayout(filter_row)

        # 리스트 헤더
        self._list_header = QLabel("가나다순")
        self._list_header.setObjectName("listHeader")
        layout.addWidget(self._list_header)

        # 스크롤 영역
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._list_container = QWidget()
        self._list_layout = QVBoxLayout(self._list_container)
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        self._list_layout.setSpacing(0)
        self._list_layout.addStretch()

        scroll.setWidget(self._list_container)
        layout.addWidget(scroll, 1)

        # 새 고객사 등록 버튼
        add_btn = QPushButton("+ 새 고객사 등록")
        add_btn.setObjectName("addCustomerButton")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self.register_requested.emit)
        layout.addWidget(add_btn)

    def set_customers(self, customers: list[Customer]):
        """고객사 목록을 설정"""
        self._all_customers = customers
        self._update_header()
        self._populate_list(customers)

        # 첫 번째 고객사 자동 선택
        if self._cards:
            self._select_card(self._cards[0])

    def set_file_type(self, file_type: str):
        self._file_type = file_type

    def _populate_list(self, customers: list[Customer]):
        """그룹 헤더 + 카드 위젯들을 생성. 국내=초성순, 해외=나라순"""
        # 기존 위젯 완전 제거
        while self._list_layout.count() > 1:  # stretch 유지
            child = self._list_layout.takeAt(0)
            w = child.widget()
            if w:
                w.hide()
                w.deleteLater()
        self._cards.clear()
        self._section_headers.clear()
        self._current_card = None

        if self._file_type == "global":
            # 해외: 나라별 그룹
            grouped: dict[str, list[Customer]] = {}
            for c in customers:
                country = c.address_or_country.strip() or "기타"
                grouped.setdefault(country, []).append(c)
            sorted_groups = sorted(grouped.items(), key=lambda x: x[0].lower())
        else:
            # 국내: 초성별 그룹
            sorted_customers = sorted(customers, key=sort_key)
            grouped: dict[str, list[Customer]] = {}
            for c in sorted_customers:
                g = get_initial(c.display_name)
                grouped.setdefault(g, []).append(c)
            sorted_groups = list(grouped.items())

        insert_idx = 0
        for group_label, group_customers in sorted_groups:
            section = SectionHeader(group_label)
            self._list_layout.insertWidget(insert_idx, section)
            self._section_headers.append(section)
            insert_idx += 1

            for customer in group_customers:
                card = CustomerCard(customer)
                card.clicked.connect(lambda c, card_ref=card: self._select_card(card_ref))
                self._list_layout.insertWidget(insert_idx, card)
                self._cards.append(card)
                insert_idx += 1

    def _select_card(self, card: CustomerCard):
        """카드 선택 처리"""
        if self._current_card:
            self._current_card.selected = False
        card.selected = True
        self._current_card = card
        self.customer_selected.emit(card.customer)

    def _filter_list(self, text: str):
        """검색어로 필터링"""
        text = text.strip().lower()
        # 카드 필터링
        for card in self._cards:
            c = card.customer
            visible = not text or any(
                text in (getattr(c, f) or "").lower()
                for f in ["company_name", "sheet_name", "contact_person", "ceo"]
            )
            card.setVisible(visible)

        # 섹션 헤더: 해당 그룹에 보이는 카드가 없으면 숨김
        if text:
            # 각 헤더 바로 뒤의 카드들이 보이는지 확인
            header_indices = {i: h for i, h in enumerate(
                [self._list_layout.itemAt(j).widget()
                 for j in range(self._list_layout.count())
                 if self._list_layout.itemAt(j).widget() in self._section_headers]
            )}
            for header in self._section_headers:
                group_label = header.findChild(QLabel).text()
                if self._file_type == "global":
                    has_visible = any(
                        card.isVisible() and (card.customer.address_or_country.strip() or "기타") == group_label
                        for card in self._cards
                    )
                else:
                    has_visible = any(
                        card.isVisible() and get_initial(card.customer.display_name) == group_label
                        for card in self._cards
                    )
                header.setVisible(has_visible)
        else:
            for header in self._section_headers:
                header.setVisible(True)

    def _on_filter(self, label: str):
        """필터 버튼 클릭"""
        for name, btn in self._filter_buttons.items():
            btn.setProperty("active", name == label)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        self._filter_list(self._search.text())

    def _update_header(self):
        count = len(self._all_customers)
        self._list_header.setText(f"가나다순    {count}곳")
