from logic.odds_logic import OddsConverterEngine
from templates.result_cards import ResultCardsTemplate


class OddsResultTemplate:

    @staticmethod
    def build(result, labels):
        converted_lines = ""

        for index, label in enumerate(labels):
            original = OddsConverterEngine.format_odd(result["original_odds"][index])
            converted = OddsConverterEngine.format_odd(result["converted_odds"][index])

            converted_lines += f"""
                <p style="font-size:17px; margin:5px 0; color:white; font-weight:normal;">
                    {label}: {original} → <b style="color:#111111;">{converted}</b>
                </p>
            """

        return f"""
        <html>
        <body style="background-color:#5a5a5a; color:white;">

            {ResultCardsTemplate.build_cards([
                {"title": "Detected Odds Key", "value": OddsConverterEngine.format_percentage(result["detected_key"])},
                {"title": "Target Odds Key", "value": OddsConverterEngine.format_percentage(result["target_key"])}
            ])}

            <hr>

            <h3 style="font-size:18px; color:white; font-weight:bold;">
                Converted Odds
            </h3>

            {converted_lines}

        </body>
        </html>
        """