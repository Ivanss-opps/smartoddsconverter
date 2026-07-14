import streamlit as st

from Pages.about import show_about
from Pages.fair_odds_calculator import show_fair_odds_calculator
from Pages.margin_calculator import show_margin_calculator
from Pages.odds_converter import show_odds_converter
from Pages.probability_converter import show_probability_converter


st.set_page_config(
    page_title="Trading Toolkit",
    layout="wide",
)


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
    show_odds_converter()

elif page == "Probability Converter":
    show_probability_converter()

elif page == "Fair Odds Calculator":
    show_fair_odds_calculator()

elif page == "Margin Calculator":
    show_margin_calculator()

elif page == "About":
    show_about()
