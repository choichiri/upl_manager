"""진행사항 추가 인라인 폼"""
import re
from datetime import datetime, date

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QLineEdit, QTextEdit, QPushButton, QFrame
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QKeyEvent

from src.models import ProgressEntry


def parse_date_input(text: str) -> str:
    """다양한 날짜 입력을 YY.MM.DD 형식으로 변환"""
    text = text.strip().replace("-", ".").replace("/", ".")
    today = date.today()
    year = today.year % 100

    # YY.MM.DD or YY.M.D
    m = re.match(r'^(\d{2})\.(\d{1,2})\.(\d{1,2})$', text)
    if m:
        return f"{int(m.group(1)):02d}.{int(m.group(2)):02d}.{int(m.group(3)):02d}"

    # MM.DD or M.D
    m = re.match(r'^(\d{1,2})\.(\d{1,2})$', text)
    if m:
        return f"{year:02d}.{int(m.group(1)):02d}.{int(m.group(2)):02d}"

    # M/D format
    m = re.match(r'^(\d{1,2})/(\d{1,2})$', text)
    if m:
        return f"{year:02d}.{int(m.group(1)):02d}.{int(m.group(2)):02d}"

    return text


class ProgressForm(QWidget):
    """진행사항 추가 인라인 폼"""
    submitted = pyqtSignal(object)  # ProgressEntry
    cancelled = pyqtSignal()

    def __init__(self, customer_name: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("progressForm")
        self._build_ui(customer_name)

    def _build_ui(self, customer_name: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        # 헤더
        header = QHBoxLayout()
        title = QLabel(f"진행사항 추가")
        title.setObjectName("progressFormTitle")
        header.addWidget(title)

        if customer_name:
            name_label = QLabel(customer_name)
            name_label.setObjectName("progressFormCustomer")
            header.addWidget(name_label)

        header.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setObjectName("progressFormClose")
        close_btn.setFixedSize(24, 24)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.cancelled.emit)
        header.addWidget(close_btn)
        layout.addLayout(header)

        # 날짜 + 내용
        body = QHBoxLayout()
        body.setSpacing(12)

        # 날짜 입력
        date_col = QVBoxLayout()
        date_col.setSpacing(4)
        date_lbl = QLabel("날짜")
        date_lbl.setObjectName("dialogFieldLabel")
        date_col.addWidget(date_lbl)

        today = datetime.now()
        self._date_input = QLineEdit(today.strftime("%y.%m.%d"))
        self._date_input.setObjectName("dialogInput")
        self._date_input.setFixedWidth(100)
        date_col.addWidget(self._date_input)

        # 오늘/어제 빠른 버튼
        quick_row = QHBoxLayout()
        quick_row.setSpacing(4)
        today_btn = QPushButton("오늘")
        today_btn.setObjectName("quickDateButton")
        today_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        today_btn.clicked.connect(
            lambda: self._date_input.setText(datetime.now().strftime("%y.%m.%d"))
        )
        quick_row.addWidget(today_btn)

        from datetime import timedelta
        yesterday_btn = QPushButton("어제")
        yesterday_btn.setObjectName("quickDateButton")
        yesterday_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        yesterday_btn.clicked.connect(
            lambda: self._date_input.setText(
                (datetime.now() - timedelta(days=1)).strftime("%y.%m.%d")
            )
        )
        quick_row.addWidget(yesterday_btn)
        quick_row.addStretch()
        date_col.addLayout(quick_row)

        auto_hint = QLabel("자동 인식: 4/2, 04-02, 26.4.2 등")
        auto_hint.setObjectName("dialogInfo")
        date_col.addWidget(auto_hint)
        date_col.addStretch()

        body.addLayout(date_col)

        # 내용 입력
        content_col = QVBoxLayout()
        content_col.setSpacing(4)
        content_lbl = QLabel("내용")
        content_lbl.setObjectName("dialogFieldLabel")
        content_col.addWidget(content_lbl)

        self._content_input = QTextEdit()
        self._content_input.setObjectName("progressContentInput")
        self._content_input.setPlaceholderText("진행사항을 입력하세요. 줄바꿈 가능.")
        self._content_input.setMinimumHeight(80)
        content_col.addWidget(self._content_input)

        body.addLayout(content_col, 1)
        layout.addLayout(body)

        # 빠른 템플릿 + 버튼
        bottom = QHBoxLayout()
        bottom.setSpacing(6)

        templates_label = QLabel("빠른 템플릿:")
        templates_label.setObjectName("dialogFieldLabel")
        bottom.addWidget(templates_label)

        for tmpl in ["통화", "메일 송부", "미팅", "출고", "입금"]:
            btn = QPushButton(tmpl)
            btn.setObjectName("templateButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, t=tmpl: self._insert_template(t))
            bottom.addWidget(btn)

        bottom.addStretch()

        cancel_btn = QPushButton("취소")
        cancel_btn.setObjectName("dialogCancelButton")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.cancelled.emit)
        bottom.addWidget(cancel_btn)

        submit_btn = QPushButton("추가 (Ctrl+Enter)")
        submit_btn.setObjectName("dialogRegisterButton")
        submit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        submit_btn.clicked.connect(self._on_submit)
        bottom.addWidget(submit_btn)

        layout.addLayout(bottom)

    def _insert_template(self, text: str):
        cursor = self._content_input.textCursor()
        cursor.insertText(text + " ")
        self._content_input.setFocus()

    def _on_submit(self):
        date_str = parse_date_input(self._date_input.text())
        content = self._content_input.toPlainText().strip()
        if not content:
            self._content_input.setFocus()
            return

        entry = ProgressEntry(date=date_str, content=content)
        self.submitted.emit(entry)

    def keyPressEvent(self, event: QKeyEvent):
        if (event.key() == Qt.Key.Key_Return and
                event.modifiers() == Qt.KeyboardModifier.ControlModifier):
            self._on_submit()
        else:
            super().keyPressEvent(event)
