
import sys
from PySide6.QtCore import (
    Qt, QSize, QByteArray, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve,
)
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QListWidget, QStackedWidget, QLabel, QFrame, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
)


from splash import IntroHost

pages = ("dashboard", "newsletter", "payments", "onboarding", "profiles",
         "grades", "classes", "attendance", "budget", "meetings", "settings")

SIDEBAR_OPEN = 230
SIDEBAR_CLOSED = 64

# ---------- Outline icons (24x24 viewBox, stroke only) ----------
ICONS = {
    "menu": '<line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>',
    "dashboard": '<rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/>',
    "newsletter": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 7l-10 6L2 7"/>',
    "payments": '<rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/>',
    "onboarding": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" y1="8" x2="19" y2="14"/><line x1="22" y1="11" x2="16" y2="11"/>',
    "profiles": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "grades": '<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89L17 22l-5-3-5 3 1.523-9.11"/>',
    "classes": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    "attendance": '<polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "budget": '<path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/>',
    "meetings": '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    "settings": '<line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/>',
}


def make_icon(name, color, size=20):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="1.8" stroke-linecap="round" '
        f'stroke-linejoin="round">{ICONS[name]}</svg>'
    )
    dpr = 2  # sharp on high-DPI screens
    pm = QPixmap(size * dpr, size * dpr)
    pm.fill(Qt.transparent)
    painter = QPainter(pm)
    QSvgRenderer(QByteArray(svg.encode())).render(painter)
    painter.end()
    pm.setDevicePixelRatio(dpr)
    return QIcon(pm)


