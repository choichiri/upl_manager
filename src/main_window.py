"""메인 윈도우 - 영업일지 관리 대시보드"""
import os
import subprocess
import sys


def resource_path(relative_path: str) -> str:
    """PyInstaller 번들 내부/개발 환경 모두에서 리소스 경로를 반환"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), relative_path)

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPixmap, QIcon, QPainter, QPen, QColor, QPixmap as QPixmap2

from src.excel_handler import ExcelHandler
from src.models import Customer, ProgressEntry, set_date_format
from src.widgets.customer_list import CustomerListPanel
from src.widgets.detail_panel import DetailPanel
from src.widgets.register_dialog import RegisterDialog
from src.widgets.edit_dialog import EditDialog
from src.widgets.settings_dialog import SettingsDialog, load_config, save_config


class MainWindow(QMainWindow):
    """메인 윈도우"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("영업일지 관리 시스템")
        self.setMinimumSize(1200, 750)
        self.resize(1400, 850)

        self._current_tab = "korean"
        self._customers: dict[str, list[Customer]] = {"korean": [], "global": []}
        self._handlers: dict[str, ExcelHandler] = {}
        self._current_customer: Customer | None = None
        self._config = load_config()
        set_date_format(self._config.get("date_format", "yy.mm.dd"))

        self._build_ui()
        self._load_data()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._build_header(root)

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        self._list_panel = CustomerListPanel()
        self._list_panel.customer_selected.connect(self._on_customer_selected)
        self._list_panel.register_requested.connect(self._on_register_requested)
        body.addWidget(self._list_panel)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setStyleSheet("color: #2a2a2a;")
        body.addWidget(sep)

        self._detail_panel = DetailPanel()
        self._detail_panel.edit_requested.connect(self._on_edit_requested)
        self._detail_panel.delete_requested.connect(self._on_delete_customer)
        self._detail_panel.excel_requested.connect(self._on_excel_requested)
        self._detail_panel.progress_added.connect(self._on_progress_added)
        self._detail_panel.progress_updated.connect(self._on_progress_updated)
        self._detail_panel.progress_deleted.connect(self._on_progress_deleted)
        body.addWidget(self._detail_panel, 1)

        root.addLayout(body, 1)

    def _build_header(self, parent_layout):
        header = QWidget()
        header.setObjectName("header")
        header.setFixedHeight(48)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(20, 0, 20, 0)
        h_layout.setSpacing(0)

        # 로고
        logo_path = resource_path(os.path.join("data", "logo02-2.png"))
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path).scaledToHeight(
                22, Qt.TransformationMode.SmoothTransformation
            )
            logo_label.setPixmap(pixmap)
            logo_label.setObjectName("headerLogo")
            h_layout.addWidget(logo_label)

        # 구분선
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.VLine)
        divider.setObjectName("headerDivider")
        divider.setFixedHeight(20)
        h_layout.addWidget(divider)

        title = QPushButton("영업일지 관리")
        title.setObjectName("tabButton")
        title.setProperty("active", False)
        title.setCursor(Qt.CursorShape.ArrowCursor)
        title.setEnabled(False)
        title.setStyleSheet("color: #333333; font-weight: bold;")
        h_layout.addWidget(title)

        h_layout.addSpacing(12)

        # 국내/해외 탭
        self._tab_korean = QPushButton("국내")
        self._tab_korean.setObjectName("tabButton")
        self._tab_korean.setCursor(Qt.CursorShape.PointingHandCursor)
        self._tab_korean.setProperty("active", True)
        self._tab_korean.clicked.connect(lambda: self._switch_tab("korean"))
        h_layout.addWidget(self._tab_korean)

        h_layout.addSpacing(4)

        self._tab_global = QPushButton("해외")
        self._tab_global.setObjectName("tabButton")
        self._tab_global.setCursor(Qt.CursorShape.PointingHandCursor)
        self._tab_global.setProperty("active", False)
        self._tab_global.clicked.connect(lambda: self._switch_tab("global"))
        h_layout.addWidget(self._tab_global)

        h_layout.addStretch()

        # 새로고침 버튼
        refresh_btn = QPushButton()
        refresh_btn.setObjectName("refreshButton")
        refresh_btn.setToolTip("엑셀 데이터 새로고침")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setIcon(self._make_refresh_icon())
        refresh_btn.clicked.connect(self._on_refresh)
        h_layout.addWidget(refresh_btn)

        h_layout.addSpacing(8)

        settings_btn = QPushButton("설정")
        settings_btn.setObjectName("settingsButton")
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.clicked.connect(self._on_settings)
        h_layout.addWidget(settings_btn)

        parent_layout.addWidget(header)

    def _load_data(self):
        # exe 실행 시: exe와 같은 폴더, 개발 시: data 폴더
        if hasattr(sys, '_MEIPASS'):
            exe_dir = os.path.dirname(sys.executable)
            data_dir = exe_dir
        else:
            data_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
            )

        files = {
            "korean": self._config.get("korean_path") or os.path.join(data_dir, "korean.xlsm"),
            "global": self._config.get("global_path") or os.path.join(data_dir, "global.xlsm"),
        }

        for key, path in files.items():
            if not path or not os.path.exists(path):
                continue
            try:
                handler = ExcelHandler(path, key)
                customers = handler.load()
                self._customers[key] = customers
                self._handlers[key] = handler
            except Exception:
                pass  # 파일 없거나 오류 시 무시

        self._update_tab_labels()
        self._apply_tab()

    def _switch_tab(self, tab: str):
        if self._current_tab == tab:
            return
        self._current_tab = tab

        is_korean = tab == "korean"
        self._tab_korean.setProperty("active", is_korean)
        self._tab_global.setProperty("active", not is_korean)
        self._tab_korean.style().unpolish(self._tab_korean)
        self._tab_korean.style().polish(self._tab_korean)
        self._tab_global.style().unpolish(self._tab_global)
        self._tab_global.style().polish(self._tab_global)

        self._apply_tab()

    def _apply_tab(self):
        self._list_panel.set_file_type(self._current_tab)
        customers = self._customers.get(self._current_tab, [])
        self._list_panel.set_customers(customers)

    def _update_tab_labels(self):
        k_count = len(self._customers.get("korean", []))
        g_count = len(self._customers.get("global", []))
        self._tab_korean.setText(f"국내 {k_count}")
        self._tab_global.setText(f"해외 {g_count}")

    @staticmethod
    def _make_refresh_icon() -> QIcon:
        """새로고침 아이콘을 직접 그린다"""
        size = 32
        pixmap = QPixmap2(size, size)
        pixmap.fill(QColor(0, 0, 0, 0))  # 투명 배경

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(QColor("#8c9099"), 2.2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        # 원호 (270도)
        rect = QRectF(8, 8, 16, 16)
        painter.drawArc(rect, 90 * 16, 270 * 16)

        # 화살표 머리
        painter.drawLine(16, 7, 20, 9)
        painter.drawLine(16, 7, 16, 12)

        painter.end()
        return QIcon(pixmap)

    def _on_refresh(self):
        """엑셀 데이터 새로고침"""
        for h in self._handlers.values():
            h.close()
        self._handlers.clear()
        self._customers = {"korean": [], "global": []}
        self._current_customer = None
        self._load_data()
        k = len(self._customers.get("korean", []))
        g = len(self._customers.get("global", []))
        QMessageBox.information(self, "갱신 완료", f"데이터를 새로 불러왔습니다.\n\n국내: {k}개  |  해외: {g}개")

    def _on_customer_selected(self, customer: Customer):
        self._current_customer = customer
        self._detail_panel.set_customer(customer)

    # === 새 고객사 등록 ===

    def _on_register_requested(self):
        dlg = RegisterDialog(self._current_tab, self)
        dlg.customer_registered.connect(self._do_register)
        dlg.exec()

    def _do_register(self, customer: Customer):
        handler = self._handlers.get(self._current_tab)
        if not handler:
            QMessageBox.warning(self, "오류", "엑셀 파일이 로드되지 않았습니다.")
            return

        try:
            if self._config.get("auto_backup"):
                handler.backup()
            handler.create_customer_sheet(customer)
            # 리스트에 추가
            self._customers[self._current_tab].append(customer)
            self._update_tab_labels()
            self._apply_tab()
            pass  # 등록 완료
        except Exception as e:
            QMessageBox.critical(self, "등록 오류", str(e))

    # === 고객사 정보 수정 ===

    def _on_edit_requested(self):
        if not self._current_customer:
            return
        dlg = EditDialog(self._current_customer, self._current_tab, self)
        dlg.customer_updated.connect(self._do_update)
        dlg.exec()

    def _do_update(self, customer: Customer):
        handler = self._handlers.get(self._current_tab)
        if not handler:
            return
        try:
            if self._config.get("auto_backup"):
                handler.backup()
            handler.save_customer_info(customer)
            self._detail_panel.set_customer(customer)
            self._apply_tab()
            pass  # 수정 완료
        except Exception as e:
            QMessageBox.critical(self, "저장 오류", str(e))

    # === 고객사 삭제 ===

    def _on_delete_customer(self):
        if not self._current_customer:
            return

        name = self._current_customer.display_name
        reply = QMessageBox.warning(
            self, "고객사 삭제",
            f"'{name}' 고객사를 삭제하시겠습니까?\n\n"
            "엑셀 파일에서 해당 시트와 Index 정보가 제거됩니다.\n"
            "이 작업은 되돌릴 수 없습니다.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        handler = self._handlers.get(self._current_tab)
        if not handler:
            return
        try:
            if self._config.get("auto_backup"):
                handler.backup()
            handler.delete_customer(self._current_customer)
            # 메모리에서도 제거
            self._customers[self._current_tab].remove(self._current_customer)
            self._current_customer = None
            self._update_tab_labels()
            self._apply_tab()
            pass  # 삭제 완료
        except Exception as e:
            QMessageBox.critical(self, "삭제 오류", str(e))

    # === 엑셀 파일 열기 ===

    def _on_excel_requested(self):
        handler = self._handlers.get(self._current_tab)
        if handler and handler.file_path.exists():
            os.startfile(str(handler.file_path))

    # === 진행사항 추가 ===

    def _on_progress_added(self, entry: ProgressEntry):
        if not self._current_customer:
            return
        handler = self._handlers.get(self._current_tab)
        if not handler:
            return
        try:
            if self._config.get("auto_backup"):
                handler.backup()
            handler.add_progress_entry(self._current_customer, entry)
            # 메모리 상의 진행사항에도 추가 (최신이 맨 위)
            self._current_customer.progress.insert(0, entry)
            self._detail_panel.set_customer(self._current_customer)
            pass  # 추가 완료
        except Exception as e:
            QMessageBox.critical(self, "저장 오류", str(e))

    # === 진행사항 수정 ===

    def _on_progress_updated(self):
        if not self._current_customer:
            return
        handler = self._handlers.get(self._current_tab)
        if not handler:
            return
        try:
            if self._config.get("auto_backup"):
                handler.backup()
            handler.save_all_progress(self._current_customer)
            pass  # 수정 완료
        except Exception as e:
            QMessageBox.critical(self, "저장 오류", str(e))

    # === 진행사항 삭제 ===

    def _on_progress_deleted(self, entry: ProgressEntry):
        if not self._current_customer:
            return
        handler = self._handlers.get(self._current_tab)
        if not handler:
            return
        try:
            if self._config.get("auto_backup"):
                handler.backup()
            # 메모리에서는 detail_panel이 이미 제거함
            handler.save_all_progress(self._current_customer)
            pass  # 삭제 완료
        except Exception as e:
            QMessageBox.critical(self, "저장 오류", str(e))

    # === 설정 ===

    def _on_settings(self):
        dlg = SettingsDialog(self._config, self)
        dlg.settings_changed.connect(self._on_settings_changed)
        dlg.exec()

    def _on_settings_changed(self, config: dict):
        old_kr = self._config.get("korean_path", "")
        old_gl = self._config.get("global_path", "")
        self._config = config

        # 날짜 형식 반영
        set_date_format(config.get("date_format", "yy.mm.dd"))

        # 경로가 변경되었으면 데이터 리로드
        new_kr = config.get("korean_path", "")
        new_gl = config.get("global_path", "")
        if new_kr != old_kr or new_gl != old_gl:
            for h in self._handlers.values():
                h.close()
            self._handlers.clear()
            self._customers = {"korean": [], "global": []}
            self._load_data()

        # 현재 화면 갱신 (날짜 형식 등)
        self._apply_tab()
        if self._current_customer:
            self._detail_panel.set_customer(self._current_customer)
