"""UPL Company 라이트 테마
Primary Blue: #0067b3
Primary Green: #008053
Accent Green: #3bb145
"""

DARK_THEME = """
/* === 전역 === */
QMainWindow, QWidget {
    background-color: #ffffff;
    color: #2c2c2c;
    font-family: "맑은 고딕", "Malgun Gothic", "Segoe UI", sans-serif;
    font-size: 13px;
}

/* === 헤더 영역 === */
#header {
    background-color: #ffffff;
    border-bottom: 2px solid #e8eaed;
    padding: 0px 20px;
}
#headerLogo {
    max-height: 26px;
    margin-right: 4px;
}
#headerDivider {
    color: #d0d3d8;
    margin: 0 6px;
}
#headerTitle {
    font-size: 14px;
    font-weight: bold;
    color: #333333;
    letter-spacing: 1px;
}
#headerInfo {
    color: #9a9da2;
    font-size: 11px;
}

/* === 탭 버튼 === */
#tabButton {
    background-color: transparent;
    border: 1px solid transparent;
    color: #8c9099;
    font-family: "맑은 고딕", "Malgun Gothic", sans-serif;
    font-size: 13px;
    font-weight: bold;
    padding: 5px 18px;
    border-radius: 6px;
}
#tabButton:hover {
    background-color: #eef0f3;
}
#tabButton[active="true"] {
    background-color: #0067b3;
    color: #ffffff;
    border-color: #0067b3;
}
#tabButton:disabled {
    color: #333333;
    background-color: transparent;
    border-color: transparent;
}

/* === 설정 버튼 === */
#settingsButton {
    background-color: #f0f1f3;
    border: 1px solid #dcdee2;
    color: #555555;
    padding: 5px 14px;
    border-radius: 6px;
    font-size: 12px;
}
#settingsButton:hover {
    background-color: #e4e6e9;
}
#refreshButton {
    background-color: transparent;
    border: 1px solid #dcdee2;
    border-radius: 16px;
    color: #8c9099;
    font-size: 17px;
    padding: 0;
    min-width: 32px;
    min-height: 32px;
    max-width: 32px;
    max-height: 32px;
}
#refreshButton:hover {
    background-color: #eef5fb;
    border-color: #b3d4ed;
    color: #0067b3;
}

/* === 좌측 패널 === */
#leftPanel {
    background-color: #fafbfc;
    border-right: 1px solid #e2e5e9;
}

/* === 검색창 === */
#searchInput {
    background-color: #ffffff;
    border: 1px solid #d8dbe0;
    border-radius: 8px;
    padding: 8px 12px;
    color: #2c2c2c;
    font-size: 13px;
}
#searchInput:focus {
    border-color: #0067b3;
}

/* === 필터 탭 === */
#filterButton {
    background-color: transparent;
    border: 1px solid #d8dbe0;
    color: #8c9099;
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 12px;
}
#filterButton:hover {
    background-color: #f0f1f3;
}
#filterButton[active="true"] {
    background-color: #eef5fb;
    color: #0067b3;
    border-color: #b3d4ed;
}

/* === 초성/알파벳 섹션 헤더 === */
#sectionHeader {
    padding: 0;
    margin: 0;
    background-color: #fafbfc;
}
#sectionHeaderLabel {
    font-size: 12px;
    font-weight: bold;
    color: #008053;
    padding: 0;
    min-width: 20px;
}
#sectionLine {
    color: #e2e5e9;
    max-height: 1px;
}

/* === 고객사 카드 === */
#customerCard {
    background-color: transparent;
    border: none;
    border-bottom: 1px solid #eef0f2;
    border-radius: 0px;
    padding: 8px 12px;
    text-align: left;
}
#customerCard:hover {
    background-color: #f0f6fb;
}
#customerCard[selected="true"] {
    background-color: #e8f2fc;
    border-left: 3px solid #0067b3;
}
#customerCardName {
    font-size: 13px;
    font-weight: bold;
    color: #1a1a1a;
}
#customerCardSub {
    font-size: 11px;
    color: #8c9099;
}
#customerCardDate {
    font-size: 11px;
    color: #0067b3;
    font-weight: bold;
}

/* === 고객사 목록 헤더 === */
#listHeader {
    color: #8c9099;
    font-size: 12px;
    padding: 4px 0;
}

/* === 새 고객사 등록 버튼 === */
#addCustomerButton {
    background-color: transparent;
    border: 1px dashed #c0c4ca;
    border-radius: 8px;
    color: #8c9099;
    padding: 10px;
    font-size: 13px;
}
#addCustomerButton:hover {
    border-color: #008053;
    color: #008053;
    background-color: #f0faf5;
}

/* === 우측 패널 === */
#rightPanel {
    background-color: #ffffff;
}

/* === 고객사 상세 헤더 === */
#detailHeader {
    background-color: #f7f8fa;
    border: 1px solid #e2e5e9;
    border-radius: 10px;
    padding: 16px 20px;
    margin: 12px;
}
#detailCompanyName {
    font-family: "맑은 고딕", "Malgun Gothic", sans-serif;
    font-size: 17px;
    font-weight: bold;
    color: #1a1a1a;
}
#detailAddress {
    font-size: 12px;
    color: #8c9099;
}
#editButton, #excelButton {
    background-color: #f0f1f3;
    border: 1px solid #dcdee2;
    color: #555555;
    padding: 5px 14px;
    border-radius: 6px;
    font-size: 12px;
}
#editButton:hover, #excelButton:hover {
    background-color: #e4e6e9;
}
#deleteButton {
    background-color: #f0f1f3;
    border: 1px solid #dcdee2;
    color: #999999;
    padding: 5px 14px;
    border-radius: 6px;
    font-size: 12px;
}
#deleteButton:hover {
    background-color: #fee2e2;
    border-color: #fca5a5;
    color: #dc2626;
}

/* === 정보 카드 === */
#infoCard {
    background-color: #f7f8fa;
    border: 1px solid #e8eaed;
    border-radius: 8px;
    padding: 12px 16px;
}
#infoLabel {
    font-size: 11px;
    color: #8c9099;
}
#infoValue {
    font-size: 13px;
    color: #1a1a1a;
    font-weight: bold;
}
#infoValueEmpty {
    font-size: 13px;
    color: #c0c4ca;
    font-weight: normal;
    font-style: italic;
}

/* === 진행사항 영역 === */
#progressSection {
    border-top: 2px solid #e2e5e9;
    padding-top: 14px;
    margin-top: 6px;
}
#progressHeader {
    font-size: 15px;
    font-weight: bold;
    color: #1a1a1a;
}
#progressCount {
    font-size: 12px;
    color: #8c9099;
    font-weight: normal;
}
#progressSearch {
    background-color: #ffffff;
    border: 1px solid #d8dbe0;
    border-radius: 6px;
    padding: 5px 10px;
    color: #2c2c2c;
    font-size: 12px;
}
#progressSearch:focus {
    border-color: #0067b3;
}
#addProgressButton {
    background-color: #008053;
    border: none;
    color: #ffffff;
    padding: 5px 14px;
    border-radius: 6px;
    font-size: 12px;
}
#addProgressButton:hover {
    background-color: #006d46;
}

/* === 타임라인 항목 === */
#timelineItem {
    background-color: #ffffff;
    border-bottom: none;
    border-radius: 0px;
    padding: 11px 8px 11px 12px;
}
#timelineItem[lastOfDate="true"] {
    border-bottom: 1px solid #dcdee2;
}
#timelineItem:hover {
    background-color: #f8fafb;
}
#timelineDate {
    font-size: 12px;
    color: #0067b3;
    font-weight: bold;
    min-width: 80px;
}
#timelineContent {
    font-size: 13px;
    color: #333333;
}
#timelineEditButton {
    background-color: #f0f1f3;
    border: 1px solid #e2e5e9;
    border-radius: 4px;
    color: #8c9099;
    font-size: 14px;
    padding: 2px 6px;
}
#timelineEditButton:hover {
    background-color: #e4e6e9;
    border-color: #d0d3d8;
    color: #0067b3;
}

/* === 스크롤바 === */
QScrollBar:vertical {
    background-color: #fafbfc;
    width: 6px;
    border: none;
}
QScrollBar::handle:vertical {
    background-color: #d0d3d8;
    border-radius: 3px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background-color: #b0b4ba;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background-color: transparent;
}

/* === 다이얼로그 공통 === */
#registerDialog, #settingsDialog {
    background-color: #ffffff;
    border: 1px solid #d8dbe0;
    border-radius: 12px;
}
#dialogTitle {
    font-size: 16px;
    font-weight: bold;
    color: #1a1a1a;
}
#dialogSectionTitle {
    font-size: 14px;
    font-weight: bold;
    color: #333333;
}
#dialogTab {
    background-color: #0067b3;
    color: #ffffff;
    padding: 2px 10px;
    border-radius: 4px;
    font-size: 12px;
}
#dialogFieldLabel {
    font-size: 12px;
    color: #6b7280;
}
#dialogInput {
    background-color: #ffffff;
    border: 1px solid #d8dbe0;
    border-radius: 6px;
    padding: 8px 10px;
    color: #2c2c2c;
    font-size: 13px;
    min-height: 18px;
}
#dialogInput:focus {
    border-color: #0067b3;
}
#dialogInfo {
    font-size: 11px;
    color: #8c9099;
}
#dialogCancelButton {
    background-color: #f0f1f3;
    border: 1px solid #dcdee2;
    color: #555555;
    padding: 6px 18px;
    border-radius: 6px;
    font-size: 13px;
}
#dialogCancelButton:hover {
    background-color: #e4e6e9;
}
#dialogCloseButton {
    background-color: transparent;
    border: 1px solid #dcdee2;
    border-radius: 16px;
    color: #888888;
    font-size: 15px;
    font-weight: bold;
}
#dialogCloseButton:hover {
    background-color: #fee2e2;
    border-color: #fca5a5;
    color: #dc2626;
}
#dialogRegisterButton {
    background-color: #0067b3;
    border: none;
    color: #ffffff;
    padding: 6px 18px;
    border-radius: 6px;
    font-size: 13px;
}
#dialogRegisterButton:hover {
    background-color: #005a9e;
}

/* === 진행사항 추가 폼 === */
#progressForm {
    background-color: #f7fafb;
    border: 1px solid #d0e3ec;
    border-radius: 8px;
}
#progressFormTitle {
    font-size: 14px;
    font-weight: bold;
    color: #1a1a1a;
}
#progressFormCustomer {
    font-size: 12px;
    color: #8c9099;
}
#progressFormClose {
    background-color: transparent;
    border: none;
    color: #8c9099;
    font-size: 16px;
}
#progressFormClose:hover {
    color: #e74c3c;
}
#progressContentInput {
    background-color: #ffffff;
    border: 1px solid #d8dbe0;
    border-radius: 6px;
    padding: 8px;
    color: #2c2c2c;
    font-size: 13px;
}
#progressContentInput:focus {
    border-color: #0067b3;
}
#quickDateButton {
    background-color: #f0f1f3;
    border: 1px solid #dcdee2;
    color: #555555;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 11px;
}
#quickDateButton:hover {
    background-color: #e4e6e9;
}
#templateButton {
    background-color: #eef5fb;
    border: 1px solid #c4ddf0;
    color: #0067b3;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 11px;
}
#templateButton:hover {
    background-color: #ddeaf6;
}

/* === 설정 체크박스 === */
#settingsCheckbox {
    color: #2c2c2c;
    font-size: 13px;
    spacing: 8px;
}
#settingsCheckbox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #c0c4ca;
    border-radius: 3px;
    background-color: #ffffff;
}
#settingsCheckbox::indicator:checked {
    background-color: #008053;
    border-color: #008053;
}

/* === 설정 경로 입력 === */
#settingsPathInput {
    background-color: #ffffff;
    border: 1px solid #d8dbe0;
    border-radius: 6px;
    padding: 8px 10px;
    color: #2c2c2c;
    font-size: 12px;
    min-height: 18px;
}
#settingsPathInput:focus {
    border-color: #0067b3;
}

/* === 연결 상태 === */
#connectedLabel {
    font-size: 11px;
    color: #3bb145;
}
"""
