from logic.fair_odds_logic import FairOddsCalculatorEngine
from templates.result_cards import ResultCardsTemplate


class FairResultTemplate:

    @staticmethod
    def build(result, labels):
        fair_lines = ""

        for index, label in enumerate(labels):
            fair_odd = FairOddsCalculatorEngine.format_odd(result["fair_odds"][index])

            fair_lines += f"""
                <p style="font-size:17px; margin:5px 0; color:white; font-weight:normal;">
                    {label}: <b style="color:#111111;">{fair_odd}</b>
                </p>
            """

        return f"""
        <html>
        <body style="background-color:#5a5a5a; color:white;">

            {ResultCardsTemplate.build_cards([
                {"title": "Original Odds Key", "value": FairOddsCalculatorEngine.format_percentage(result["market_margin"])},
                {"title": "Target Odds Key", "value": "100.00%"}
            ])}

            <hr>

            <h3 style="font-size:18px; color:white; font-weight:bold;">
                Fair Odds
            </h3>

            {fair_lines}

        </body>
        </html>
        """