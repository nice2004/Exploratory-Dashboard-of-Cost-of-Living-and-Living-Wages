import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table, Input, Output, State
import plotly.graph_objects as go
from Words_in_tabs import datasource_text, Fun_Wonder_Text, About_text, footer
from dash import html
import dash_core_components as dcc

data_set1 = pd.read_excel('Cost-of-transportation-expenses.xlsx', sheet_name='Annual')
data_set2 = pd.read_excel('household-goods-dataset.xlsx', sheet_name='Quarterly')
data_set3 = pd.read_excel('Median-Income-Dataset.xlsx', sheet_name='Annual')
data_set4 = pd.read_csv('NY-House-Dataset.csv')

merged_dataset = pd.merge(data_set1, data_set2, on='observation_date', how='outer')
merged_dataset = pd.merge(merged_dataset, data_set3, on='observation_date', how='outer')
merged_dataset = pd.merge(merged_dataset, data_set4, how='cross')

print(merged_dataset.columns)


app = Dash(__name__,
           external_stylesheets=[dbc.themes.JOURNAL, dbc.icons.FONT_AWESOME])

# maximum value in the 'observation_date' column of a DataFrame
MAX_YR = merged_dataset.observation_date.max()
MIN_YR = merged_dataset.observation_date.min()
START_YR = 1990

# Sorting the df in order so that it is arranged in years
# row = pd.DataFrame({'observation_date': [MIN_YR - 1]})
# df = (pd.concat([merged_dataset, row], ignore_index=True).sort_values(
#    'observation_date', ignore_index=True
# ).fillna(0))

COLORS = {
    "Income": "#3cb521",
    "Goods": "#fd7e14",
    "Transportation expenses": "#446e9b",
    "background": "whitesmoke",
}

""""
============================================
Markdown Text
Export Please 
"""

"""
==========================================================================
Tables
"""

outcomes_table = dash_table.DataTable(
    id="outcomes",
    columns=[{"id": "observation_date", "name": "Year", "type": "text"}]
            + [
                {"id": col, "name": col, "type": "numeric", "format": {"specifier": "$,.0f"}}
                for col in merged_dataset.columns[1:]
            ],
    page_size=15,
    style_table={"overflowX": "scroll"},
)

"""
==========================================================================
Figures
"""


def make_bar(slider_input, title):
    fig = go.Figure(
        data=[
            go.Bar(
                x=["Income", "Housing", "Transportation"],
                y=slider_input,
                textposition="inside",
                marker=dict(color=[COLORS["Income"], COLORS["Housing"], COLORS["Transportation"]]),

            )
        ]
    )
    fig.update_layout(
        title_text=title,
        title_x=0.5,
        margin=dict(b=25, t=75, l=35, r=25),
        height=325,
        paper_bgcolor=COLORS["background"],
        xaxis_title='Asset Type',
        yaxis_title='Percentage',
        showlegend=False,
    )
    return fig


def make_line_chart(dff, selected_column):
    fig = go.Figure()

    # start = merged_dataset.loc[1, "observation_data"]
    # yrs = merged_dataset["observation_data"].size - 1
    # dtick = 1 if yrs < 16 else 2 if yrs in range(16, 30) else 5
    for col in selected_column:
        fig.add_trace(
            go.Scatter(
                x=dff["observation_data"],
                y=dff[col],
                mode='lines',
                name=col,
                marker_color=COLORS.get(col, '#000000')
            )
        )

    fig.update_layout(
        title=f"Multiple Line Charts: {','.join(selected_column)}",
        template="none",
        showlegend=True,
        legend=dict(x=0.01, y=0.99),
        height=400,
        margin=dict(l=40, r=10, t=60, b=55),
        yaxis=dict(tickprefix="$", fixedrange=True),
        xaxis=dict(title="Year Ended", fixedrange=True),
    )
    return fig


"""
==========================================================================
Make Tabs
"""

previous_button = dbc.Button('Previous Setting', id='previous-setting-btn', n_clicks=0, disabled=True, color='primary')
# Add the text in fun and wonders
Fun_wonders_card = dbc.Card(Fun_Wonder_Text, className="mt-2")

# Make a dropdown that people can select of baths and bedrooms

Bathrooms = dbc.InputGroup(
    [dbc.InputGroupText('Nbr of Bathrooms'),
     dcc.Dropdown(
         id='Nbr of Bathrooms',
         options=[
             {'label': str(i), 'value': i} for i in range(1, int(merged_dataset['BATH'].max()) + 1)
         ],
         value=1,  # default value
         placeholder='Select a value',
         style={'width': '60%', 'font-size': '20px', 'height': '40px'},
     ),
     ],
    className='mb-3'
)

Cities = dbc.InputGroup([
    dbc.InputGroupText('NewYork Counties'),
    dcc.Dropdown(
        id='NewYork Counties',
        options=[{'label': str(i), 'value': i} for i in merged_dataset['SUBLOCALITY'].unique()],
        value='Brookyln',
        placeholder='Select a city',
        style={'width': '60%', 'font-size': '20px', 'height': '40px'},
    ),
],
    className='mb-3'
)

Beds = dbc.InputGroup(
    [dbc.InputGroupText('Nbr of Beds'),
     dcc.Dropdown(
         id='Nbr of Beds',
         options=[
             {'label': str(i), 'value': i} for i in range(1, int(merged_dataset['BEDS'].max()) + 1)
         ],
         value=1,  # default value
         placeholder='Select a value',
         style={'width': '60%', 'font-size': '20px', 'height': '40px'},

     ),
     ],
    className='mb-3'
)

