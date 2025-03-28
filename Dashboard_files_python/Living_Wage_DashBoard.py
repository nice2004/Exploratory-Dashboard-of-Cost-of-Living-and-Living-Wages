
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table, Input, Output, callback
import plotly.graph_objects as go
from Words_in_tabs import About_text, Fun_Wonder_Text, footer
from dash.dependencies import Input, Output

file_path1 = ('./Datasets'
              '/Cost-of-transportation-expenses.xlsx')
file_path2 = ('./Datasets/household'
              '-goods-dataset.xlsx')
file_path3 = ('./Datasets/Median-Income'
              '-Dataset.xlsx')
file_path4 = ('./Datasets/NY-House'
              '-Dataset.csv')

data_set1 = None
data_set2 = None
data_set3 = None
data_set4 = None

def load_data():
    global data_set1, data_set2, data_set3, data_set4
    data_set1 = pd.read_excel(file_path1, sheet_name='Annual')
    data_set2 = pd.read_excel(file_path2, sheet_name='Quarterly')
    data_set3 = pd.read_excel(file_path3, sheet_name='Annual')
    data_set4 = pd.read_csv(file_path4)

    for df in [data_set1, data_set2, data_set3]:
        if 'observation_date' in df.columns:
            df['observation_date'] = pd.to_datetime(df['observation_date']).dt.year

    # merging datasets
    merged_dataset = pd.merge(data_set1, data_set2, on='observation_date', how='outer')
    merged_dataset = pd.merge(merged_dataset, data_set3, on='observation_date', how='outer')

    years = merged_dataset['observation_date'].unique()
    housing_years = []

    for year in years:
        temp_df = data_set4.copy()
        temp_df['observation_date'] = year
        housing_years.append(temp_df)

    housing_with_years = pd.concat(housing_years, ignore_index=True)
    final_dataset = pd.merge(merged_dataset, housing_with_years, on='observation_date', how='inner').dropna(
        subset=['observation_date'])

    final_dataset = final_dataset.ffill().bfill()

    final_dataset['PRICE_PER_SQFT'] = final_dataset['PRICE'] / final_dataset['PROPERTYSQFT']

    # Calculate key expense ratios
    final_dataset['Housing_Income_Ratio'] = final_dataset['PRICE'] / final_dataset['Income']
    final_dataset['Transport_Income_Ratio'] = final_dataset['Transportation_Expense'] / final_dataset['Income']
    final_dataset['Goods_Income_Ratio'] = final_dataset['Durable_Goods'] / final_dataset['Income']
    final_dataset['Total_Expense_Ratio'] = (final_dataset['PRICE'] +
                                            final_dataset['Transportation_Expense'] +
                                            final_dataset['Durable_Goods']) / final_dataset['Income']

    print(final_dataset.head())
    print(final_dataset.columns)

    return final_dataset


merged_dataset = load_data()

COLORS = {
    "Income": "#3cb521",
    "Housing": "#fd7e14",
    "Transportation": "#446e9b",
    "Goods": "#6f42c1",
    "background": "whitesmoke",
}

app = Dash(__name__,
           external_stylesheets=[dbc.themes.JOURNAL, dbc.icons.FONT_AWESOME])

