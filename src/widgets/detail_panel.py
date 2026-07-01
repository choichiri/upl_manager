"""우측 고객사 상세정보 + 진행사항 타임라인 패널"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QLineEdit, QSizePolicy,
    QMenu, QDialog, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction

from src.models import Customer, ProgressEntry
from src.widgets.progress_form import ProgressForm, parse_date_input


class ProgressEditDialog(QDialog):
    """진행사항 수정 다이얼로그"""
    def __init__(self, entry: ProgressEntry, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.setWindowTitle("진행사항 수정")
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(500, 300)
        self.setObjectName("registerDialog")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        # 헤더
        header = QHBoxLayout()
        title = QLabel("진행사항 수정")
        title.setObjectName("dialogTitle")
        header.addWidget(title)
        header.addStretch()
        close_btn = QPushButton("✕")
        close_btn.setObjectName("dialogCloseButton")
        close_btn.setFixedSize(32, 32)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.reject)
        header.addWidget(close_btn)
        layout.addLayout(header)

        # 날짜
        date_row = QHBoxLayout()
        date_label = QLabel("날짜")
        date_label.setObjectName("dialogFieldLabel")
        date_row.addWidget(date_label)
        self._date_input = QLineEdit(self.entry.date_str)
        self._date_input.setObjectName("dialogInput")
        self._date_input.setFixedWidth(120)
        date_row.addWidget(self._date_input)
        date_row.addStretch()
        layout.addLayout(date_row)

        # 내용
        content_label = QLabel("내용")
        content_label.setObjectName("dialogFieldLabel")
        layout.addWidget(content_label)

        self._content_input = QTextEdit()
        self._content_input.setObjectName("progressContentInput")
        self._content_input.setPlainText(self.entry.content)
        layout.addWidget(self._content_input, 1)

        # 버튼
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        cancel_btn = QPushButton("취소")
        cancel_btn.setObjectName("dialogCancelButton")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        save_btn = QPushButton("저장")
        save_btn.setObjectName("dialogRegisterButton")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self._on_save)
        btn_row.addWidget(save_btn)

        layout.addLayout(btn_row)

    def _on_save(self):
        content = self._content_input.toPlainText().strip()
        if not content:
            return
        self.entry.date = parse_date_input(self._date_input.text())
        self.entry.content = content
        self.accept()


class InfoCard(QWidget):
    """기본정보 카드"""
    def __init__(self, label: str, value: str, parent=None):
        super().__init__(parent)
        self.setObjectName("infoCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(2)

        lbl = QLabel(label)
        lbl.setObjectName("infoLabel")
        layout.addWidget(lbl)

        self._value_label = QLabel()
        self._value_label.setWordWrap(True)
        self._set_display(value)
        layout.addWidget(self._value_label)

    def set_value(self, value: str):
        self._set_display(value)

    def _set_display(self, value: str):
        if value and value.strip():
            self._value_label.setText(value.strip())
            self._value_label.setObjectName("infoValue")
        else:
            self._value_label.setText("정보 없음")
            self._value_label.setObjectName("infoValueEmpty")
        self._value_label.style().unpolish(self._value_label)
        self._value_label.style().polish(self._value_label)


class TimelineItem(QWidget):
    """진행사항 타임라인 개별 항목"""
    edit_clicked = pyqtSignal(object)    # ProgressEntry
    delete_clicked = pyqtSignal(object)  # ProgressEntry

    def __init__(self, entry: ProgressEntry, parent=None, show_date: bool = True):
        super().__init__(parent)
        self.entry = entry
        self.setObjectName("timelineItem")
        # 커스텀 QWidget은 이 속성이 있어야 QSS의 배경/구분선이 렌더링됨
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        # 같은 날짜의 연속 항목은 날짜를 숨겨 그룹처럼 보이게 한다 (폭은 유지해 정렬 맞춤)
        date_label = QLabel(entry.date_str if show_date else "")
        date_label.setObjectName("timelineDate")
        date_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        date_label.setFixedWidth(80)
        layout.addWidget(date_label)

        content_label = QLabel(entry.content)
        content_label.setObjectName("timelineContent")
        content_label.setWordWrap(True)
        content_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(content_label, 1)

        edit_btn = QPushButton("⋯")
        edit_btn.setObjectName("timelineEditButton")
        edit_btn.setFixedSize(24, 24)
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.clicked.connect(self._show_menu)
        layout.addWidget(edit_btn, 0, Qt.AlignmentFlag.AlignTop)

    def _show_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background: #ffffff; border: 1px solid #dcdee2; border-radius: 6px; padding: 4px; }
            QMenu::item { padding: 6px 20px; border-radius: 4px; }
            QMenu::item:selected { background: #eef5fb; color: #0067b3; }
        """)
        edit_action = menu.addAction("수정")
        delete_action = menu.addAction("삭제")
        delete_action.setObjectName("deleteAction")

        action = menu.exec(self.mapToGlobal(self.rect().topRight()))
        if action == edit_action:
            self.edit_clicked.emit(self.entry)
        elif action == delete_action:
            self.delete_clicked.emit(self.entry)


