"""고객사 정보 수정 다이얼로그"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from src.models import Customer


class EditDialog(QDialog):
    """고객사 정보 수정 다이얼로그"""
    customer_updated = pyqtSignal(object)  # Customer

    def __init__(self, customer: Customer, file_type: str = "korean", parent=None):
        super().__init__(parent)
        self._customer = customer
        self._file_type = file_type
        self.setWindowTitle("고객사 정보 수정")
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(500, 460)
        self.setObjectName("registerDialog")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        title = QLabel("고객사 정보 수정")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        # 고객사명
        layout.addWidget(self._make_label("고객사명 *"))
        self._name_input = QLineEdit(self._customer.company_name)
        self._name_input.setObjectName("dialogInput")
        layout.addWidget(self._name_input)

        # 대표자 + 사업자등록번호
        row1 = QHBoxLayout()
        col1 = QVBoxLayout()
        col1.addWidget(self._make_label("대표자 *"))
        self._ceo_input = QLineEdit(self._customer.ceo)
        self._ceo_input.setObjectName("dialogInput")
        col1.addWidget(self._ceo_input)
        row1.addLayout(col1)

        col2 = QVBoxLayout()
        col2.addWidget(self._make_label("사업자등록번호"))
        self._biznum_input = QLineEdit(self._customer.business_number)
        self._biznum_input.setObjectName("dialogInput")
        col2.addWidget(self._biznum_input)
        row1.addLayout(col2)
        layout.addLayout(row1)

        # 주소/국가
        addr_label = "주소" if self._file_type == "korean" else "국가"
        layout.addWidget(self._make_label(addr_label))
        self._addr_input = QLineEdit(self._customer.address_or_country)
        self._addr_input.setObjectName("dialogInput")
        layout.addWidget(self._addr_input)

        # 담당자
        layout.addWidget(self._make_label("담당자 성명/직급"))
        self._contact_input = QLineEdit(self._customer.contact_person)
        self._contact_input.setObjectName("dialogInput")
        layout.addWidget(self._contact_input)

        # 연락처 + Email
        row2 = QHBoxLayout()
        col3 = QVBoxLayout()
        col3.addWidget(self._make_label("연락처"))
        self._phone_input = QLineEdit(self._customer.phone)
        self._phone_input.setObjectName("dialogInput")
        col3.addWidget(self._phone_input)
        row2.addLayout(col3)

        col4 = QVBoxLayout()
        col4.addWidget(self._make_label("Email"))
        self._email_input = QLineEdit(self._customer.email)
        self._email_input.setObjectName("dialogInput")
        col4.addWidget(self._email_input)
        row2.addLayout(col4)
        layout.addLayout(row2)

        layout.addStretch()

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

    def _make_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("dialogFieldLabel")
        return lbl

    def _on_save(self):
        name = self._name_input.text().strip()
        ceo = self._ceo_input.text().strip()
        if not name:
            QMessageBox.warning(self, "입력 오류", "고객사명은 필수입니다.")
            return
        if not ceo:
            QMessageBox.warning(self, "입력 오류", "대표자는 필수입니다.")
            return

        biznum = self._biznum_input.text().strip()
        digits = biznum.replace("-", "")
        if digits.isdigit() and len(digits) == 10:
            biznum = f"{digits[:3]}-{digits[3:5]}-{digits[5:]}"

        self._customer.company_name = name
        self._customer.ceo = ceo
        self._customer.business_number = biznum
        self._customer.address_or_country = self._addr_input.text().strip()
        self._customer.contact_person = self._contact_input.text().strip()
        self._customer.phone = self._phone_input.text().strip()
        self._customer.email = self._email_input.text().strip()

        self.customer_updated.emit(self._customer)
        self.accept()
