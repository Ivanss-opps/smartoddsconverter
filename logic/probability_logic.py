from fractions import Fraction


class ProbabilityConverterEngine:

    @staticmethod
    def decimal_to_american(decimal):
        if decimal >= 2:
            return f"+{round((decimal - 1) * 100)}"

        return str(round(-100 / (decimal - 1)))

    @staticmethod
    def american_to_decimal(american):
        if american > 0:
            return (american / 100) + 1

        return (100 / abs(american)) + 1

    @staticmethod
    def decimal_to_fraction(decimal):
        value = decimal - 1
        fraction = Fraction(value).limit_denominator(1000)

        return f"{fraction.numerator}/{fraction.denominator}"

    @staticmethod
    def fraction_to_decimal(value):
        value = value.strip()

        if "/" not in value:
            return None

        parts = value.split("/")

        if len(parts) != 2:
            return None

        try:
            numerator = float(parts[0])
            denominator = float(parts[1])
        except ValueError:
            return None

        if denominator == 0:
            return None

        return (numerator / denominator) + 1

    @staticmethod
    def decimal_to_probability(decimal):
        return 100 / decimal

    @staticmethod
    def probability_to_decimal(probability):
        return 100 / probability

    @staticmethod
    def format_decimal(value):
        return f"{value:.2f}"

    @staticmethod
    def format_probability(value):
        return f"{value:.2f}"