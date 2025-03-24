from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context

"""
==========================================================================
Markdown Text
"""

datasource_text = dcc.Markdown(
    """
    [Data source:](https://fred.stlouisfed.org/series/BOGZ1LM155111005Q)
    Datasets for the amount households spend on Durable Goods, Transportation Expenses, and their median Income 
    """
)

Fun_Wonder_Text = dcc.Markdown(
    """> **Cost of Living Wage** is what one full-time worker must earn on an hourly basis to help cover the cost of 
    their family’s minimum basic needs where they live while still being self-sufficient.
      Play with the app and see for yourself!

> Select the number of beds, bathrooms, NYC county you wish in your house and see how the transporation and expense is
affected by housing
  Beneath this one, try selecting different columns to see how Income, expenses change over time
"""
)

About_text = dcc.Markdown(
    """The task for this project was to use the pre-reading I read as an inspiration and apply what I have learned thus 
    far through the readings (SwD, TBoD), labs, and lectures to produce a data dashboard that enables its users to 
    perform exploratory analysis of cost of living and living wage in the region of your choice."""

    
    """This dashboard from this project allows a user who is interested in NewYork City's living wage to explore 
     different scenarios and factors of living wage consideration. This dashboard helps users get an idea of what 
     kind of stories may be worth telling with the available data. Without any doubt, this dashboard is like an 
     intermediary data analysis tool for someone who may be planning on speaking to their local county board of 
     supervisors regarding the county's welfare funding."""
)

footer = html.Div(
    dcc.Markdown(
        """
         This information is intended solely as general information for educational
        and entertainment purposes only and is not a substitute for professional advice and
        services from qualified financial services providers familiar with your financial
        situation.    
        """
    ),
    className="p-2 mt-5 bg-primary text-white small",
)
