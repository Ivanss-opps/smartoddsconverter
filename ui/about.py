from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class About(QWidget):

    def __init__(self):
        super().__init__()
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("Trading Toolkit v0")
        title.setObjectName("pageTitle")
        title.setAlignment(Qt.AlignCenter)

        description = QLabel("""
-------------------------------------------------------
                                                       
Trading Toolkit v0 is an internal desktop application designed to provide
quick and reliable utilities for the team.

Current tools:

• Odds Key Converter
  Convert prices between different Odds Keys.

• Probability Converter
  Convert between Decimal, Fractional, American and Implied Probability.

• Fair Odds Calculator
  Remove margin from market odds and calculate fair prices.

• Margin Calculator
  Calculate bookmaker margin and overround from market prices.

Future roadmap:

• Arbitrage Calculator
• OCR Odds Reader


-------------------------------------------------------

Version: 0.1.0

Developed by:
I.Silvera and AI
(Almost all AI)
                             
-------------------------------------------------------
                             
Internal Use Only

-------------------------------------------------------                                            
""")

        description.setObjectName("aboutText")
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignTop)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(description)
        layout.addStretch()