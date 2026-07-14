from logic.margin_logic import MarginCalculatorEngine
from templates.result_cards import ResultCardsTemplate


class MarginResultTemplate:

    @staticmethod
    def build(margin, overround):
        return f"""
        <html>
        <body style="background-color:#5a5a5a; color:white;">

            {ResultCardsTemplate.build_cards([
                {"title": "Margin", "value": MarginCalculatorEngine.format_percentage(margin)},
                {"title": "Overround", "value": MarginCalculatorEngine.format_percentage(overround)}
            ])}

        </body>
        </html>
        """