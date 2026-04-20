"""영업일지 관리 시스템"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from src.main_window import MainWindow, resource_path
from src.styles import DARK_THEME


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME)

    # 앱 아이콘 (작업표시줄 + 윈도우 타이틀바)
    icon_path = resource_path(os.path.join("data", "app_icon.ico"))
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()

    # 백그라운드 업데이트 체크
    from src.updater import check_for_updates
    check_for_updates(window)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