drop_downs_card = dbc.Card([
    dbc.CardHeader('Dropdowns'),
    dbc.CardBody([
        Cities,
        Bathrooms,
        Beds
    ])
])

app.layout = html.Div([
    drop_downs_card
])

# the slider that plays the time period buttons
# An animation slide

column_dropdown = dcc.Dropdown(
    id='column-dropdown',
    options=[{'label': col, 'value': col} for col in ['Transportation_Expense', 'Durable_Goods', 'Income', 'PRICE']
             ],
    multi=True,
    value='Transportation-Expense',  # Default Value
    style={'width': '50%'}
)
select_colum_card = dbc.Card([

        html.H4('Select Dataset', className='card_title'),
        html.Div(id='column-value', className='card-text'),

])
column_card = dbc.Card([
    dbc.CardHeader('Datasets'),
    dbc.CardBody([
        column_dropdown,
        select_colum_card,

    ])
])
app.layout = html.Div([
    column_dropdown,
    select_colum_card
])

# =====  Results Tab components

outcome_card = dbc.Card(
    [
        dbc.CardHeader("My Dream life on living in NYC"),
        html.Div([outcomes_table]),
    ],
    className="mt-4",
)

# ==== History Tab Component


# ==== About Tab Components
about_card = dbc.Card(
    [
        dbc.CardHeader("Welcome to your dream life of living in NYC"),
        dbc.CardBody(About_text),  # Insert the learn text in here
    ],
    className="mt-4",
)

# ========= Build tabs
tabs = dbc.Tabs(
    [
        dbc.Tab(about_card, tab_id="tab1", label="About"),
        dbc.Tab(
            [Fun_wonders_card, drop_downs_card, column_card],
            tab_id="tab-2",
            label="Fun and Wonders",
            className="pb-4",
        ),
        dbc.Tab([outcome_card], tab_id="tab-3", label="Results"),

    ],
    id="tabs",
    active_tab="tab-2",
    className="mt-2",
)

"""
==========================================================================
Helper functions to calculate investment results, cagr and worst periods
"""

"""
===========================================================================
Main Layout
"""

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H2(
                    "Nice Teta Hirwa -- CS150 -- Professor Mike Ryu",
                    className="bg-primary p-2 mb-2 text-center",
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                html.H2(
                    "Cost of Living Wages in NewYork City",
                    className="text-center bg-primary text-white p-2",
                ),
            )
        ),
        dbc.Row(
            [
                dbc.Col(tabs, width=12, lg=5, className="mt-4 border"),
                dbc.Col(
                    [
                        dcc.Graph(id="Income and Expenses_bar_chart", className="mb-2"),
                        dcc.Graph(id="Changes_Over-Time_Chart", className="pb-4"),
                        html.Hr(),
                        html.H6(footer, className="my-2"),
                    ],
                    width=12,
                    lg=7,
                    className="pt-4",
                ),
            ],
            className="ms-1",
        ),
    ],
    fluid=True,
)

"""
==========================================================================
Callbacks
"""


@app.callback(
    Output('Income and Expenses_bar_chart', 'figure'),
    Input('NewYork Counties', 'value'),
    Input('Nbr of Bathrooms', 'value'),
    Input('Nbr of Beds', 'value')
)
def update_bar_chart(cities, bathrooms, beds):
    filtered_data = merged_dataset[
        (merged_dataset['BEDS'] == beds) &
        (merged_dataset['SUBLOCALITY'] == cities) &
        (merged_dataset['BATH'] == bathrooms)
        ]

    if filtered_data.empty:
        return go.Figure()

    average_price = filtered_data['PRICE'].mean()
    average_income = filtered_data['Income'].mean()
    average_expense = filtered_data['Transportation_Expense'].mean()
    print(filtered_data.head())

    bar_data = [
        go.Bar(
            x=['Price', 'Income', 'Transportation Expense'],
            y=[average_price, average_income, average_expense],
            textposition='inside',
            marker=dict(color=[COLORS['Income'], COLORS['Goods'], COLORS['Transportation Expenses']])
        )
    ]

    bar_fig = go.Figure(data=bar_data)

    bar_fig.update_layout(
        title='Price, Income, and Transportation expense',
        title_x=0.5,
        height=3.25,
        margin=dict(b=25, t=75, l=35, r=25),
        xaxis_title='Category',
        yaxis_title='Amount ($)',
        showlegend=False,
    )

    return bar_fig


@app.callback(
    Output('Changes_Over-Time_Chart', 'figure'),
    Input('column-dropdown', 'value')
)
def update_line_chart(selected_column):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=merged_dataset['observation_date'],
            y=merged_dataset[selected_column],
            mode='lines',
            name=selected_column,
            marker_color=COLORS.get(selected_column, '#000000')
        )
    )
    fig.update_layout(
        title=f'{selected_column} Over Time',
        template='none',
        showlegend=True,
        legend=dict(x=0.01, y=0.99),
        height=400,
        margin=dict(l=40, r=10, t=60, b=55),
        yaxis=dict(tickprefix='$', fixedrange=True),
        xaxis=dict(title='Year Ended', fixedrange=True),
    )

    return fig


if __name__ == '__main__':
    app.run(debug=True)
