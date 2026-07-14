import streamlit as st

from logic.fair_odds_logic import FairOddsCalculatorEngine


def reset_fair_odds_calculator():
    input_keys = [
        "fair_odds_home",
        "fair_odds_draw",
        "fair_odds_away",
    ]

    for key in input_keys:
        st.session_state[key] = ""

    st.session_state.fair_odds_result = None


def fair_market_changed():
    reset_fair_odds_calculator()


def get_fair_market_fields(market):
    if market == "1X2":
        return [
            ("Home", "fair_odds_home"),
            ("Draw", "fair_odds_draw"),
            ("Away", "fair_odds_away"),
        ]

    return [
        ("Home", "fair_odds_home"),
        ("Away", "fair_odds_away"),
    ]


def show_fair_odds_calculator():
    if "fair_odds_result" not in st.session_state:
        st.session_state.fair_odds_result = None

    st.title("Fair Odds Calculator")
    st.divider()

    market = st.selectbox(
        "Market",
        options=[
            "2-Way",
            "1X2",
        ],
        key="fair_odds_market",
        on_change=fair_market_changed,
    )

    st.divider()
    st.subheader("Input Odds")

    market_fields = get_fair_market_fields(market)

    with st.form("fair_odds_form"):
        for label, input_key in market_fields:
            st.text_input(
                label,
                placeholder=f"Enter {label} odds",
                key=input_key,
            )

        st.divider()

        calculate_column, reset_column = st.columns(2)

        with calculate_column:
            calculate_button = st.form_submit_button(
                "Calculate",
                use_container_width=True,
            )

        with reset_column:
            st.form_submit_button(
                "Reset",
                use_container_width=True,
                on_click=reset_fair_odds_calculator,
            )

    if calculate_button:
        odds = []
        valid_odds = True

        for _, input_key in market_fields:
            input_text = st.session_state.get(
                input_key,
                "",
            ).strip()

            try:
                odd = float(input_text)

                if odd <= 1:
                    valid_odds = False
                    break

                odds.append(odd)

            except ValueError:
                valid_odds = False
                break

        if not valid_odds:
            st.session_state.fair_odds_result = None
            st.error("Please enter valid odds.")

        else:
            st.session_state.fair_odds_result = (
                FairOddsCalculatorEngine.calculate_fair_odds(
                    odds
                )
            )

    st.divider()
    st.subheader("Results")

    result = st.session_state.fair_odds_result

    if result is None:
        st.markdown(
            """
            <p style="text-align: center;">
                Waiting for calculation...
            </p>
            """,
            unsafe_allow_html=True,
        )

    else:
        market_margin = (
            FairOddsCalculatorEngine.format_percentage(
                result["market_margin"]
            )
        )

        st.metric(
            "Market Margin",
            market_margin,
        )

        st.divider()
        st.subheader("Fair Odds")

        labels = [
            label
            for label, _ in market_fields
        ]

        for index, label in enumerate(labels):
            fair_odd = (
                FairOddsCalculatorEngine.format_odd(
                    result["fair_odds"][index]
                )
            )

            label_column, value_column = st.columns(
                [2, 1]
            )

            with label_column:
                st.write(f"**{label}**")

            with value_column:
                st.write(f"**{fair_odd}**")
