class MarginCalculatorEngine:

    @staticmethod
    def calculate_margin(odds):
        total_probability = 0

        for odd in odds:
            total_probability += 1 / odd

        return total_probability

    @staticmethod
    def calculate_overround(odds):
        margin = MarginCalculatorEngine.calculate_margin(odds)

        return margin - 1

    @staticmethod
    def format_percentage(value):
        return f"{value * 100:.2f}%"

    @staticmethod
    def format_odd(value):
        return f"{value:.2f}"