STYLE = """
* { font-family: "Segoe UI", "Inter", sans-serif; font-size: 13px; color: #2B2F36; }
QMainWindow, #content { background: #F3F4F6; }

/* Sidebar */
#sidebarFrame { background: #22262B; }
#brand { color: #FFFFFF; font-size: 22px;}

QPushButton#burger {
    background: transparent; border: none; border-radius: 8px;
}
QPushButton#burger:hover { background: #2C3138; }

QListWidget#sidebar { background: transparent; border: none; outline: none; }
QListWidget#sidebar::item {
    color: #B4BAC3; padding: 11px 16px; border-left: 3px solid transparent;
}
QListWidget#sidebar[collapsed="true"]::item { padding: 12px 0px 12px 19px; }
QListWidget#sidebar::item:hover { background: #2C3138; color: #FFFFFF; }
QListWidget#sidebar::item:selected {
    background: #2C3138; color: #FFFFFF; border-left: 3px solid #F97316;
}

/* Top bar */
#topbar { background: #FFFFFF; border-bottom: 1px solid #E3E5E8; }
#pageTitle { font-size: 18px; font-weight: 700; }
QLineEdit#search {
    background: #F3F4F6; border: 1px solid #E3E5E8; border-radius: 6px;
    padding: 7px 12px; min-width: 220px;
}
QLineEdit#search:focus { border: 1px solid #F97316; background: #FFFFFF; }

/* Buttons */
QPushButton#primary {
    background: #F97316; color: #FFFFFF; border: none; border-radius: 6px;
    padding: 8px 16px; font-weight: 600;
}
QPushButton#primary:hover { background: #EA6A0E; }
QPushButton#primary:pressed { background: #C2570B; }

/* Cards */
QFrame#card { background: #FFFFFF; border: 1px solid #E3E5E8; border-radius: 10px; }
#cardTitle { color: #6B7280; font-size: 12px; font-weight: 600; }
#cardValue { font-size: 26px; font-weight: 700; }
#cardNote { color: #F97316; font-size: 12px; font-weight: 600; }
#sectionTitle { font-size: 14px; font-weight: 700; }

/* Table */
QTableWidget {
    background: #FFFFFF; border: none; gridline-color: transparent;
    alternate-background-color: #F9FAFB; selection-background-color: #FFEDD5;
    selection-color: #2B2F36;
}
QHeaderView::section {
    background: #FFFFFF; color: #6B7280; font-weight: 600; font-size: 12px;
    border: none; border-bottom: 1px solid #E3E5E8; padding: 8px;
}
QTableWidget::item { padding: 6px 8px; border: none; }

/* Scrollbars */
QScrollBar:vertical { background: transparent; width: 10px; }
QScrollBar::handle:vertical { background: #D1D5DB; border-radius: 5px; min-height: 30px; }
QScrollBar::add-line, QScrollBar::sub-line { height: 0; }
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" ")
        blank = QPixmap(32, 32)
        blank.fill(Qt.transparent)
        self.setWindowIcon(QIcon(blank))
        self.setStyleSheet(STYLE)
        self.collapsed = False

        # Pre-render icons: grey (idle) and orange (active)
        self.icons_idle = {n: make_icon(n, "#B4BAC3") for n in pages}
        self.icons_active = {n: make_icon(n, "#F97316") for n in pages}

        root = QWidget()
        row = QHBoxLayout(root)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)

        row.addWidget(self._build_sidebar())

        right = QWidget()
        right.setObjectName("content")
        rlay = QVBoxLayout(right)
        rlay.setContentsMargins(0, 0, 0, 0)
        rlay.setSpacing(0)
        rlay.addWidget(self._build_topbar())

        self.stack = QStackedWidget()
        self.stack.addWidget(self.dashboard_page())
        self.stack.addWidget(self.newsletter_page())
        self.stack.addWidget(self.payments_page())
        self.stack.addWidget(self.onboarding_page())
        self.stack.addWidget(self.profiles_page())
        self.stack.addWidget(self.grades_page())
        self.stack.addWidget(self.classes_page())
        self.stack.addWidget(self.attendance_page())
        self.stack.addWidget(self.budget_page())
        self.stack.addWidget(self.meetings_page())
        self.stack.addWidget(self.settings_page())
        rlay.addWidget(self.stack, 1)
        row.addWidget(right, 1)

        self.sidebar.currentRowChanged.connect(self._on_nav)
        self.sidebar.setCurrentRow(0)
        self.setCentralWidget(IntroHost(root))

    # ---------- Shell ----------
    def _build_sidebar(self):
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("sidebarFrame")
        self.sidebar_frame.setMinimumWidth(SIDEBAR_OPEN)
        self.sidebar_frame.setMaximumWidth(SIDEBAR_OPEN)
        lay = QVBoxLayout(self.sidebar_frame)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Header: hamburger + brand
        header = QWidget()
        hl = QHBoxLayout(header)
        hl.setContentsMargins(12, 12, 12, 12)
        hl.setSpacing(10)

        self.burger = QPushButton()
        self.burger.setObjectName("burger")
        self.burger.setIcon(make_icon("menu", "#FFFFFF", 22))
        self.burger.setIconSize(QSize(22, 22))
        self.burger.setFixedSize(40, 40)
        self.burger.setCursor(Qt.PointingHandCursor)
        self.burger.setToolTip("Toggle sidebar")
        self.burger.clicked.connect(self.toggle_sidebar)
        hl.addWidget(self.burger)

        self.brand_box = QWidget()
        bl = QVBoxLayout(self.brand_box)
        bl.setContentsMargins(0, 0, 0, 0)
        bl.setSpacing(0)
        brand = QLabel(
            "<span style=\"font-family:'Bahnschrift','Segoe UI'; "
            "font-weight:600; letter-spacing:3px;\">PEPA</span>"
        )
        brand.setObjectName("brand")
        bl.addWidget(brand)
        hl.addWidget(self.brand_box, 1)
        lay.addWidget(header)

        # Nav list
        self.sidebar = QListWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setProperty("collapsed", False)
        self.sidebar.setFocusPolicy(Qt.NoFocus)
        self.sidebar.setIconSize(QSize(20, 20))
        self.sidebar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        for name in pages:
            self.sidebar.addItem(name.capitalize())
            item = self.sidebar.item(self.sidebar.count() - 1)
            item.setIcon(self.icons_idle[name])
            item.setToolTip(name.capitalize())
        lay.addWidget(self.sidebar, 1)

        # Width animation
        self.anim = QParallelAnimationGroup(self)
        for prop in (b"minimumWidth", b"maximumWidth"):
            a = QPropertyAnimation(self.sidebar_frame, prop)
            a.setDuration(200)
            a.setEasingCurve(QEasingCurve.InOutCubic)
            self.anim.addAnimation(a)
        self.anim.finished.connect(self._on_anim_done)
        return self.sidebar_frame

    def _build_topbar(self):
        bar = QFrame()
        bar.setObjectName("topbar")
        bar.setFixedHeight(64)
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(28, 0, 28, 0)

        self.page_title = QLabel("Dashboard")
        self.page_title.setObjectName("pageTitle")
        lay.addWidget(self.page_title)
        lay.addStretch()

        search = QLineEdit()
        search.setObjectName("search")
        search.setPlaceholderText("Search...")
        lay.addWidget(search)

        btn = QPushButton("+ New")
        btn.setObjectName("primary")
        btn.setCursor(Qt.PointingHandCursor)
        lay.addWidget(btn)
        return bar

    # ---------- Sidebar behaviour ----------
    def toggle_sidebar(self):
        self.collapsed = not self.collapsed
        start = self.sidebar_frame.width()
        end = SIDEBAR_CLOSED if self.collapsed else SIDEBAR_OPEN

        if self.collapsed:
            self._set_labels(False)  # icons only, right away

        for i in range(self.anim.animationCount()):
            a = self.anim.animationAt(i)
            a.setStartValue(start)
            a.setEndValue(end)
        self.anim.start()

    def _on_anim_done(self):
        if not self.collapsed:
            self._set_labels(True)  # bring text back once fully open

    def _set_labels(self, show):
        self.brand_box.setVisible(show)
        self.sidebar.setProperty("collapsed", not show)
        self.sidebar.style().unpolish(self.sidebar)
        self.sidebar.style().polish(self.sidebar)
        for i, name in enumerate(pages):
            self.sidebar.item(i).setText(("  " + name.capitalize()) if show else "")

    def _on_nav(self, index):
        self.stack.setCurrentIndex(index)
        self.page_title.setText(pages[index].capitalize())
        for i, name in enumerate(pages):
            icon = self.icons_active[name] if i == index else self.icons_idle[name]
            self.sidebar.item(i).setIcon(icon)

    # ---------- Reusable components ----------
    def _stat_card(self, title, value, note):
        card = QFrame()
        card.setObjectName("card")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(20, 16, 20, 16)
        lay.setSpacing(4)
        t = QLabel(title.upper()); t.setObjectName("cardTitle")
        v = QLabel(value);         v.setObjectName("cardValue")
        n = QLabel(note);          n.setObjectName("cardNote")
        for w in (t, v, n):
            lay.addWidget(w)
        return card

    def _table_card(self, title, headers, rows):
        card = QFrame()
        card.setObjectName("card")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(20, 16, 20, 16)

        heading = QLabel(title)
        heading.setObjectName("sectionTitle")
        lay.addWidget(heading)

        table = QTableWidget(len(rows), len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for r, rec in enumerate(rows):
            for c, val in enumerate(rec):
                table.setItem(r, c, QTableWidgetItem(val))
        lay.addWidget(table)
        return card

    def _make_page(self, title):
        page = QWidget()
        page.setObjectName("content")
        lay = QVBoxLayout(page)
        lay.setContentsMargins(28, 24, 28, 24)
        card = QFrame(); card.setObjectName("card")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 16, 20, 16)
        h = QLabel(f"{title} - coming soon"); h.setObjectName("sectionTitle")
        cl.addWidget(h)
        cl.addStretch()
        lay.addWidget(card)
        return page

    # ---------- Pages ----------
    def dashboard_page(self):
        page = QWidget()
        page.setObjectName("content")
        lay = QVBoxLayout(page)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(18)

        grid = QGridLayout()
        grid.setSpacing(18)
        grid.addWidget(self._stat_card("Learners", "48", "+3 this term"), 0, 0)
        grid.addWidget(self._stat_card("Attendance", "94%", "+2% vs last week"), 0, 1)
        grid.addWidget(self._stat_card("Fees collected", "R 32,400", "86% of target"), 0, 2)
        grid.addWidget(self._stat_card("Outstanding", "R 5,300", "7 accounts"), 0, 3)
        lay.addLayout(grid)

        lay.addWidget(self._table_card(
            "Recent payments",
            ["Parent", "Learner", "Amount", "Date", "Status"],
            [
                ("N. Dlamini", "Lwazi D.", "R 750", "2026-10-12", "Paid"),
                ("T. Mokoena", "Thando M.", "R 750", "2026-10-11", "Paid"),
                ("S. Naidoo",  "Aarav N.", "R 750", "2026-10-09", "Pending"),
                ("P. Khumalo", "Sipho K.",  "R 750", "2026-10-08", "Paid"),
            ],
        ), 1)
        return page

    def newsletter_page(self):  return self._make_page("Newsletter")
    def payments_page(self):    return self._make_page("Payments")
    def onboarding_page(self):  return self._make_page("Onboarding")
    def profiles_page(self):    return self._make_page("Profiles")
    def grades_page(self):      return self._make_page("Grades")
    def classes_page(self):     return self._make_page("Classes")
    def attendance_page(self):  return self._make_page("Attendance")
    def budget_page(self):      return self._make_page("Budget")
    def meetings_page(self):    return self._make_page("Meetings")
    def settings_page(self):    return self._make_page("Settings")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.resize(1280, 800)
    window.show()
    sys.exit(app.exec())
