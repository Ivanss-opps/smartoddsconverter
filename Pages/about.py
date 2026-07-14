import streamlit as st


def show_about():
    st.title("About")
    st.divider()

    st.markdown(
        """
## Trading Toolkit v0.0.2

Trading Toolkit is an internal application designed to provide
quick and reliable betting utilities.

### Modules

- Odds Key Converter
- Probability Converter
- Fair Odds Calculator
- Margin Calculator

---

Version 0.0.2

Built with Python & Streamlit by I.S. & AI.
"""
    )