# creating the data table
outcomes_table = dash_table.DataTable(
    id="outcomes-table",
    columns=[{"id": "observation_date", "name": "Year", "type": "text"}] +
            [{"id": "Income", "name": "Income", "type": "numeric", "format": {"specifier": "$,.0f"}}] +
            [{"id": "PRICE", "name": "Housing Price", "type": "numeric", "format": {"specifier": "$,.0f"}}] +
            [{"id": "Transportation_Expense", "name": "Transportation", "type": "numeric",
              "format": {"specifier": "$,.0f"}}] +
            [{"id": "Durable_Goods", "name": "Durable Goods", "type": "numeric",
              "format": {"specifier": "$,.0f"}}] +
            [{"id": "Housing_Income_Ratio", "name": "Housing/Income Ratio", "type": "numeric",
              "format": {"specifier": ".2f"}}] +
            [{"id": "Transport_Income_Ratio", "name": "Transport/Income Ratio", "type": "numeric",
              "format": {"specifier": ".2f"}}] +
            [{"id": "Goods_Income_Ratio", "name": "Goods/Income Ratio", "type": "numeric",
              "format": {"specifier": ".2f"}}] +
            [{"id": "Total_Expense_Ratio", "name": "Total Expense Ratio", "type": "numeric",
              "format": {"specifier": ".2f"}}],
    page_size=10,
    style_table={"overflowX": "scroll"},
    style_cell={
        'textAlign': 'center',
        'padding': '8px'
    },
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    },
    style_data_conditional=[
        {
            'if': {'column_id': 'Total_Expense_Ratio'},
            'backgroundColor': 'rgba(255, 236, 236, 0.7)',
            'color': 'red',
            'fontWeight': 'bold'
        },
    ]
)

# NYC Dropdowns
boroughs_dropdown = dcc.Dropdown(
    id='nyc-counties',
    options=[{'label': str(i), 'value': i} for i in sorted(merged_dataset['SUBLOCALITY'].unique())],
    value=sorted(merged_dataset['SUBLOCALITY'].unique())[0],  # Default to first value
    clearable=False,
    style={'width': '100%'}
)

# dropdown for data selection

dataset_dropdown = dcc.Dropdown(
    id='dataset-dropdown',
    options=[{'label': 'Cost of Transportation', 'value': 'dataset1'},
             {'label': 'Household Goods', 'value': 'dataset2'},
             {'label': 'Median Income', 'value': 'dataset3'},
             {'label': 'NY House Dataset', 'value': 'dataset4'}],
    value='dataset1',
    clearable=False,
    style={'width': '100%'}
)

# housing slider
sqft_slider = dcc.RangeSlider(
    id='sqft-slider',
    min=int(merged_dataset['PROPERTYSQFT'].min()),
    max=int(merged_dataset['PROPERTYSQFT'].max()),
    step=100,
    value=[int(merged_dataset['PROPERTYSQFT'].min()),
           min(3000, int(merged_dataset['PROPERTYSQFT'].max()))],  # Default to a reasonable range
    marks={i: f"{i} sqft" for i in range(
        int(merged_dataset['PROPERTYSQFT'].min()),
        int(merged_dataset['PROPERTYSQFT'].max()) + 1,
        10000)},
    tooltip={"placement": "bottom", "always_visible": True}
)

# year slider
year_slider = dcc.Slider(
    id='year-slider',
    min=merged_dataset['observation_date'].min(),
    max=merged_dataset['observation_date'].max(),
    step=1,
    value=merged_dataset['observation_date'].max(),
    marks={str(year): str(year) for year in
           range(int(merged_dataset['observation_date'].min()),
                 int(merged_dataset['observation_date'].max()) + 1,
                 10)},
    tooltip={"placement": "bottom", "always_visible": True}
)

# Create cards for components
filter_card = dbc.Card([
    dbc.CardHeader("Filter Options", className="text-center"),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.Label("NYC Counties:"),
                boroughs_dropdown
            ], width=12, className="mb-3"),
        ]),
        dbc.Row([
            dbc.Col([
                html.Label("Property Size (Square Feet):"),
                sqft_slider
            ], width=12, className="mb-3"),
        ]),
        dbc.Row([
            dbc.Col([
                html.Label("Select Year:"),
                year_slider
            ], width=12, className="mb-3"),
        ]),
    ])
])
dataset_card = dbc.Card([
    dbc.CardHeader("Select Dataset to Compare"),
    dbc.CardBody([
        dataset_dropdown
    ])
])
# measures the expense to income ratio
metrics_card = dbc.Card([
    dbc.CardHeader("Key Metrics", className="text-center"),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H6("Average Home Price:", className="card-subtitle mb-2 text-muted"),
                    html.H3(id="avg-home-price", className="card-title text-primary")
                ], className="text-center mb-4"),
            ], width=12, md=4),
            dbc.Col([
                html.Div([
                    html.H6("Price/Sqft:", className="card-subtitle mb-2 text-muted"),
                    html.H3(id="price-per-sqft", className="card-title text-primary")
                ], className="text-center mb-4"),
            ], width=12, md=4),
            dbc.Col([
                html.Div([
                    html.H6("Total Expense Ratio:", className="card-subtitle mb-2 text-muted"),
                    html.H3(id="expense-ratio", className="card-title")
                ], className="text-center mb-4"),
            ], width=12, md=4),
        ]),
    ])
])

