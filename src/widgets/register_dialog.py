"""새 고객사 등록 모달 다이얼로그"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QWidget, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from src.models import Customer


class RegisterDialog(QDialog):
    """새 고객사 등록 다이얼로그"""
    customer_registered = pyqtSignal(object)  # Customer

    def __init__(self, file_type: str = "korean", parent=None):
        super().__init__(parent)
        self._file_type = file_type
        self.setWindowTitle("새 고객사 등록")
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(500, 500)
        self.setObjectName("registerDialog")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        # 헤더
        header = QHBoxLayout()
        title = QLabel("새 고객사 등록")
        title.setObjectName("dialogTitle")
        header.addWidget(title)
        header.addStretch()

        tab_label = QLabel("국내" if self._file_type == "korean" else "해외")
        tab_label.setObjectName("dialogTab")
        header.addWidget(tab_label)
        layout.addLayout(header)

        # 고객사명 *
        layout.addWidget(self._make_label("고객사명 *"))
        self._name_input = QLineEdit()
        self._name_input.setObjectName("dialogInput")
        self._name_input.setPlaceholderText("예) 주식회사 오제이엔티")
        layout.addWidget(self._name_input)

        # 대표자 * + 사업자등록번호
        row1 = QHBoxLayout()
        col1 = QVBoxLayout()
        col1.addWidget(self._make_label("대표자 *"))
        self._ceo_input = QLineEdit()
        self._ceo_input.setObjectName("dialogInput")
        self._ceo_input.setPlaceholderText("예) 오종영")
        col1.addWidget(self._ceo_input)
        row1.addLayout(col1)

        col2 = QVBoxLayout()
        col2.addWidget(self._make_label("사업자등록번호"))
        self._biznum_input = QLineEdit()
        self._biznum_input.setObjectName("dialogInput")
        self._biznum_input.setPlaceholderText("000-00-00000")
        col2.addWidget(self._biznum_input)
        row1.addLayout(col2)
        layout.addLayout(row1)

        # 주소/국가
        addr_label = "주소" if self._file_type == "korean" else "국가"
        layout.addWidget(self._make_label(addr_label))
        self._addr_input = QLineEdit()
        self._addr_input.setObjectName("dialogInput")
        self._addr_input.setPlaceholderText(
            "서울특별시 서초구..." if self._file_type == "korean" else "예) Japan"
        )
        layout.addWidget(self._addr_input)

        # 담당자 정보
        layout.addWidget(self._make_label("담당자 정보"))
        self._contact_input = QLineEdit()
        self._contact_input.setObjectName("dialogInput")
        self._contact_input.setPlaceholderText("담당자 성명 / 직급 (예: 오나영 과장)")
        layout.addWidget(self._contact_input)

        # 연락처 + Email
        row2 = QHBoxLayout()
        col3 = QVBoxLayout()
        col3.addWidget(self._make_label("연락처"))
        self._phone_input = QLineEdit()
        self._phone_input.setObjectName("dialogInput")
        self._phone_input.setPlaceholderText("010-0000-0000")
        col3.addWidget(self._phone_input)
        row2.addLayout(col3)

        col4 = QVBoxLayout()
        col4.addWidget(self._make_label("Email"))
        self._email_input = QLineEdit()
        self._email_input.setObjectName("dialogInput")
        self._email_input.setPlaceholderText("example@email.com")
        col4.addWidget(self._email_input)
        row2.addLayout(col4)
        layout.addLayout(row2)

        # 안내 문구
        info = QLabel("ℹ 등록 시 엑셀 파일에 새 시트가 자동 생성되고 Index가 갱신됩니다.")
        info.setObjectName("dialogInfo")
        info.setWordWrap(True)
        layout.addWidget(info)

        layout.addStretch()

        # 버튼
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        cancel_btn = QPushButton("취소")
        cancel_btn.setObjectName("dialogCancelButton")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        register_btn = QPushButton("등록하기")
        register_btn.setObjectName("dialogRegisterButton")
        register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        register_btn.clicked.connect(self._on_register)
        btn_row.addWidget(register_btn)

        layout.addLayout(btn_row)

    def _make_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("dialogFieldLabel")
        return lbl

    def _on_register(self):
        name = self._name_input.text().strip()
        ceo = self._ceo_input.text().strip()

        if not name:
            QMessageBox.warning(self, "입력 오류", "고객사명은 필수 항목입니다.")
            self._name_input.setFocus()
            return
        if not ceo:
            QMessageBox.warning(self, "입력 오류", "대표자는 필수 항목입니다.")
            self._ceo_input.setFocus()
            return

        # 사업자번호 자동 포맷 (숫자만 입력 시)
        biznum = self._biznum_input.text().strip()
        digits = biznum.replace("-", "")
        if digits.isdigit() and len(digits) == 10:
            biznum = f"{digits[:3]}-{digits[3:5]}-{digits[5:]}"

        customer = Customer(
            sheet_name=name,
            company_name=name,
            address_or_country=self._addr_input.text().strip(),
            ceo=ceo,
            business_number=biznum,
            contact_person=self._contact_input.text().strip(),
            phone=self._phone_input.text().strip(),
            email=self._email_input.text().strip(),
        )
        self.customer_registered.emit(customer)
        self.accept()