class DetailPanel(QWidget):
    """우측 고객사 상세 패널"""
    edit_requested = pyqtSignal()
    delete_requested = pyqtSignal()
    excel_requested = pyqtSignal()
    progress_added = pyqtSignal(object)
    progress_updated = pyqtSignal()
    progress_deleted = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("rightPanel")
        self._timeline_items: list[QWidget] = []
        self._all_entries: list[ProgressEntry] = []
        self._progress_form: ProgressForm | None = None
        self._current_customer_name = ""
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        self._content_layout = QVBoxLayout(content)
        self._content_layout.setContentsMargins(16, 8, 16, 16)
        self._content_layout.setSpacing(12)

        self._build_header()
        self._build_info_cards()
        self._build_progress_header()

        self._form_placeholder = QVBoxLayout()
        self._content_layout.addLayout(self._form_placeholder)

        self._timeline_container = QWidget()
        self._timeline_layout = QVBoxLayout(self._timeline_container)
        self._timeline_layout.setContentsMargins(0, 0, 0, 0)
        self._timeline_layout.setSpacing(0)
        self._content_layout.addWidget(self._timeline_container)

        self._content_layout.addStretch()
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        self._show_empty()

    def _build_header(self):
        """상단 헤더 — 아바타 없이 이름 + 주소 + 버튼"""
        header = QWidget()
        header.setObjectName("detailHeader")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(20, 14, 16, 14)
        h_layout.setSpacing(12)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(3)
        self._company_label = QLabel()
        self._company_label.setObjectName("detailCompanyName")
        info_layout.addWidget(self._company_label)
        self._address_label = QLabel()
        self._address_label.setObjectName("detailAddress")
        self._address_label.setWordWrap(True)
        info_layout.addWidget(self._address_label)
        h_layout.addLayout(info_layout, 1)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(6)
        edit_btn = QPushButton("수정")
        edit_btn.setObjectName("editButton")
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.clicked.connect(self.edit_requested.emit)
        btn_layout.addWidget(edit_btn)

        delete_btn = QPushButton("삭제")
        delete_btn.setObjectName("deleteButton")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.clicked.connect(self.delete_requested.emit)
        btn_layout.addWidget(delete_btn)

        excel_btn = QPushButton("엑셀 열기")
        excel_btn.setObjectName("excelButton")
        excel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        excel_btn.clicked.connect(self.excel_requested.emit)
        btn_layout.addWidget(excel_btn)
        h_layout.addLayout(btn_layout)

        self._header_widget = header
        self._content_layout.addWidget(header)

    def _build_info_cards(self):
        cards_row = QHBoxLayout()
        cards_row.setSpacing(8)

        self._info_ceo = InfoCard("대표자", "")
        self._info_contact = InfoCard("담당자", "")
        self._info_phone = InfoCard("연락처", "")
        self._info_biznum = InfoCard("사업자번호", "")

        cards_row.addWidget(self._info_ceo)
        cards_row.addWidget(self._info_contact)
        cards_row.addWidget(self._info_phone)
        cards_row.addWidget(self._info_biznum)

        self._info_row = QWidget()
        self._info_row.setLayout(cards_row)
        self._content_layout.addWidget(self._info_row)

    def _build_progress_header(self):
        row = QHBoxLayout()
        row.setSpacing(8)

        self._progress_title = QLabel("진행사항")
        self._progress_title.setObjectName("progressHeader")
        row.addWidget(self._progress_title)

        self._progress_count = QLabel("")
        self._progress_count.setObjectName("progressCount")
        row.addWidget(self._progress_count)

        row.addStretch()

        self._progress_search = QLineEdit()
        self._progress_search.setObjectName("progressSearch")
        self._progress_search.setPlaceholderText("내용 검색...")
        self._progress_search.setFixedWidth(160)
        self._progress_search.textChanged.connect(self._filter_timeline)
        row.addWidget(self._progress_search)

        add_btn = QPushButton("+ 진행사항 추가")
        add_btn.setObjectName("addProgressButton")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self._show_progress_form)
        row.addWidget(add_btn)

        self._progress_header = QWidget()
        self._progress_header.setObjectName("progressSection")
        self._progress_header.setLayout(row)
        self._content_layout.addWidget(self._progress_header)

    def set_customer(self, customer: Customer):
        self._show_content()
        self._current_customer_name = customer.display_name
        self._hide_progress_form()

        name = customer.display_name
        self._company_label.setText(name)

        addr = customer.address_or_country
        if customer.company_name and customer.company_name != customer.sheet_name:
            full_name = customer.company_name.replace("\n", " ").replace("\r", "")
            addr = f"{full_name} · {addr}" if addr else full_name
        self._address_label.setText(addr)

        self._info_ceo.set_value(customer.ceo)
        self._info_contact.set_value(customer.contact_person)
        self._info_phone.set_value(customer.phone)
        self._info_biznum.set_value(customer.business_number)

        self._all_entries = customer.progress
        self._progress_count.setText(f"총 {len(customer.progress)}건")
        self._progress_search.clear()
        self._populate_timeline(customer.progress)

    def _populate_timeline(self, entries: list[ProgressEntry]):
        # 기존 항목 제거
        while self._timeline_layout.count():
            child = self._timeline_layout.takeAt(0)
            w = child.widget()
            if w:
                w.hide()
                w.deleteLater()
        self._timeline_items.clear()

        for i, entry in enumerate(entries):
            # 같은 날짜의 연속 항목은 두 번째부터 날짜를 숨긴다
            show_date = (i == 0) or (entries[i - 1].date_str != entry.date_str)
            item = TimelineItem(entry, show_date=show_date)
            # 날짜가 바뀌는 경계(또는 마지막 항목)에만 구분선을 긋는다
            last_of_date = (i == len(entries) - 1) or (entries[i + 1].date_str != entry.date_str)
            item.setProperty("lastOfDate", last_of_date)
            item.edit_clicked.connect(self._on_edit_entry)
            item.delete_clicked.connect(self._on_delete_entry)
            self._timeline_layout.addWidget(item)
            self._timeline_items.append(item)

    def _filter_timeline(self, text: str):
        text = text.strip().lower()
        if not text:
            self._populate_timeline(self._all_entries)
            return
        filtered = [e for e in self._all_entries if text in e.content.lower()]
        self._populate_timeline(filtered)

    def _show_progress_form(self):
        if self._progress_form:
            return
        self._progress_form = ProgressForm(self._current_customer_name)
        self._progress_form.submitted.connect(self._on_progress_submitted)
        self._progress_form.cancelled.connect(self._hide_progress_form)
        self._form_placeholder.addWidget(self._progress_form)

    def _hide_progress_form(self):
        if self._progress_form:
            self._progress_form.hide()
            self._progress_form.deleteLater()
            self._progress_form = None

    def _on_progress_submitted(self, entry: ProgressEntry):
        self._hide_progress_form()
        self.progress_added.emit(entry)

    def _on_edit_entry(self, entry: ProgressEntry):
        dlg = ProgressEditDialog(entry, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._populate_timeline(self._all_entries)
            self.progress_updated.emit()

    def _on_delete_entry(self, entry: ProgressEntry):
        reply = QMessageBox.question(
            self, "삭제 확인",
            f"이 진행사항을 삭제하시겠습니까?\n\n{entry.date_str}  {entry.content[:50]}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if entry in self._all_entries:
                self._all_entries.remove(entry)
            self._progress_count.setText(f"총 {len(self._all_entries)}건")
            self._populate_timeline(self._all_entries)
            self.progress_deleted.emit(entry)

    def _show_empty(self):
        self._header_widget.hide()
        self._info_row.hide()
        self._progress_header.hide()
        self._timeline_container.hide()

    def _show_content(self):
        self._header_widget.show()
        self._info_row.show()
        self._progress_header.show()
        self._timeline_container.show()