# ====================================== Tabs

tabs = dbc.Tabs([
    dbc.Tab([
        dbc.Card([
            dbc.CardBody([About_text])
        ], className="mt-3")
    ], tab_id="about-tab", label="About"),

    dbc.Tab([
        dbc.Card([
            dbc.CardHeader('County Predictor'),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H4('Find your Potential NYC County', className='mb-4'),
                        dbc.Form([
                            dbc.CardGroup([
                                dbc.Label('Annual Income ($)'),
                                dbc.Input(
                                    id='income-input',
                                    type='number',
                                    placeholder='Enter annual income',
                                    min=0,
                                    step=10000
                                )
                            ], className='mb-3'),
                            dbc.CardGroup([
                                dbc.Label('Annual Durable Goods Expenses ($)'),
                                dbc.Input(
                                    id='goods-input',
                                    type='number',
                                    placeholder='Enter annual goods expenses',
                                    min=0,
                                    step=100
                                )
                            ], className='mb-3'),
                            dbc.CardGroup([
                                dbc.Label('Annual Transportation  Expenses ($)'),
                                dbc.Input(
                                    id='transport-input',
                                    type='number',
                                    placeholder='Entre annual transportation expense',
                                    min=0,
                                    step=100
                                )

                            ], className='mb-3'),
                            dbc.Button('Find My county', id='predict-button', color='primary', className='mt-3')
                        ])
                    ], width=6),
                    dbc.Col([
                        html.Div(id='prediction-results', className='mt-4')
                    ], width=6)
                ])
            ])

        ], className='mt-3')
    ], tab_id='predictor-tab', label='County Predictor'),

    dbc.Tab([
        dbc.Card([
            dbc.CardBody([Fun_Wonder_Text])
        ], className="mt-3"),
        filter_card,
        dataset_card,
        metrics_card,
        html.Div(className="my-3"),  # Spacer
    ], tab_id="explorer-tab", label="Cost of Living Explorer", active_label_class_name="fw-bold"),

    dbc.Tab([
        dbc.Card([
            dbc.CardHeader("Data Analysis Results"),
            dbc.CardBody([
                html.Div(id="affordability-text", className="alert alert-info mb-3"),
                html.Div([outcomes_table]),
            ])
        ], className="mt-3")
    ], tab_id="results-tab", label="Results"),
], id="tabs", active_tab="explorer-tab", className="mt-2")

# ========================================= App Layout

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Nice Teta Hirwa — CS150 — Professor Mike Ryu",
                        className="bg-primary p-2 mb-2 text-center text-white"))
    ]),
    dbc.Row([
        dbc.Col(html.H2("Cost of Living in New York City",
                        className="text-center bg-primary text-white p-2"))
    ]),
    dbc.Row([
        dbc.Col(tabs, width=12, lg=5, className="mt-4"),
        dbc.Col([
            dcc.Graph(id="expense-chart", className="mb-4 shadow"),
            dcc.Graph(id="historical-trend", className="mb-4 shadow"),
            html.Hr(),
            html.H6(footer, className="my-2 text-center text-muted"),
        ], width=12, lg=7, className="pt-4"),
    ]),
], fluid=True, className="mb-5")


