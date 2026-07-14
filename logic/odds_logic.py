class OddsConverterEngine:

    @staticmethod
    def detect_odds_key(odds):
        total_probability = 0

        for odd in odds:
            total_probability += 1 / odd

        return total_probability

    @staticmethod
    def convert(odds, target_key):
        detected_key = OddsConverterEngine.detect_odds_key(odds)

        factor = target_key / detected_key

        converted_odds = []

        for odd in odds:
            probability = 1 / odd
            new_probability = probability * factor
            new_odd = 1 / new_probability

            converted_odds.append(new_odd)

        return {
            "detected_key": detected_key,
            "target_key": target_key,
            "original_odds": odds,
            "converted_odds": converted_odds
        }

    @staticmethod
    def format_percentage(value):
        return f"{value * 100:.2f}%"

    @staticmethod
    def format_odd(value):
        return f"{value:.2f}"