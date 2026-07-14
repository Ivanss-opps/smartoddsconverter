from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QComboBox
)
from PySide6.QtCore import Qt

from logic.margin_logic import MarginCalculatorEngine
from templates.margin_result import MarginResultTemplate


class MarginCalculator(QWidget):

    def __init__(self):
        super().__init__()
        self.input_fields = []
        self.create_ui()

    def create_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        title = QLabel("Margin Calculator")
        title.setObjectName("pageTitle")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        self.add_separator(main_layout)

        market_label = QLabel("Market")
        market_label.setObjectName("fieldLabel")

        self.market_select = QComboBox()
        self.market_select.addItems(["2-Way", "1X2"])
        self.market_select.currentTextChanged.connect(self.update_inputs)

        main_layout.addWidget(market_label)
        main_layout.addWidget(self.market_select)

        self.add_separator(main_layout)

        input_title = QLabel("Input Odds")
        input_title.setObjectName("sectionTitle")
        main_layout.addWidget(input_title)
        main_layout.addSpacing(12)

        self.inputs_layout = QVBoxLayout()
        main_layout.addLayout(self.inputs_layout)

        self.add_separator(main_layout)

        buttons_layout = QHBoxLayout()

        self.calculate_button = QPushButton("Calculate")
        self.reset_button = QPushButton("Reset")

        self.calculate_button.clicked.connect(self.calculate_margin)
        self.reset_button.clicked.connect(self.reset_form)

        buttons_layout.addWidget(self.calculate_button)
        buttons_layout.addWidget(self.reset_button)

        main_layout.addLayout(buttons_layout)

        main_layout.addSpacing(12)
        self.add_separator(main_layout)

        results_title = QLabel("Results")
        results_title.setObjectName("sectionTitle")
        main_layout.addWidget(results_title)

        self.result_label = QLabel("Waiting for calculation...")
        self.result_label.setObjectName("placeholderText")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setTextFormat(Qt.RichText)
        self.result_label.setWordWrap(True)

        main_layout.addWidget(self.result_label)
        main_layout.addStretch()

        self.update_inputs()

    def update_inputs(self):
        while self.inputs_layout.count():
            item = self.inputs_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        self.input_fields = []

        if self.market_select.currentText() == "1X2":
            labels = ["Home", "Draw", "Away"]
        else:
            labels = ["Home", "Away"]

        for label_text in labels:
            label = QLabel(label_text)
            label.setObjectName("fieldLabel")

            field = QLineEdit()
            field.setPlaceholderText(f"Enter {label_text} odds")

            self.inputs_layout.addWidget(label)
            self.inputs_layout.addWidget(field)

            self.input_fields.append(field)

        self.result_label.setText("Waiting for calculation...")

    def get_input_odds(self):
        odds = []

        for field in self.input_fields:
            text = field.text().strip()

            try:
                odd = float(text)
            except ValueError:
                return None

            if odd <= 1:
                return None

            odds.append(odd)

        return odds

    def calculate_margin(self):
        odds = self.get_input_odds()

        if odds is None:
            self.result_label.setText("Please enter valid odds.")
            return

        margin = MarginCalculatorEngine.calculate_margin(odds)
        overround = MarginCalculatorEngine.calculate_overround(odds)

        html = MarginResultTemplate.build(margin, overround)

        self.result_label.setText(html)

    def reset_form(self):
        for field in self.input_fields:
            field.clear()

        self.result_label.setText("Waiting for calculation...")

    def add_separator(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)