from dash import Dash, dcc, html, Input, Output, callback
import os

import pandas as pd
import plotly.express as px

app = Dash(__name__, suppress_callback_exceptions=True)

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# load the dataset
wildlife = pd.read_csv('CleanData.csv')

index_page = html.Div([
    dcc.Link('Go to Imports Bar Graph', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Exports Bar Graph', href='/page-2'),
    html.Br(),
    dcc.Link('Go to Purpose Pie Chart', href='/page-3'),
    html.Br(),
    dcc.Link('Go to Appendix Scatter Plot', href='/page-4'),
])
page_1_layout = html.Div(children=[
    html.H1(children='Wildlife Import Dashboard'),
    dcc.Dropdown(id='Imp-dropdown',
                 options=[{'label': i, 'value': i}
                          for i in wildlife['Importer'].unique()],
                 value='US'),
    dcc.Graph(id='import-graph'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

# set up the callback function
@callback(
    Output(component_id='import-graph', component_property='figure'),
    Input(component_id='Imp-dropdown', component_property='value')
)
def page_1_dropdown(selected_geography):
    filtered_wildlife = wildlife[wildlife['Importer'] == selected_geography]
    bar_fig = px.bar(filtered_wildlife,
                     x='Term', y='imported in kgs',
                     color='App.', title=f'Wildlife Imports in {selected_geography}')
    return bar_fig


page_2_layout = html.Div(children=[
    html.H1(children='Wildlife Export Dashboard'),
    dcc.Dropdown(id='Exp-dropdown',
                 options=[{'label': i, 'value': i}
                          for i in wildlife['Exporter'].unique()],
                 value='US'),
    dcc.Graph(id='export-graph'),
    html.Br(),
    dcc.Link('Go back to home', href='/')

])


# set up the callback function
@callback(
    Output(component_id='export-graph', component_property='figure'),
    Input(component_id='Exp-dropdown', component_property='value')
)
def page_2_dropdown(selected_geography):
    filtered_wildlife = wildlife[wildlife['Exporter'] == selected_geography]
    bar_fig = px.bar(filtered_wildlife,
                     x='Term', y='Exported in kgs',
                     color='App.', title=f'Wildlife Exports in {selected_geography}')
    return bar_fig


page_3_layout = html.Div(children=[
    html.H1(children='Trading Purpose and Total Quantity'),
    dcc.Dropdown(id='App-dropdown_3',
                 options=[{'label': i, 'value': i}
                          for i in wildlife['App.'].unique()],
                 value='I'),
    dcc.Graph(id='app-graph_3'),
    html.Br(),
    dcc.Link('Go back to home', href='/')

])


# set up the callback function
@callback(
    Output(component_id='app-graph_3', component_property='figure'),
    Input(component_id='App-dropdown_3', component_property='value')
)
def page_3_dropdown(selected_geography):
    filtered_wildlife = wildlife[wildlife['App.'] == selected_geography]
    pie_fig = px.pie(filtered_wildlife,
                     values='Total Quantity', names='Purpose',
                     title=f'Trading Purpose and Total Quantity of Appendix {selected_geography} Species')
    return pie_fig


page_4_layout = html.Div(children=[
    html.H1(children='Imports and Exports based on Appendix'),
    dcc.Dropdown(id='App-dropdown_4',
                 options=[{'label': i, 'value': i}
                          for i in wildlife['App.'].unique()],
                 value='I'),
    dcc.Graph(id='app-graph_4'),
    html.Br(),
    dcc.Link('Go back to home', href='/')

])


# set up the callback function
@callback(
    Output(component_id='app-graph_4', component_property='figure'),
    Input(component_id='App-dropdown_4', component_property='value')
)
def page_4_dropdown(selected_geography):
    filtered_wildlife = wildlife[wildlife['App.'] == selected_geography]
    scatter_fig = px.scatter(filtered_wildlife,
                     x='imported in kgs', y='Exported in kgs',
                     title=f'Wildlife Imports and Exports in {selected_geography}')
    return scatter_fig


# Update the index
@callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
        return page_4_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

if __name__ == '__main__':
    app.run_server(debug=True)