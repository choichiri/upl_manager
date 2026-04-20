"""고객사 카드 위젯 - 좌측 리스트에 표시되는 개별 카드"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal, Qt, QRect
from PyQt6.QtGui import QFontMetrics, QPainter

from src.models import Customer


class ElidedLabel(QWidget):
    """텍스트가 넘치면 ...으로 말줄임하는 위젯 (paintEvent 방식)"""
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self._text = text
        self._is_name = False
        self._color = None

    def setText(self, text):
        self._text = text
        self.update()

    def setAsName(self, is_name: bool):
        """이름용(볼드, 진한색) 또는 서브(연한색) 설정"""
        self._is_name = is_name

    def paintEvent(self, event):
        from PyQt6.QtGui import QFont, QColor
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        # 앱 전체와 동일한 폰트 사용
        font = self.font()  # 부모로부터 상속된 스타일시트 폰트
        if self._is_name:
            font.setPixelSize(13)
            font.setBold(True)
            painter.setPen(QColor("#1a1a1a"))
        else:
            font.setPixelSize(11)
            font.setBold(False)
            painter.setPen(QColor("#8c9099"))

        painter.setFont(font)
        fm = painter.fontMetrics()
        elided = fm.elidedText(self._text, Qt.TextElideMode.ElideRight, self.width())
        painter.drawText(QRect(0, 0, self.width(), self.height()),
                         Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                         elided)
        painter.end()


class CustomerCard(QWidget):
    """좌측 패널의 고객사 카드"""
    clicked = pyqtSignal(object)

    def __init__(self, customer: Customer, parent=None):
        super().__init__(parent)
        self.customer = customer
        self._selected = False
        self.setObjectName("customerCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(50)
        self._build_ui()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 10, 6)
        layout.setSpacing(6)

        # 왼쪽: 이름 + 담당자
        left = QVBoxLayout()
        left.setSpacing(2)

        name_label = ElidedLabel(self.customer.display_name)
        name_label.setAsName(True)
        name_label.setFixedHeight(18)
        left.addWidget(name_label)

        sub_parts = []
        if self.customer.ceo:
            sub_parts.append(self.customer.ceo.replace("\n", " ").replace("\r", ""))
        if self.customer.contact_person:
            sub_parts.append(self.customer.contact_person.replace("\n", " ").replace("\r", ""))
        sub_text = " · ".join(sub_parts) if sub_parts else ""
        sub_label = ElidedLabel(sub_text)
        sub_label.setAsName(False)
        sub_label.setFixedHeight(15)
        left.addWidget(sub_label)

        layout.addLayout(left, 1)

        # 오른쪽: 날짜 (충분한 폭 확보)
        date_text = self.customer.last_activity_date
        if date_text:
            # 짧은 형식으로 표시 (MM.DD)
            parts = date_text.split(".")
            if len(parts) >= 3:
                short_date = f"{parts[0]}.{parts[1]}"
            else:
                short_date = date_text
            date_label = QLabel(short_date)
            date_label.setObjectName("customerCardDate")
            date_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            date_label.setToolTip(date_text)
            layout.addWidget(date_label)

    @property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, value: bool):
        self._selected = value
        self.setProperty("selected", value)
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event):
        self.clicked.emit(self.customer)
        super().mousePressEvent(event)
