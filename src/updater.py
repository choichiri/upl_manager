"""자동 업데이트 — GitHub Releases에서 exe 다운로드 + 자동 교체"""
import json
import os
import sys
import tempfile
import urllib.request
from PyQt6.QtWidgets import QMessageBox, QProgressDialog
from PyQt6.QtCore import QThread, pyqtSignal, Qt

CURRENT_VERSION = "1.2.0"
GITHUB_REPO = "choichiri/upl_manager"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


class UpdateChecker(QThread):
    """백그라운드에서 GitHub 최신 릴리즈 확인"""
    update_available = pyqtSignal(str, str)  # (version, exe_download_url)

    def run(self):
        try:
            req = urllib.request.Request(GITHUB_API, headers={"User-Agent": "UPL-Manager"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())

            latest = data.get("tag_name", "").lstrip("v")
            if not latest or not self._is_newer(latest, CURRENT_VERSION):
                return

            # .exe 파일 asset 찾기
            for asset in data.get("assets", []):
                if asset["name"].endswith(".exe"):
                    self.update_available.emit(latest, asset["browser_download_url"])
                    return

        except Exception:
            pass

    @staticmethod
    def _is_newer(latest: str, current: str) -> bool:
        try:
            l = [int(x) for x in latest.split(".")]
            c = [int(x) for x in current.split(".")]
            return l > c
        except ValueError:
            return False


class DownloadThread(QThread):
    """exe 파일 다운로드"""
    progress = pyqtSignal(int)  # 퍼센트
    finished = pyqtSignal(str)  # 다운로드된 파일 경로
    error = pyqtSignal(str)

    def __init__(self, url: str, save_path: str, parent=None):
        super().__init__(parent)
        self.url = url
        self.save_path = save_path

    def run(self):
        try:
            req = urllib.request.Request(self.url, headers={"User-Agent": "UPL-Manager"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                total = int(resp.headers.get("Content-Length", 0))
                downloaded = 0
                chunk_size = 65536

                with open(self.save_path, "wb") as f:
                    while True:
                        chunk = resp.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total > 0:
                            self.progress.emit(int(downloaded / total * 100))

            self.finished.emit(self.save_path)
        except Exception as e:
            self.error.emit(str(e))


def _apply_update(new_exe_path: str):
    """배치 스크립트로 exe 교체 후 재실행"""
    current_exe = sys.executable
    bat_path = os.path.join(tempfile.gettempdir(), "upl_update.bat")

    # 배치 스크립트: 기존 exe 삭제 → 새 exe 이동 → 재실행 → 배치 자체 삭제
    bat_content = f'''@echo off
timeout /t 2 /nobreak >nul
del /f "{current_exe}"
move /y "{new_exe_path}" "{current_exe}"
start "" "{current_exe}"
del /f "%~f0"
'''
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(bat_content)

    os.startfile(bat_path)
    sys.exit(0)


def check_for_updates(parent):
    """업데이트 체크 시작"""
    checker = UpdateChecker(parent)

    def on_update(version, exe_url):
        reply = QMessageBox.information(
            parent,
            "업데이트 알림",
            f"새로운 버전이 있습니다.\n\n"
            f"현재 버전: v{CURRENT_VERSION}\n"
            f"최신 버전: v{version}\n\n"
            f"자동으로 업데이트할까요?\n"
            f"(프로그램이 재시작됩니다)",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            _start_download(parent, version, exe_url)

    checker.update_available.connect(on_update)
    checker.start()
    parent._update_checker = checker


def _start_download(parent, version, exe_url):
    """다운로드 + 교체"""
    # 임시 폴더에 다운로드
    temp_path = os.path.join(tempfile.gettempdir(), f"upl_manager_v{version}.exe")

    # 프로그레스 다이얼로그
    progress = QProgressDialog(f"v{version} 다운로드 중...", "취소", 0, 100, parent)
    progress.setWindowTitle("업데이트")
    progress.setWindowModality(Qt.WindowModality.WindowModal)
    progress.setMinimumDuration(0)
    progress.setValue(0)

    downloader = DownloadThread(exe_url, temp_path, parent)

    def on_progress(pct):
        progress.setValue(pct)

    def on_finished(path):
        progress.close()
        QMessageBox.information(
            parent,
            "업데이트",
            "다운로드 완료. 프로그램을 재시작합니다."
        )
        _apply_update(path)

    def on_error(msg):
        progress.close()
        QMessageBox.critical(parent, "업데이트 오류", f"다운로드 실패:\n{msg}")

    def on_cancel():
        downloader.terminate()

    downloader.progress.connect(on_progress)
    downloader.finished.connect(on_finished)
    downloader.error.connect(on_error)
    progress.canceled.connect(on_cancel)

    downloader.start()
    parent._downloader = downloader
