import streamlit as st

from logic.margin_logic import MarginCalculatorEngine


def reset_margin_calculator():
    input_keys = [
        "margin_home",
        "margin_draw",
        "margin_away",
    ]

    for key in input_keys:
        st.session_state[key] = ""

    st.session_state.margin_result = None


def margin_market_changed():
    reset_margin_calculator()


def get_market_fields(market):
    if market == "1X2":
        return [
            ("Home", "margin_home"),
            ("Draw", "margin_draw"),
            ("Away", "margin_away"),
        ]

    return [
        ("Home", "margin_home"),
        ("Away", "margin_away"),
    ]


def show_margin_calculator():

    if "margin_result" not in st.session_state:
        st.session_state.margin_result = None

    st.title("Margin Calculator")
    st.divider()

    market = st.selectbox(
        "Market",
        [
            "2-Way",
            "1X2",
        ],
        key="margin_market",
        on_change=margin_market_changed,
    )

    st.divider()
    st.subheader("Input Odds")

    market_fields = get_market_fields(market)

    with st.form("margin_form"):

        for label, key in market_fields:
            st.text_input(
                label,
                key=key,
                placeholder=f"Enter {label} odds",
            )

        st.divider()

        c1, c2 = st.columns(2)

        with c1:
            calculate = st.form_submit_button(
                "Calculate",
                use_container_width=True,
            )

        with c2:
            st.form_submit_button(
                "Reset",
                use_container_width=True,
                on_click=reset_margin_calculator,
            )

    if calculate:

        odds = []

        valid = True

        for _, key in market_fields:

            value = st.session_state[key].strip()

            try:

                odd = float(value)

                if odd <= 1:
                    valid = False
                    break

                odds.append(odd)

            except ValueError:

                valid = False
                break

        if not valid:

            st.error("Please enter valid odds.")
            st.session_state.margin_result = None

        else:

            margin = MarginCalculatorEngine.calculate_margin(odds)

            overround = MarginCalculatorEngine.calculate_overround(
                odds
            )

            st.session_state.margin_result = {
                "margin": margin,
                "overround": overround,
            }

    st.divider()
    st.subheader("Results")

    result = st.session_state.margin_result

    if result is None:

        st.info("Waiting for calculation...")

    else:

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Market %",
                MarginCalculatorEngine.format_percentage(
                    result["margin"]
                ),
            )

        with c2:
            st.metric(
                "Overround",
                MarginCalculatorEngine.format_percentage(
                    result["overround"]
                ),
            )
