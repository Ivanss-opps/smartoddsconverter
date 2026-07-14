from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QLineEdit, QPushButton, QFrame
)
from PySide6.QtCore import Qt

from logic.odds_logic import OddsConverterEngine
from templates.odds_result import OddsResultTemplate


class OddsConverter(QWidget):

    def __init__(self):
        super().__init__()
        self.input_fields = []
        self.create_ui()

    def create_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        title = QLabel("Odds Key Converter")
        title.setObjectName("pageTitle")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        self.add_separator(main_layout)

        settings_layout = QHBoxLayout()

        market_layout = QVBoxLayout()
        market_label = QLabel("Market")
        market_label.setObjectName("fieldLabel")

        self.market_select = QComboBox()
        self.market_select.addItems(["Winner", "1X2", "Totals", "Handicap"])
        self.market_select.currentTextChanged.connect(self.update_inputs)

        market_layout.addWidget(market_label)
        market_layout.addWidget(self.market_select)

        odds_key_layout = QVBoxLayout()
        odds_key_label = QLabel("Target Odds Key")
        odds_key_label.setObjectName("fieldLabel")

        self.odds_key_select = QComboBox()

        for value in range(100, 121):
            self.odds_key_select.addItem(f"{value}%")

        self.odds_key_select.setCurrentText("108%")

        odds_key_layout.addWidget(odds_key_label)
        odds_key_layout.addWidget(self.odds_key_select)

        settings_layout.addLayout(market_layout)
        settings_layout.addLayout(odds_key_layout)

        main_layout.addLayout(settings_layout)

        self.add_separator(main_layout)

        input_title = QLabel("Input Odds")
        input_title.setObjectName("sectionTitle")
        main_layout.addWidget(input_title)
        main_layout.addSpacing(12)

        self.inputs_layout = QVBoxLayout()
        main_layout.addLayout(self.inputs_layout)

        self.add_separator(main_layout)

        buttons_layout = QHBoxLayout()

        self.convert_button = QPushButton("Convert")
        self.reset_button = QPushButton("Reset")

        self.convert_button.clicked.connect(self.convert_odds)
        self.reset_button.clicked.connect(self.reset_form)

        buttons_layout.addWidget(self.convert_button)
        buttons_layout.addWidget(self.reset_button)

        main_layout.addLayout(buttons_layout)

        main_layout.addSpacing(12)
        self.add_separator(main_layout)

        results_title = QLabel("Results")
        results_title.setObjectName("sectionTitle")
        main_layout.addWidget(results_title)

        self.result_label = QLabel("Waiting for conversion...")
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

        market = self.market_select.currentText()

        if market == "1X2":
            labels = ["Home", "Draw", "Away"]
        elif market == "Totals":
            labels = ["Over", "Under"]
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

        self.result_label.setText("Waiting for conversion...")

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

    def get_target_key(self):
        text = self.odds_key_select.currentText()
        value = text.replace("%", "")

        return float(value) / 100

    def convert_odds(self):
        odds = self.get_input_odds()

        if odds is None:
            self.result_label.setText("Please enter valid odds.")
            return

        target_key = self.get_target_key()

        result = OddsConverterEngine.convert(odds, target_key)

        self.show_result(result)

    def show_result(self, result):
        market = self.market_select.currentText()

        if market == "1X2":
            labels = ["Home", "Draw", "Away"]
        elif market == "Totals":
            labels = ["Over", "Under"]
        else:
            labels = ["Home", "Away"]

        html = OddsResultTemplate.build(result, labels)
        self.result_label.setText(html)

    def reset_form(self):
        for field in self.input_fields:
            field.clear()

        self.result_label.setText("Waiting for conversion...")

    def add_separator(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)