# ================= Functions
def get_affordability_rating(ratio):
    if ratio < 0.5:
        return "Very Affordable", "text-success"
    elif ratio < 0.7:
        return "Affordable", "text-success"
    elif ratio < 1.0:
        return "Moderately Affordable", "text-warning"
    elif ratio < 1.2:
        return "Stretched", "text-warning"
    else:
        return "Expensive", "text-danger"


def empty_bar_chart():
    fig = go.Figure()
    fig.update_layout(
        title="No data available",
        height=400,
        template="plotly_white"
    )
    fig.add_annotation(
        text="Select valid filter options to display data",
        showarrow=False,
        font=dict(size=16)
    )
    return fig


def empty_line_chart():
    fig = go.Figure()
    fig.update_layout(
        title="No data available",
        height=400,
        template="plotly_white"
    )
    fig.add_annotation(
        text="Select valid filter options to display data",
        showarrow=False,
        font=dict(size=16)
    )
    return fig


# ==================================================================== Callbacks
# for updating the dashboard


@callback(
    [Output("expense-chart", "figure"),
     Output("historical-trend", "figure"),
     Output("outcomes-table", "data"),
     Output("avg-home-price", "children"),
     Output("price-per-sqft", "children"),
     Output("expense-ratio", "children"),
     Output("expense-ratio", "className"),
     Output("affordability-text", "children")],
    [Input("nyc-counties", "value"),
     Input("sqft-slider", "value"),
     Input("year-slider", "value"),
     Input("dataset-dropdown", "value")]
)
def update_dashboard(borough, sqft_range, selected_year, dataset_choice):
    line_fig = go.Figure()

    # Select the appropriate dataset and trend columns
    if dataset_choice == "dataset1":
        selected_dataset = data_set1
        trend_columns = {
            "Transportation Expense": {"column": "Transportation_Expense", "color": COLORS["Transportation"]},
            "Income": {"column": "Income", "color": COLORS["Income"]}
        }
    elif dataset_choice == "dataset2":
        selected_dataset = data_set2
        trend_columns = {
            "Durable Goods": {"column": "Durable_Goods", "color": COLORS["Goods"]},
            "Income": {"column": "Income", "color": COLORS["Income"]}
        }
    elif dataset_choice == "dataset3":
        selected_dataset = data_set3
        trend_columns = {
            "Income": {"column": "Income", "color": COLORS["Income"]},
            "Housing Price": {"column": "PRICE", "color": COLORS["Housing"]}
        }
    elif dataset_choice == "dataset4":
        selected_dataset = data_set4
        trend_columns = {
            "Housing Price": {"column": "PRICE", "color": COLORS["Housing"]},
            "Price per Sq Ft": {"column": "PRICE_PER_SQFT", "color": "#ff6b6b"}
        }
    else:
        selected_dataset = merged_dataset
        trend_columns = {}

    # Debug print statements
    print("Dataset Choice:", dataset_choice)
    print("Selected Dataset Columns:", selected_dataset.columns)
    print("Observation Dates:", selected_dataset['observation_date'].unique())
    print("Dataset Shape:", selected_dataset.shape)

    if 'observation_date' not in selected_dataset.columns:
        line_fig = empty_line_chart()
    else:
         # when errors='coerce' is applied, any value that cannot be converted to the desired data type will be replaced with a "Not a Number" value (NaN).
        selected_dataset['observation_date'] = pd.to_numeric(selected_dataset['observation_date'], errors='coerce')

        # Sort the dataset by observation_date
        selected_dataset = selected_dataset.sort_values('observation_date')

        # Create the line graph
        for label, info in trend_columns.items():
            # Check if the column exists in the selected dataset
            if info["column"] in selected_dataset.columns:
                line_fig.add_trace(go.Scatter(
                    x=selected_dataset['observation_date'],
                    y=selected_dataset[info["column"]],
                    mode="lines+markers",
                    name=label,
                    line=dict(color=info["color"], width=3),
                    marker=dict(size=8)
                ))

        # Update layout for the line figure
        line_fig.update_layout(
            title=f"{dataset_choice.replace('dataset', 'Dataset ')} Historical Trends",
            height=400,
            template="plotly_white",
            yaxis=dict(title="Amount ($)", tickprefix="$", tickformat=","),
            xaxis=dict(
                title="Year",
                type='linear',  # Explicitly set linear type
                tickmode="linear",
                # Use the actual min and max years from the dataset
                range=[selected_dataset['observation_date'].min(),
                       selected_dataset['observation_date'].max()],
                tick0=selected_dataset['observation_date'].min(),
                dtick=10
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=100, b=50, l=50, r=50)
        )


    # PART 2: the logic for filtering by year, calculating averages, and preparing output
    filtered_data = merged_dataset[
        (merged_dataset["observation_date"] == selected_year) &
        (merged_dataset["PROPERTYSQFT"] >= sqft_range[0]) &
        (merged_dataset["PROPERTYSQFT"] <= sqft_range[1])
        ]  # Applying filters based on year and sqft

    if filtered_data.empty:
        empty_outputs = [
            empty_bar_chart(), empty_line_chart(), [], "$0", "$0/sqft", "N/A", "card-title", "No data available"
        ]
        return empty_outputs

    # calculating  key metrics
    avg_price = filtered_data["PRICE"].mean()
    avg_price_per_sqft = filtered_data["PRICE_PER_SQFT"].mean()
    avg_income = filtered_data["Income"].mean()
    avg_transport = filtered_data["Transportation_Expense"].mean()
    avg_goods = filtered_data["Durable_Goods"].mean()

    # Calculate expense ratios
    housing_income_ratio = avg_price / avg_income if avg_income > 0 else 0
    transport_income_ratio = avg_transport / avg_income if avg_income > 0 else 0
    goods_income_ratio = avg_goods / avg_income if avg_income > 0 else 0
    total_expense_ratio = housing_income_ratio + transport_income_ratio + goods_income_ratio

    # affordability rating
    affordability_label, affordability_class = get_affordability_rating(total_expense_ratio)

    # Expense chart (Bar chart: Income vs Housing)
    expense_fig = go.Figure()
    categories = ["Income", "Housing"]
    values = [avg_income, avg_price]
    colors = [COLORS["Income"], COLORS["Housing"]]

    expense_fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=[f"${int(val):,}" for val in values],
        textposition="auto"
    ))

    expense_fig.update_layout(
        title=f"Income vs Housing Price for {borough} ({selected_year})",
        height=400,
        template="plotly_white",
        yaxis=dict(title="Amount ($)", tickprefix="$", tickformat=","),
        margin=dict(t=100, b=50, l=50, r=50)
    )

    # line_fig = go.Figure()
    # constant_housing_price = filtered_data["PRICE"].median()

   # metrics = {
    #    "Housing Price": {"column": "PRICE", "color": COLORS["Housing"]},
     #   "Durable Goods": {"column": "Durable_Goods", "color": COLORS["Goods"]},
   #  }

    #for label, info in metrics.items():
     #   if label == "Housing Price":
            # Use constant value for Housing Price across all years
      #      y_values = [constant_housing_price] * len(filtered_data["observation_date"])
       # else:
        #    y_values = filtered_data[info["column"]]

        # line_fig.add_trace(go.Scatter(
          #  x=filtered_data["observation_date"],
           # y=y_values,
            # mode="lines+markers",
          #  name=label,
           # line=dict(color=info["color"], width=3),
           # marker=dict(size=8)
        # ))

    # line_fig.update_layout(
      #  title="Historical Trends",
       # height=400,
       # template="plotly_white",
       # yaxis=dict(title="Amount ($)", tickprefix="$", tickformat=","),
       # xaxis=dict(title="Year", tickmode="linear", range=[1990, filtered_data['observation_date'].max()], tick0=1990,
        #           dtick=5),
        # legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        # margin=dict(t=100, b=50, l=50, r=50)
    # )

    # Prepare table data
    table_data = filtered_data.sort_values("observation_date", ascending=False).copy()
    table_data = table_data.replace([float('inf'), float('-inf')], float('nan'))
    table_data = table_data[[
        "observation_date", "Income", "PRICE", "Transportation_Expense", "Durable_Goods",
        "Housing_Income_Ratio", "Transport_Income_Ratio", "Goods_Income_Ratio", "Total_Expense_Ratio"
    ]].to_dict("records")

    # Create affordability text
    affordability_text = [
        f"Properties in {borough} with size {sqft_range[0]}-{sqft_range[1]} sq.ft cost about ${int(avg_price):,} in {selected_year}.",
        f"With annual income of ${int(avg_income):,}, transportation costs of ${int(avg_transport):,}, and durable goods expenses of ${int(avg_goods):,},",
        f"the total expense-to-income ratio is {total_expense_ratio:.2f}, which is considered {affordability_label.lower()}."
    ]

    if total_expense_ratio > 1.0:
        affordability_text.append(
            "This ratio exceeds the recommended expense-to-income threshold of 1.0, suggesting financial stress.")
    else:
        affordability_text.append(
            "This ratio is within the recommended expense-to-income threshold of 1.0, suggesting financial sustainability.")

    return (
        expense_fig,
        line_fig,
        table_data,
        f"${int(avg_price):,}",
        f"${avg_price_per_sqft:.2f}/sqft",
        f"{total_expense_ratio:.2f}",
        f"card-title {affordability_class}",
        " ".join(affordability_text)
    )


