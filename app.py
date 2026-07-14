import streamlit as st

from logic.odds_logic import OddsConverterEngine


st.set_page_config(
    page_title="Trading Toolkit v0",
    layout="wide",
)


def reset_odds_converter():
    """Clear the Odds Key Converter inputs and result."""
    keys_to_remove = [
        key
        for key in st.session_state
        if key.startswith("odds_input_")
    ]

    for key in keys_to_remove:
        del st.session_state[key]

    st.session_state.odds_result = None


def market_changed():
    """Reset inputs and result when the selected market changes."""
    reset_odds_converter()


if "odds_result" not in st.session_state:
    st.session_state.odds_result = None


st.sidebar.title("Trading Toolkit v0")

page = st.sidebar.radio(
    "Navigation",
    [
        "Odds Key Converter",
        "Probability Converter",
        "Fair Odds Calculator",
        "Margin Calculator",
        "About",
    ],
)


if page == "Odds Key Converter":
    st.title("Odds Key Converter")
    st.divider()

    settings_column_1, settings_column_2 = st.columns(2)

    with settings_column_1:
        market = st.selectbox(
            "Market",
            ["Winner", "1X2", "Totals", "Handicap"],
            key="odds_market",
            on_change=market_changed,
        )

    with settings_column_2:
        target_key_text = st.selectbox(
            "Target Odds Key",
            [f"{value}%" for value in range(100, 121)],
            index=8,
            key="odds_target_key",
        )

    st.divider()
    st.subheader("Input Odds")

    if market == "1X2":
        labels = ["Home", "Draw", "Away"]
    elif market == "Totals":
        labels = ["Over", "Under"]
    else:
        labels = ["Home", "Away"]

    with st.form("odds_converter_form"):
        input_keys = []

        for index, label in enumerate(labels):
            input_key = f"odds_input_{index}"
            input_keys.append(input_key)

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

        for input_key in input_keys:
            text = st.session_state.get(input_key, "").strip()

            try:
                odd = float(text)

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
            target_key = float(
                target_key_text.replace("%", "")
            ) / 100

            st.session_state.odds_result = OddsConverterEngine.convert(
                odds,
                target_key,
            )

    st.divider()
    st.subheader("Results")

    if st.session_state.odds_result is None:
        st.markdown(
            "<p style='text-align:center;'>Waiting for conversion...</p>",
            unsafe_allow_html=True,
        )

    else:
        result = st.session_state.odds_result

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

        for index, label in enumerate(labels):
            original_odd = OddsConverterEngine.format_odd(
                result["original_odds"][index]
            )

            converted_odd = OddsConverterEngine.format_odd(
                result["converted_odds"][index]
            )

            label_column, original_column, arrow_column, converted_column = (
                st.columns([2, 1, 0.4, 1])
            )

            with label_column:
                st.write(f"**{label}**")

            with original_column:
                st.write(original_odd)

            with arrow_column:
                st.write("→")

            with converted_column:
                st.write(f"**{converted_odd}**")

elif page == "Probability Converter":
    st.title("Probability Converter")
    st.divider()
    st.write("Streamlit conversion in progress.")


elif page == "Fair Odds Calculator":
    st.title("Fair Odds Calculator")
    st.divider()
    st.write("Streamlit conversion in progress.")


elif page == "Margin Calculator":
    st.title("Margin Calculator")
    st.divider()
    st.write("Streamlit conversion in progress.")


elif page == "About":
    st.title("Trading Toolkit v0")
    st.divider()

    st.write(
        """
        Trading Toolkit v0 is an internal application designed to provide
        quick and reliable utilities for the team.
        """
    )
