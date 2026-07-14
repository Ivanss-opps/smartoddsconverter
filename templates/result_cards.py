class ResultCardsTemplate:

    CARD_BACKGROUND = "#6a6a6a"
    CARD_BORDER = "#9b9b9b"
    TITLE_COLOR = "#111111"
    VALUE_COLOR = "#5f86ff"

    @staticmethod
    def build_cards(cards):
        card_html = ""

        for card in cards:
            card_html += f"""
                <td align="center" style="
                    background-color:{ResultCardsTemplate.CARD_BACKGROUND};
                    border:1px solid {ResultCardsTemplate.CARD_BORDER};
                    padding:18px;
                ">
                    <b style="color:{ResultCardsTemplate.TITLE_COLOR}; font-size:15px;">
                        {card["title"]}
                    </b><br>

                    <span style="
                        font-size:30px;
                        color:{ResultCardsTemplate.VALUE_COLOR};
                        font-weight:bold;
                    ">
                        {card["value"]}
                    </span>
                </td>
            """

        return f"""
            <table width="100%" cellspacing="12">
                <tr>
                    {card_html}
                </tr>
            </table>
        """