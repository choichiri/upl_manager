"""설정 화면"""
import json
import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QCheckBox, QFileDialog,
    QWidget, QFrame, QButtonGroup, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal


import sys as _sys

def _get_config_path():
    if hasattr(_sys, '_MEIPASS'):
        return os.path.join(os.path.dirname(_sys.executable), "config.json")
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "config.json"
    )

CONFIG_PATH = _get_config_path()

DEFAULT_CONFIG = {
    "korean_path": "",
    "global_path": "",
    "auto_save": True,
    "auto_backup": True,
    "date_format": "yy.mm.dd",
}


def load_config() -> dict:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            saved = json.load(f)
            config = {**DEFAULT_CONFIG, **saved}
            return config
    return dict(DEFAULT_CONFIG)


def save_config(config: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


class SettingsDialog(QDialog):
    """설정 다이얼로그"""
    settings_changed = pyqtSignal(dict)

    def __init__(self, config: dict, parent=None):
        super().__init__(parent)
        self._config = dict(config)
        self.setWindowTitle("설정")
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(620, 540)
        self.resize(680, 560)
        self.setObjectName("settingsDialog")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # 헤더
        header = QHBoxLayout()
        title = QLabel("설정")
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

        # === 엑셀 파일 경로 ===
        layout.addWidget(self._make_section_label("엑셀 파일 경로"))

        # 국내
        layout.addWidget(self._make_label("국내 영업일지"))
        kr_row = QHBoxLayout()
        self._korean_path = QLineEdit(self._config.get("korean_path", ""))
        self._korean_path.setObjectName("settingsPathInput")
        self._korean_path.setPlaceholderText("국내 영업일지 .xlsm 파일 선택")
        self._korean_path.setMinimumWidth(400)
        kr_row.addWidget(self._korean_path, 1)
        kr_browse = QPushButton("찾아보기")
        kr_browse.setObjectName("editButton")
        kr_browse.setCursor(Qt.CursorShape.PointingHandCursor)
        kr_browse.clicked.connect(lambda: self._browse("korean"))
        kr_row.addWidget(kr_browse)
        layout.addLayout(kr_row)

        # 해외
        layout.addWidget(self._make_label("해외 영업일지"))
        gl_row = QHBoxLayout()
        self._global_path = QLineEdit(self._config.get("global_path", ""))
        self._global_path.setObjectName("settingsPathInput")
        self._global_path.setPlaceholderText("해외 영업일지 .xlsm 파일 선택")
        self._global_path.setMinimumWidth(400)
        gl_row.addWidget(self._global_path, 1)
        gl_browse = QPushButton("찾아보기")
        gl_browse.setObjectName("editButton")
        gl_browse.setCursor(Qt.CursorShape.PointingHandCursor)
        gl_browse.clicked.connect(lambda: self._browse("global"))
        gl_row.addWidget(gl_browse)
        layout.addLayout(gl_row)

        # 구분선
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setObjectName("sectionLine")
        layout.addWidget(sep)

        # === 자동 저장 ===
        layout.addWidget(self._make_section_label("자동 저장"))

        self._auto_save_cb = QCheckBox("변경 사항 즉시 저장")
        self._auto_save_cb.setObjectName("settingsCheckbox")
        self._auto_save_cb.setChecked(self._config.get("auto_save", True))
        layout.addWidget(self._auto_save_cb)
        hint1 = QLabel("진행사항 추가/수정 시 엑셀에 바로 반영 (권장)")
        hint1.setObjectName("dialogInfo")
        layout.addWidget(hint1)

        self._auto_backup_cb = QCheckBox("저장 전 자동 백업")
        self._auto_backup_cb.setObjectName("settingsCheckbox")
        self._auto_backup_cb.setChecked(self._config.get("auto_backup", True))
        layout.addWidget(self._auto_backup_cb)
        hint2 = QLabel('원본 파일을 "_백업" 폴더에 복사 후 저장')
        hint2.setObjectName("dialogInfo")
        layout.addWidget(hint2)

        # 구분선
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setObjectName("sectionLine")
        layout.addWidget(sep2)

        # === 날짜 형식 ===
        layout.addWidget(self._make_section_label("날짜 형식"))
        date_row = QHBoxLayout()
        date_row.setSpacing(8)
        self._date_buttons = {}
        formats = [
            ("yy.mm.dd", "26.04.01"),
            ("yyyy-mm-dd", "2026-04-01"),
            ("yyyy.mm.dd", "2026.04.01"),
            ("mm/dd", "04/01"),
        ]
        current_fmt = self._config.get("date_format", "yy.mm.dd")
        for fmt, example in formats:
            btn = QPushButton(example)
            btn.setObjectName("filterButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setProperty("active", fmt == current_fmt)
            btn.clicked.connect(lambda checked, f=fmt: self._select_date_format(f))
            date_row.addWidget(btn)
            self._date_buttons[fmt] = btn
        date_row.addStretch()
        layout.addLayout(date_row)

        layout.addStretch()

        # 저장 버튼
        btn_row = QHBoxLayout()
        btn_row.addStretch()
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

    def _make_section_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("dialogTitle")
        lbl.setStyleSheet("font-size: 14px;")
        return lbl

    def _browse(self, key: str):
        path, _ = QFileDialog.getOpenFileName(
            self, "엑셀 파일 선택", "",
            "Excel Files (*.xlsm *.xlsx);;All Files (*)"
        )
        if path:
            if key == "korean":
                self._korean_path.setText(path)
            else:
                self._global_path.setText(path)

    def _select_date_format(self, fmt: str):
        for f, btn in self._date_buttons.items():
            btn.setProperty("active", f == fmt)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        self._config["date_format"] = fmt

    def _on_save(self):
        self._config["korean_path"] = self._korean_path.text().strip()
        self._config["global_path"] = self._global_path.text().strip()
        self._config["auto_save"] = self._auto_save_cb.isChecked()
        self._config["auto_backup"] = self._auto_backup_cb.isChecked()

        save_config(self._config)
        self.settings_changed.emit(self._config)
        self.accept()
