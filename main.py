import pandas as pd
from pathlib import Path
import duckdb
from taipy.gui import Gui
import taipy.gui.builder as tgb
import os

GRAY_1 = "rgb(74, 85, 101)"
GRAY_2 = "rgb(153, 161, 175)"

DATA_DIRECTORY = Path(__file__).parent / "data"

df = pd.read_csv(
    DATA_DIRECTORY / "norway_new_car_sales_by_model.csv", encoding="latin-1"
)
# new deploy

df_year = (
    duckdb.query(
        """
    SELECT 
        year, SUM(quantity) AS Quantity,
    FROM 
        df
    GROUP BY 
        year
    ORDER BY year
"""
    )
    .df()
    .iloc[:-1]
)


properties = {
    "layout": dict(
        title=dict(
            text="Sales per car brand in Norway from 2007 to 2016",
            font=dict(weight="bold", size=18, color=GRAY_1),
            y=1.1,
        ),
        xaxis=dict(
            showgrid=False,
            title=dict(text="YEAR FROM 2007", font=dict(weight="bold", color=GRAY_1)),
        ),
        yaxis=dict(
            showgrid=False,
            title=dict(text="Quantity", font=dict(weight="bold", color=GRAY_1)),
        ),
        hovermode="x",
        annotations=[
            dict(
                text="Dip due to financial crisis",
                x=2009.15,
                y=49500,
                ax=120,
                ay=-30,
                arrowcolor=GRAY_2,
                font=dict(color=GRAY_1),
            )
        ],
        margin=dict(b=80, l=60, t=50, r=0),
    ),
    "marker": dict(size=10, symbol="square"),
    "line": dict(dash="dash", width=3),
}

chart_config = {
    "hovertemplate": "<b>Year:</b> %{x}<br><b>Quantity:</b> %{y}<extra></extra>"
}


port = int(os.environ.get("PORT", 8000))

with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        tgb.text("# Line chart with tgb.chart()", mode="md")
        with tgb.layout(columns="1 1", gap="2rem"):
            with tgb.part() as line_chart:
                tgb.text("## Line Chart", mode="md")

                tgb.chart(
                    "{df_year}",
                    x="Year",
                    y="Quantity",
                    properties="{properties}",
                    options=chart_config,
                )

            with tgb.part() as raw_data:
                tgb.text("## Raw data", mode="md")
                tgb.table("{df}", page_size=7)


if __name__ == "__main__":
    Gui(page=page).run(host="0.0.0.0", port=port, use_reloader=True, dark_mode=False)
