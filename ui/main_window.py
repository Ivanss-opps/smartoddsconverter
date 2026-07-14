from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QHBoxLayout,
    QVBoxLayout
)

from ui.odds_converter import OddsConverter
from ui.probability_converter import ProbabilityConverter
from ui.fair_odds_calculator import FairOddsCalculator
from ui.margin_calculator import MarginCalculator
from ui.about import About


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Trading Toolkit v0")
        self.resize(1200, 700)

        self.nav_buttons = []

        self.create_ui()

    def create_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        central_widget.setLayout(main_layout)

        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(240)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(12, 18, 12, 18)
        sidebar_layout.setSpacing(10)

        sidebar.setLayout(sidebar_layout)

        self.pages = QStackedWidget()
        self.pages.setObjectName("contentArea")

        self.pages.addWidget(OddsConverter())
        self.pages.addWidget(ProbabilityConverter())
        self.pages.addWidget(FairOddsCalculator())
        self.pages.addWidget(MarginCalculator())
        self.pages.addWidget(About())

        self.add_nav_button(sidebar_layout, "Odds Key Converter", 0)
        self.add_nav_button(sidebar_layout, "Probability Converter", 1)
        self.add_nav_button(sidebar_layout, "Fair Odds Calculator", 2)
        self.add_nav_button(sidebar_layout, "Margin Calculator", 3)

        sidebar_layout.addStretch()

        self.add_nav_button(sidebar_layout, "About", 4)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)

        self.set_active_page(0)

    def add_nav_button(self, layout, text, index):
        button = QPushButton(text)
        button.setObjectName("navButton")
        button.setCheckable(True)
        button.clicked.connect(lambda: self.set_active_page(index))

        layout.addWidget(button)

        self.nav_buttons.append(button)

    def set_active_page(self, index):
        self.pages.setCurrentIndex(index)

        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == index)