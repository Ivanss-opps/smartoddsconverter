class FairOddsCalculatorEngine:

    @staticmethod
    def calculate_fair_odds(odds):
        total_probability = 0

        for odd in odds:
            total_probability += 1 / odd

        fair_odds = []

        for odd in odds:
            probability = 1 / odd
            fair_probability = probability / total_probability
            fair_odd = 1 / fair_probability

            fair_odds.append(fair_odd)

        return {
            "market_margin": total_probability,
            "fair_odds": fair_odds
        }

    @staticmethod
    def format_percentage(value):
        return f"{value * 100:.2f}%"

    @staticmethod
    def format_odd(value):
        return f"{value:.2f}"