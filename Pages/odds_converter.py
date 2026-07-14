import streamlit as st

from logic.odds_logic import OddsConverterEngine


def reset_odds_converter():
    input_keys = [
        "odds_input_home",
        "odds_input_draw",
        "odds_input_away",
        "odds_input_over",
        "odds_input_under",
    ]

    for key in input_keys:
        st.session_state[key] = ""

    st.session_state.odds_result = None


def market_changed():
    reset_odds_converter()


def get_market_configuration(market):
    if market == "1X2":
        return [
            ("Home", "odds_input_home"),
            ("Draw", "odds_input_draw"),
            ("Away", "odds_input_away"),
        ]

    if market == "Totals":
        return [
            ("Over", "odds_input_over"),
            ("Under", "odds_input_under"),
        ]

    return [
        ("Home", "odds_input_home"),
        ("Away", "odds_input_away"),
    ]


def show_odds_converter():
    if "odds_result" not in st.session_state:
        st.session_state.odds_result = None

    st.title("Odds Key Converter")
    st.divider()

    settings_column_1, settings_column_2 = st.columns(2)

    with settings_column_1:
        market = st.selectbox(
            "Market",
            options=[
                "Winner",
                "1X2",
                "Totals",
                "Handicap",
            ],
            key="odds_market",
            on_change=market_changed,
        )

    with settings_column_2:
        target_key_text = st.selectbox(
            "Target Odds Key",
            options=[
                f"{value}%"
                for value in range(100, 121)
            ],
            index=8,
            key="odds_target_key",
        )

    st.divider()
    st.subheader("Input Odds")

    market_fields = get_market_configuration(market)

    with st.form("odds_converter_form"):
        for label, input_key in market_fields:
            st.text_input(
                label,
                placeholder=f"Enter {label} odds",
                key=input_key,
            )

        st.divider()

        button_column_1, button_column_2 = st.columns(2)

        with button_column_1:
            convert_button = st.form_submit_button(
                "Convert",
                use_container_width=True,
            )

        with button_column_2:
            st.form_submit_button(
                "Reset",
                use_container_width=True,
                on_click=reset_odds_converter,
            )

    if convert_button:
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
            st.session_state.odds_result = None
            st.error("Please enter valid odds.")

        else:
            target_key = (
                float(
                    target_key_text.replace("%", "")
                )
                / 100
            )

            st.session_state.odds_result = (
                OddsConverterEngine.convert(
                    odds,
                    target_key,
                )
            )

    st.divider()
    st.subheader("Results")

    result = st.session_state.odds_result

    if result is None:
        st.markdown(
            """
            <p style="text-align: center;">
                Waiting for conversion...
            </p>
            """,
            unsafe_allow_html=True,
        )

    else:
        detected_column, target_column = st.columns(2)

        with detected_column:
            st.metric(
                "Detected Odds Key",
                OddsConverterEngine.format_percentage(
                    result["detected_key"]
                ),
            )

        with target_column:
            st.metric(
                "Target Odds Key",
                OddsConverterEngine.format_percentage(
                    result["target_key"]
                ),
            )

        st.divider()
        st.subheader("Converted Odds")

        labels = [
            label
            for label, _ in market_fields
        ]

        for index, label in enumerate(labels):
            original_odd = (
                OddsConverterEngine.format_odd(
                    result["original_odds"][index]
                )
            )

            converted_odd = (
                OddsConverterEngine.format_odd(
                    result["converted_odds"][index]
                )
            )

            (
                label_column,
                original_column,
                arrow_column,
                converted_column,
            ) = st.columns([2, 1, 0.4, 1])

            with label_column:
                st.write(f"**{label}**")

            with original_column:
                st.write(original_odd)

            with arrow_column:
                st.write("→")

            with converted_column:
                st.write(f"**{converted_odd}**")
