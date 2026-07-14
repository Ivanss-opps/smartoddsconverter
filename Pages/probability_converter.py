import streamlit as st

from logic.probability_logic import ProbabilityConverterEngine


def clear_probability_fields():
    st.session_state.probability_fraction = ""
    st.session_state.probability_decimal = ""
    st.session_state.probability_american = ""
    st.session_state.probability_percent = ""


def convert_from_fraction():
    text = st.session_state.get(
        "probability_fraction",
        "",
    ).strip()

    if text == "":
        clear_probability_fields()
        return

    decimal = ProbabilityConverterEngine.fraction_to_decimal(
        text
    )

    if decimal is None or decimal <= 1:
        return

    st.session_state.probability_decimal = (
        ProbabilityConverterEngine.format_decimal(
            decimal
        )
    )

    st.session_state.probability_american = (
        ProbabilityConverterEngine.decimal_to_american(
            decimal
        )
    )

    st.session_state.probability_percent = (
        ProbabilityConverterEngine.format_probability(
            ProbabilityConverterEngine.decimal_to_probability(
                decimal
            )
        )
    )


def convert_from_decimal():
    text = st.session_state.get(
        "probability_decimal",
        "",
    ).strip()

    try:
        decimal = float(text)
    except ValueError:
        clear_probability_fields()
        return

    if decimal <= 1:
        clear_probability_fields()
        return

    st.session_state.probability_fraction = (
        ProbabilityConverterEngine.decimal_to_fraction(
            decimal
        )
    )

    st.session_state.probability_american = (
        ProbabilityConverterEngine.decimal_to_american(
            decimal
        )
    )

    st.session_state.probability_percent = (
        ProbabilityConverterEngine.format_probability(
            ProbabilityConverterEngine.decimal_to_probability(
                decimal
            )
        )
    )


def convert_from_american():
    text = st.session_state.get(
        "probability_american",
        "",
    ).strip()

    if text == "":
        clear_probability_fields()
        return

    text = text.replace("+", "")

    try:
        american = int(text)
    except ValueError:
        return

    if american == 0:
        return

    decimal = (
        ProbabilityConverterEngine.american_to_decimal(
            american
        )
    )

    st.session_state.probability_decimal = (
        ProbabilityConverterEngine.format_decimal(
            decimal
        )
    )

    st.session_state.probability_fraction = (
        ProbabilityConverterEngine.decimal_to_fraction(
            decimal
        )
    )

    st.session_state.probability_percent = (
        ProbabilityConverterEngine.format_probability(
            ProbabilityConverterEngine.decimal_to_probability(
                decimal
            )
        )
    )


def convert_from_probability():
    text = st.session_state.get(
        "probability_percent",
        "",
    ).strip()

    try:
        probability = float(text)
    except ValueError:
        clear_probability_fields()
        return

    if probability <= 0 or probability >= 100:
        clear_probability_fields()
        return

    decimal = (
        ProbabilityConverterEngine.probability_to_decimal(
            probability
        )
    )

    st.session_state.probability_decimal = (
        ProbabilityConverterEngine.format_decimal(
            decimal
        )
    )

    st.session_state.probability_american = (
        ProbabilityConverterEngine.decimal_to_american(
            decimal
        )
    )

    st.session_state.probability_fraction = (
        ProbabilityConverterEngine.decimal_to_fraction(
            decimal
        )
    )


def initialize_probability_state():
    default_values = {
        "probability_fraction": "",
        "probability_decimal": "",
        "probability_american": "",
        "probability_percent": "",
    }

    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


def show_probability_converter():
    initialize_probability_state()

    st.title("Probability Converter")
    st.divider()

    (
        fraction_column,
        decimal_column,
        american_column,
        probability_column,
    ) = st.columns(4)

    with fraction_column:
        st.text_input(
            "Fraction",
            placeholder="2/1",
            key="probability_fraction",
            on_change=convert_from_fraction,
        )

    with decimal_column:
        st.text_input(
            "Decimal",
            placeholder="3.00",
            key="probability_decimal",
            on_change=convert_from_decimal,
        )

    with american_column:
        st.text_input(
            "American",
            placeholder="+200",
            key="probability_american",
            on_change=convert_from_american,
        )

    with probability_column:
        st.text_input(
            "Probability %",
            placeholder="33.33",
            key="probability_percent",
            on_change=convert_from_probability,
        )
