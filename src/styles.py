"""UPL Company 라이트 테마
Primary Blue: #0067b3
Primary Green: #008053
Accent Green: #3bb145

배경(canvas) #f4f6f9 위에 흰색 카드(surface)를 올리는 구성.
텍스트: #1f2329(본문) / #5b6270(보조) / #7d838e(희미)
테두리: #e5e8ec(기본) / #d5dae0(강조)
"""

DARK_THEME = """
/* === 전역 === */
QWidget {
    background-color: transparent;
    color: #1f2329;
    font-family: "맑은 고딕", "Malgun Gothic", "Segoe UI", sans-serif;
    font-size: 13px;
}
QMainWindow, QDialog {
    background-color: #f4f6f9;
}
QToolTip {
    background-color: #1f2329;
    color: #ffffff;
    border: none;
    padding: 5px 8px;
    border-radius: 4px;
    font-size: 12px;
}

/* === 헤더 영역 === */
#header {
    background-color: #ffffff;
    border-bottom: 1px solid #e5e8ec;
}
#headerDivider {
    color: #e5e8ec;
}
#headerTitle {
    font-size: 15px;
    font-weight: bold;
    color: #1f2329;
}
#headerInfo {
    color: #7d838e;
    font-size: 12px;
}

/* === 국내/해외 세그먼트 탭 === */
#segmented {
    background-color: #eef0f3;
    border-radius: 9px;
}
#tabButton {
    background-color: transparent;
    border: none;
    color: #5b6270;
    font-size: 13px;
    font-weight: bold;
    padding: 6px 18px;
    border-radius: 7px;
}
#tabButton:hover {
    color: #1f2329;
}
#tabButton[active="true"] {
    background-color: #ffffff;
    color: #0067b3;
    border: 1px solid #e0e4e9;
}

/* === 헤더 우측 버튼 === */
#settingsButton {
    background-color: #ffffff;
    border: 1px solid #d5dae0;
    color: #3a404a;
    padding: 6px 16px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: bold;
}
#settingsButton:hover {
    background-color: #f4f6f9;
    border-color: #c4cad2;
}
#refreshButton {
    background-color: #ffffff;
    border: 1px solid #d5dae0;
    border-radius: 8px;
    padding: 0;
    min-width: 32px;
    min-height: 32px;
    max-width: 32px;
    max-height: 32px;
}
#refreshButton:hover {
    background-color: #e9f2fb;
    border-color: #a9cbe8;
}

/* === 좌측 패널 === */
#leftPanel {
    background-color: #ffffff;
    border-right: 1px solid #e5e8ec;
}

/* === 검색창 === */
#searchInput {
    background-color: #f4f6f9;
    border: 1px solid #f4f6f9;
    border-radius: 9px;
    padding: 8px 8px;
    color: #1f2329;
    font-size: 14px;
}
#searchInput:hover {
    border-color: #e0e4e9;
}
#searchInput:focus {
    background-color: #ffffff;
    border-color: #0067b3;
}

/* === 필터 탭 === */
#filterButton {
    background-color: transparent;
    border: 1px solid transparent;
    color: #5b6270;
    padding: 4px 12px;
    border-radius: 13px;
    font-size: 12px;
}
#filterButton:hover {
    background-color: #f4f6f9;
}
#filterButton[active="true"] {
    background-color: #1f2329;
    color: #ffffff;
    font-weight: bold;
}

/* === 초성/국가 섹션 헤더 === */
#sectionHeader {
    padding: 0;
    margin: 0;
}
#sectionHeaderLabel {
    font-size: 12px;
    font-weight: bold;
    color: #008053;
    padding: 0;
    min-width: 20px;
}
#sectionLine {
    color: #eef0f3;
    max-height: 1px;
}

/* === 고객사 카드 === */
#customerCard {
    border: none;
    border-radius: 8px;
}
#leftPanel #customerCard:hover {
    background-color: #f4f6f9;
}
#leftPanel #customerCard[selected="true"] {
    background-color: #e9f2fb;
}
#customerAvatar {
    border-radius: 16px;
    color: #ffffff;
    font-size: 13px;
    font-weight: bold;
}
#leftPanel #customerCardDate {
    font-size: 12px;
    color: #5b6270;
    background-color: #f1f3f6;
    border-radius: 9px;
    padding: 2px 7px;
}
#leftPanel #customerCard[selected="true"] #customerCardDate {
    background-color: #d4e6f7;
    color: #0067b3;
    font-weight: bold;
}

/* === 고객사 목록 헤더 === */
#listHeader {
    color: #7d838e;
    font-size: 12px;
    padding: 2px 4px;
}

/* === 새 고객사 등록 버튼 === */
#addCustomerButton {
    background-color: #008053;
    border: none;
    border-radius: 9px;
    color: #ffffff;
    padding: 10px;
    font-size: 13px;
    font-weight: bold;
}
#addCustomerButton:hover {
    background-color: #006d46;
}

/* === 우측 패널 === */
#rightPanel, #rightPanel QScrollArea, #detailContent {
    background-color: #f4f6f9;
}
#emptyState {
    color: #7d838e;
    font-size: 14px;
}

/* === 고객사 상세 헤더 === */
#detailHeader {
    background-color: transparent;
}
#detailCompanyName {
    font-size: 22px;
    font-weight: bold;
    color: #1f2329;
}
#detailAddress {
    font-size: 13px;
    color: #5b6270;
}
#editButton, #excelButton, #deleteButton {
    background-color: #ffffff;
    border: 1px solid #d5dae0;
    color: #3a404a;
    padding: 7px 16px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: bold;
}
#editButton:hover {
    background-color: #f4f6f9;
    border-color: #c4cad2;
}
#excelButton {
    color: #008053;
    border-color: #b5dccb;
}
#excelButton:hover {
    background-color: #e7f5ee;
    border-color: #008053;
}
#deleteButton {
    color: #7d838e;
}
#deleteButton:hover {
    background-color: #fdecec;
    border-color: #f3b4b4;
    color: #d93838;
}

/* === 정보 카드 === */
#infoRow {
    background-color: #ffffff;
    border: 1px solid #e5e8ec;
    border-radius: 12px;
}
#infoDivider {
    color: #eef0f3;
}
#infoLabel {
    font-size: 12px;
    color: #7d838e;
}
#infoValue {
    font-size: 14px;
    color: #1f2329;
    font-weight: bold;
}
#infoValueEmpty {
    font-size: 14px;
    color: #c4cad2;
    font-weight: normal;
}

/* === 진행사항 영역 === */
#progressCard {
    background-color: #ffffff;
    border: 1px solid #e5e8ec;
    border-radius: 12px;
}
#progressSection {
    border-bottom: 1px solid #eef0f3;
}
#progressHeader {
    font-size: 15px;
    font-weight: bold;
    color: #1f2329;
}
#progressCount {
    font-size: 12px;
    color: #0067b3;
    background-color: #e9f2fb;
    border-radius: 9px;
    padding: 2px 8px;
    font-weight: bold;
}
#progressCard #progressSearch {
    background-color: #f4f6f9;
    border: 1px solid #f4f6f9;
    border-radius: 8px;
    padding: 6px 8px;
    color: #1f2329;
    font-size: 12px;
}
#progressCard #progressSearch:focus {
    background-color: #ffffff;
    border-color: #0067b3;
}
#addProgressButton {
    background-color: #0067b3;
    border: none;
    color: #ffffff;
    padding: 7px 16px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: bold;
}
#addProgressButton:hover {
    background-color: #00589a;
}
#timelineEmpty {
    color: #7d838e;
    font-size: 13px;
    padding: 30px;
}

/* === 타임라인 항목 === */
#progressCard #timelineItem {
    border-radius: 8px;
}
#progressCard #timelineItem:hover {
    background-color: #f7f9fb;
}
#timelineDate {
    font-size: 13px;
    color: #0067b3;
    font-weight: bold;
}
#timelineContent {
    font-size: 14px;
    color: #1f2329;
}
#timelineEditButton {
    background-color: transparent;
    border: none;
    border-radius: 6px;
    color: #7d838e;
    font-family: "Segoe UI";
    font-size: 18px;
    font-weight: bold;
    padding: 0 0 6px 0;
}
#timelineEditButton:hover {
    background-color: #eef0f3;
    color: #0067b3;
}

/* === 스크롤바 === */
QScrollBar:vertical {
    background-color: transparent;
    width: 8px;
    margin: 2px;
    border: none;
}
QScrollBar::handle:vertical {
    background-color: #d5dae0;
    border-radius: 2px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background-color: #b0b6bf;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background-color: transparent;
}

/* === 팝업 메뉴 === */
QMenu {
    background-color: #ffffff;
    border: 1px solid #e0e4e9;
    border-radius: 8px;
    padding: 4px;
}
QMenu::item {
    padding: 7px 24px 7px 14px;
    border-radius: 5px;
    color: #1f2329;
}
QMenu::item:selected {
    background-color: #e9f2fb;
    color: #0067b3;
}

/* === 메시지 박스 === */
QMessageBox {
    background-color: #ffffff;
}
QMessageBox QLabel {
    color: #1f2329;
    font-size: 13px;
}
QMessageBox QPushButton {
    background-color: #ffffff;
    border: 1px solid #d5dae0;
    color: #3a404a;
    padding: 6px 18px;
    border-radius: 7px;
    min-width: 60px;
}
QMessageBox QPushButton:hover {
    background-color: #f4f6f9;
}
QMessageBox QPushButton:default {
    background-color: #0067b3;
    border-color: #0067b3;
    color: #ffffff;
}

/* === 다이얼로그 공통 === */
#registerDialog, #settingsDialog {
    background-color: #ffffff;
    border: 1px solid #d5dae0;
    border-radius: 14px;
}
#dialogTitle {
    font-size: 17px;
    font-weight: bold;
    color: #1f2329;
}
#dialogSectionTitle {
    font-size: 14px;
    font-weight: bold;
    color: #1f2329;
}
#dialogTab {
    background-color: #e9f2fb;
    color: #0067b3;
    padding: 3px 10px;
    border-radius: 9px;
    font-size: 12px;
    font-weight: bold;
}
#dialogFieldLabel {
    font-size: 12px;
    color: #5b6270;
    font-weight: bold;
}
#dialogInput {
    background-color: #ffffff;
    border: 1px solid #d5dae0;
    border-radius: 8px;
    padding: 8px 10px;
    color: #1f2329;
    font-size: 13px;
    min-height: 18px;
}
#dialogInput:hover {
    border-color: #c4cad2;
}
#dialogInput:focus {
    border-color: #0067b3;
}
#dialogInfo {
    font-size: 12px;
    color: #7d838e;
}
#dialogCancelButton {
    background-color: #ffffff;
    border: 1px solid #d5dae0;
    color: #3a404a;
    padding: 7px 18px;
    border-radius: 8px;
    font-size: 13px;
}
#dialogCancelButton:hover {
    background-color: #f4f6f9;
}
#dialogCloseButton {
    background-color: transparent;
    border: none;
    border-radius: 8px;
    color: #7d838e;
    font-size: 14px;
    font-weight: bold;
}
#dialogCloseButton:hover {
    background-color: #f4f6f9;
    color: #1f2329;
}
#dialogRegisterButton {
    background-color: #0067b3;
    border: none;
    color: #ffffff;
    padding: 7px 18px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: bold;
}
#dialogRegisterButton:hover {
    background-color: #00589a;
}

/* === 진행사항 추가 폼 === */
#progressForm {
    background-color: #f7fafd;
    border: 1px solid #cfe1f2;
    border-radius: 10px;
}
#progressFormTitle {
    font-size: 14px;
    font-weight: bold;
    color: #1f2329;
}
#progressFormCustomer {
    font-size: 12px;
    color: #7d838e;
}
#progressFormClose {
    background-color: transparent;
    border: none;
    border-radius: 6px;
    color: #7d838e;
    font-size: 14px;
}
#progressFormClose:hover {
    background-color: #eef0f3;
    color: #1f2329;
}
#progressContentInput, #progressForm #progressContentInput {
    background-color: #ffffff;
    border: 1px solid #d5dae0;
    border-radius: 8px;
    padding: 8px;
    color: #1f2329;
    font-size: 13px;
}
#progressContentInput:focus, #progressForm #progressContentInput:focus {
    border-color: #0067b3;
}
#progressForm #dialogInput {
    background-color: #ffffff;
}
#quickDateButton {
    background-color: #ffffff;
    border: 1px solid #d5dae0;
    color: #3a404a;
    padding: 3px 10px;
    border-radius: 11px;
    font-size: 12px;
}
#quickDateButton:hover {
    background-color: #f4f6f9;
}
#templateButton {
    background-color: #ffffff;
    border: 1px solid #cfe1f2;
    color: #0067b3;
    padding: 3px 11px;
    border-radius: 11px;
    font-size: 12px;
}
#templateButton:hover {
    background-color: #e9f2fb;
}

/* === 설정 체크박스 === */
#settingsCheckbox {
    color: #1f2329;
    font-size: 13px;
    spacing: 8px;
}
#settingsCheckbox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #c4cad2;
    border-radius: 4px;
    background-color: #ffffff;
}
#settingsCheckbox::indicator:checked {
    background-color: #008053;
    border-color: #008053;
}

/* === 설정 경로 입력 === */
#settingsPathInput {
    background-color: #ffffff;
    border: 1px solid #d5dae0;
    border-radius: 8px;
    padding: 8px 10px;
    color: #1f2329;
    font-size: 12px;
    min-height: 18px;
}
#settingsPathInput:focus {
    border-color: #0067b3;
}

/* === 연결 상태 === */
#connectedLabel {
    font-size: 12px;
    color: #3bb145;
}
"""
