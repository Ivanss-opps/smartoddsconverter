import streamlit as st


st.set_page_config(
    page_title="Trading Toolkit v0",
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
    st.title("Odds Key Converter")
    st.divider()
    st.write("Streamlit conversion in progress.")

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
