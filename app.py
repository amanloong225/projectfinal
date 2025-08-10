import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Load your dataset (make sure this CSV is in the same folder as app.py)
data = pd.read_csv("global_food_wastage_dataset.csv")

# Mapping for metric labels
metric_map = {
    "total_waste_(tons)": "Total Waste (Tons)",
    "economic_loss_(million_$)": "Economic Loss (Million $)",
    "avg_waste_per_capita_(kg)": "Avg Waste per Capita (Kg)",
    "household_waste_(%)": "Household Waste (%)"
}

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Global Food Wastage Dashboard"

# App layout
app.layout = html.Div([
    html.H1("Global Food Wastage", style={
        'textAlign': 'center',
        'color': 'darkgreen',
        'fontFamily': 'Fraunces, serif',
        'fontWeight': 'bold'
    }),

    html.Label("Filter by Country:"),
    dcc.Dropdown(
        id="country_filter",
        options=[{"label": c, "value": c} for c in sorted(data["Country"].unique())],
        multi=True,
        placeholder="Select Country(s)"
    ),

    html.Label("Filter by Year:"),
    dcc.Dropdown(
        id="year_filter",
        options=[{"label": y, "value": y} for y in sorted(data["Year"].unique())],
        multi=False,
        placeholder="Select Year"
    ),

    html.Label("Filter by Food Category(s):"),
    dcc.Dropdown(
        id="food_category_filter",
        options=[{"label": f, "value": f} for f in sorted(data["Food Category"].unique())],
        multi=True,
        placeholder="Select Food Category(s)"
    ),

    html.Label("Select Metric:"),
    dcc.Dropdown(
        id="metric_filter",
        options=[
            {"label": "Total Waste (Tons)", "value": "total_waste_(tons)"},
            {"label": "Economic Loss (Million $)", "value": "economic_loss_(million_$)"},
            {"label": "Avg Waste per Capita (Kg)", "value": "avg_waste_per_capita_(kg)"},
            {"label": "Household Waste (%)", "value": "household_waste_(%)"}
        ],
        value="total_waste_(tons)",
        clearable=False
    ),

    dcc.Graph(id="chart")
], style={"padding": "20px"})

# Callback to update chart
@app.callback(
    Output("chart", "figure"),
    Input("country_filter", "value"),
    Input("year_filter", "value"),
    Input("food_category_filter", "value"),
    Input("metric_filter", "value")
)
def update_chart(selected_country, selected_year, selected_food_category, selected_metric):
    filtered_data = data.copy()

    if selected_country:
        filtered_data = filtered_data[filtered_data["Country"].isin(selected_country)]
    if selected_year:
        filtered_data = filtered_data[filtered_data["Year"] == selected_year]
    if selected_food_category:
        filtered_data = filtered_data[filtered_data["Food Category"].isin(selected_food_category)]

    metric_column = metric_map[selected_metric]

    if filtered_data.empty:
        return px.bar(title="No data available for selected filters")

    fig = px.bar(
        filtered_data,
        x="Food Category",
        y=metric_column,
        color="Country",
        barmode="group",
        labels={metric_column: metric_column}
    )

    fig.update_layout(
        title=f"{metric_column} by Food Category ({selected_year})",
        xaxis_title="Food Category",
        yaxis_title=metric_column,
        legend_title="Country"
    )

    return fig

# No need for app.run_server — Render uses gunicorn to serve the app