#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import json
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Define the API endpoint and parameters
url = "https://api.census.gov/data/timeseries/poverty/histpov2"
params = {
    "get": "POV,YEAR,FAM,FAMPOV,FEMHH,FEMHHPOV,PCTFAMPOV,PCTFEMHHPOV,PCTPOV,PCTUNRELPOV,POP,UNREL,UNRELPOV",
    "for": "us:*",
    "key": "829e1ebde12a775d3c9558f3be1968fae49ec2b9"  # Replace with your actual Census API key
}

# Function to get data from the API
def get_census_data(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print("Response content:", response.text)
            raise
    else:
        print("Non-200 status code received")
        print("Response status code:", response.status_code)
        print("Response content:", response.text)
        response.raise_for_status()

# Fetch data from the Census API
data = get_census_data(url, params)

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data[1:], columns=data[0])

# Convert columns to appropriate data types
df["POV"] = pd.to_numeric(df["POV"])
df["YEAR"] = pd.to_numeric(df["YEAR"])
df["FAM"] = pd.to_numeric(df["FAM"])
df["FAMPOV"] = pd.to_numeric(df["FAMPOV"])
df["FEMHH"] = pd.to_numeric(df["FEMHH"])
df["FEMHHPOV"] = pd.to_numeric(df["FEMHHPOV"])
df["PCTFAMPOV"] = pd.to_numeric(df["PCTFAMPOV"])
df["PCTFEMHHPOV"] = pd.to_numeric(df["PCTFEMHHPOV"])
df["PCTPOV"] = pd.to_numeric(df["PCTPOV"])
df["PCTUNRELPOV"] = pd.to_numeric(df["PCTUNRELPOV"])
df["POP"] = pd.to_numeric(df["POP"])
df["UNREL"] = pd.to_numeric(df["UNREL"])
df["UNRELPOV"] = pd.to_numeric(df["UNRELPOV"])

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Census Poverty Data Dashboard"), className="mb-2")
    ]),
    dbc.Row([
        dbc.Col(html.H5("Interactive dashboard using Census API data"), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='poverty-time-series'),
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            html.H4("Data Table"),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': year, 'value': year} for year in df['YEAR'].unique()],
                value=df['YEAR'].max(),
                multi=False,
                clearable=False,
                style={'width': '50%'}
            ),
            html.Div(id='table-container')
        ], width=12),
    ]),
])

# Update the time series graph
@app.callback(
    Output('poverty-time-series', 'figure'),
    Input('year-dropdown', 'value')
)
def update_graph(selected_year):
    filtered_df = df[df['YEAR'] == selected_year]
    fig = px.line(df, x='YEAR', y='POV', title='Poverty Count Over Time')
    return fig

# Update the data table based on the selected year
@app.callback(
    Output('table-container', 'children'),
    Input('year-dropdown', 'value')
)
def update_table(selected_year):
    filtered_df = df[df['YEAR'] == selected_year]
    table = dbc.Table.from_dataframe(filtered_df, striped=True, bordered=True, hover=True)
    return table

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




