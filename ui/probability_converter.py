from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QFrame
)
from PySide6.QtCore import Qt

from logic.probability_logic import ProbabilityConverterEngine


class ProbabilityConverter(QWidget):

    def __init__(self):
        super().__init__()
        self.updating = False
        self.create_ui()

    def create_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        title = QLabel("Probability Converter")
        title.setObjectName("pageTitle")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        self.add_separator(main_layout)

        inputs_layout = QHBoxLayout()

        self.fraction_input = self.create_input("Fraction", "2/1")
        self.decimal_input = self.create_input("Decimal", "3.00")
        self.american_input = self.create_input("American", "+200")
        self.probability_input = self.create_input("Probability %", "33.33")

        inputs_layout.addLayout(self.fraction_input["layout"])
        inputs_layout.addLayout(self.decimal_input["layout"])
        inputs_layout.addLayout(self.american_input["layout"])
        inputs_layout.addLayout(self.probability_input["layout"])

        main_layout.addLayout(inputs_layout)
        main_layout.addStretch()

        self.decimal_input["field"].textChanged.connect(self.decimal_changed)
        self.american_input["field"].textChanged.connect(self.american_changed)
        self.probability_input["field"].textChanged.connect(self.probability_changed)
        self.fraction_input["field"].editingFinished.connect(self.fraction_changed)
        self.fraction_input["field"].textChanged.connect(self.fraction_text_changed)

    def create_input(self, label_text, placeholder):
        layout = QVBoxLayout()

        label = QLabel(label_text)
        label.setObjectName("fieldLabel")
        label.setAlignment(Qt.AlignCenter)

        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)
        layout.addWidget(field)

        return {"layout": layout, "field": field}

    def decimal_changed(self):
        if self.updating:
            return

        try:
            decimal = float(self.decimal_input["field"].text().strip())
        except ValueError:
            self.clear_all()
            return

        if decimal <= 1:
            self.clear_all()
            return

        self.updating = True
        self.american_input["field"].setText(
            ProbabilityConverterEngine.decimal_to_american(decimal)
        )
        self.fraction_input["field"].setText(
            ProbabilityConverterEngine.decimal_to_fraction(decimal)
        )
        self.probability_input["field"].setText(
            ProbabilityConverterEngine.format_probability(
                ProbabilityConverterEngine.decimal_to_probability(decimal)
            )
        )
        self.updating = False

    def american_changed(self):
        if self.updating:
            return

        text = self.american_input["field"].text().strip()

        if text == "":
            self.clear_all()
            return

        text = text.replace("+", "")

        try:
            american = int(text)
        except ValueError:
            return

        if american == 0:
            return

        self.updating = True

        decimal = ProbabilityConverterEngine.american_to_decimal(american)

        self.decimal_input["field"].setText(
            ProbabilityConverterEngine.format_decimal(decimal)
        )
        self.fraction_input["field"].setText(
            ProbabilityConverterEngine.decimal_to_fraction(decimal)
        )
        self.probability_input["field"].setText(
            ProbabilityConverterEngine.format_probability(
                ProbabilityConverterEngine.decimal_to_probability(decimal)
            )
        )

        self.updating = False

    def probability_changed(self):
        if self.updating:
            return

        try:
            probability = float(self.probability_input["field"].text().strip())
        except ValueError:
            self.clear_all()
            return

        if probability <= 0 or probability >= 100:
            self.clear_all()
            return

        self.updating = True

        decimal = ProbabilityConverterEngine.probability_to_decimal(probability)

        self.decimal_input["field"].setText(
            ProbabilityConverterEngine.format_decimal(decimal)
        )
        self.american_input["field"].setText(
            ProbabilityConverterEngine.decimal_to_american(decimal)
        )
        self.fraction_input["field"].setText(
            ProbabilityConverterEngine.decimal_to_fraction(decimal)
        )

        self.updating = False

    def fraction_text_changed(self):
        if self.updating:
            return

        text = self.fraction_input["field"].text().strip()

        if "/" not in text:
            return

        parts = text.split("/")

        if len(parts) != 2:
            return

        if parts[0] == "" or parts[1] == "":
            return

        self.fraction_changed()

    def fraction_changed(self):
        if self.updating:
            return

        text = self.fraction_input["field"].text().strip()

        if text == "":
            self.clear_all()
            return

        decimal = ProbabilityConverterEngine.fraction_to_decimal(text)

        if decimal is None or decimal <= 1:
            return

        self.updating = True

        self.decimal_input["field"].setText(
            ProbabilityConverterEngine.format_decimal(decimal)
        )
        self.american_input["field"].setText(
            ProbabilityConverterEngine.decimal_to_american(decimal)
        )
        self.probability_input["field"].setText(
            ProbabilityConverterEngine.format_probability(
                ProbabilityConverterEngine.decimal_to_probability(decimal)
            )
        )

        self.updating = False

    def clear_all(self):
        if self.updating:
            return

        self.updating = True

        self.fraction_input["field"].clear()
        self.decimal_input["field"].clear()
        self.american_input["field"].clear()
        self.probability_input["field"].clear()

        self.updating = False

    def add_separator(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)