# for predicting the county
@callback(
    Output("prediction-results", "children"),
    [Input("predict-button", "n_clicks")],
    [
        Input("income-input", "value"),
        Input("goods-input", "value"),
        Input("transport-input", "value")
    ],
    prevent_initial_call=True
)
def predict_county(n_clicks, income, goods, transport):
    if not all([income, goods, transport]):
        return dbc.Alert("Please fill in all input fields.", color="warning")

    # Find the closest matches in the dataset
    def find_closest_match(input_value, column):
        differences = abs(merged_dataset[column] - input_value)
        closest_index = differences.idxmin()
        return merged_dataset.loc[closest_index, 'SUBLOCALITY'], merged_dataset.loc[closest_index, column]

    # Find closest counties for each input
    income_county, income_match = find_closest_match(income, 'Income')
    goods_county, goods_match = find_closest_match(goods, 'Durable_Goods')
    transport_county, transport_match = find_closest_match(transport, 'Transportation_Expense')

    # Create results
    results = [
        dbc.Card([
            dbc.CardHeader("Prediction Results", className="text-center"),
            dbc.CardBody([
                html.H5("Based on Your Inputs:", className="card-title mb-3"),

                dbc.Row([
                    dbc.Col([
                        html.H6("Income Prediction", className="text-muted"),
                        html.P(f"County: {income_county}"),
                        html.P(f"Matched Income: ${income_match:,.0f}")
                    ], width=4),

                    dbc.Col([
                        html.H6("Goods Expenses Prediction", className="text-muted"),
                        html.P(f"County: {goods_county}"),
                        html.P(f"Matched Goods Expenses: ${goods_match:,.0f}")
                    ], width=4),

                    dbc.Col([
                        html.H6("Transportation Expenses Prediction", className="text-muted"),
                        html.P(f"County: {transport_county}"),
                        html.P(f"Matched Transport Expenses: ${transport_match:,.0f}")
                    ], width=4)
                ])
            ])
        ], className="mt-3")
    ]

    # Additional context based on the predictions
    if len(set([income_county, goods_county, transport_county])) == 1:
        results.append(
            dbc.Alert(
                f"Interesting! All your inputs closely match the data for {income_county} County.",
                color="success"
            )
        )
    else:
        results.append(
            dbc.Alert(
                "Your inputs match different counties. This could indicate variations in living costs across NYC.",
                color="info"
            )
        )

    return results


if __name__ == '__main__':
    app.run(debug=True)
