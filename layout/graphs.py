from dash import html, dcc
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output , State
import pandas as pd
import plotly.express as px
from layout.nav_bar import create_nav_bar

# we need 15 graph for each methode 
# each one is beside the other

file_path ='./code/output/StatisticalSummary_CS342Spring2024.xlsx'

aho_df = pd.read_excel(file_path, sheet_name="AhoCorasick")
regular_df = pd.read_excel(file_path, sheet_name="Regex")

def create_graphs() : 
    return html.Div (
        children=[
            create_nav_bar(),

            dbc.Container(children=[
                html.Label("Select Data Source:",style={"fontSize" : "20px" , "marginTop" : "30px" , "marginBottom" : "10px"}),
                dcc.Dropdown(
                    id='sheet-choice',
                    options=[
                        {'label': 'AhoCorasick', 'value': 'AhoCorasick'},
                        {'label': 'Regex', 'value': 'Regex'},
                        {'label': 'Aho vs Regular', 'value': 'compare'}
                    ],
                    value='aho'  # Default value
                ),]
            ),
            # Dropdown to select column for Y-axis
            dbc.Container(
                children=[
                    html.Label("Select Y-axis Column:",style={"fontSize" : "20px" , "marginTop" : "30px" , "marginBottom" : "10px"}),
                    dcc.Dropdown(
                        id='y-axis-column',
                        options=[{'label' : col , 'value' : col} for col in aho_df.columns],
                        value=aho_df.columns[1]
                    ),
                ]
            ),

            dbc.Container(
                dbc.Button(id="make_graph" , children="Create Graph" , style={"fontSize" : "25px" , "marginTop" : "20px"}),style={"width" : "100%" , "display" : "flex" , "justifyContent" : "center"}
            ),

            # Graph to display the column chart
            dcc.Graph(id='column-chart' , style={"height" : "500px"}),
    ],
        style={}
    )

def register_callback_graph (app) :
    @app.callback (
        Output("column-chart" , "figure"),
        Input("make_graph" , "n_clicks"),
        State("sheet-choice" , "value"),
        State("y-axis-column" , "value"),

        prevent_initial_call=True
    )

    def update_chart(n_clicks,sheet_choice, y_col):
        if sheet_choice == 'AhoCorasick':
            fig = px.bar(aho_df, x='D.frame size', y=y_col, title=f"AhoCorasick Data ({y_col}for each chunk size)")
        elif sheet_choice == 'Regex':
            fig = px.bar(regular_df, x='D.frame size', y=y_col, title=f"Regex Data ({y_col}for each chunk size)")
        
        else: 
            compare_df = pd.DataFrame({
                'chunck': aho_df['D.frame size'],
                'AhoCorasick': aho_df[y_col],
                'Regex': regular_df[y_col]
            }).melt(id_vars='chunck', var_name='Source', value_name=y_col)

            fig = px.line(
                compare_df, 
                x='chunck', 
                y=y_col, 
                color='Source',  # Lines will be grouped and colored by 'Source'
                markers=True,    # Adds markers to the line graph for better visibility
                title=f"Comparison: Aho vs Regular ({y_col})"
            )

            fig.update_layout(
                xaxis_title="Chunk",
                yaxis_title=y_col,
                title_x=0.5  # Centers the title
            )
            # compare_df = pd.DataFrame({
            #     'chunck': aho_df['D.frame size'],
            #     'AhoCorasick': aho_df[y_col],
            #     'Regex': regular_df[y_col]
            # }).melt(id_vars='chunck', var_name='Source', value_name=y_col)

            # fig = px.bar(
            #     compare_df, 
            #     x='chunck', 
            #     y=y_col, 
            #     color='Source', 
            #     barmode='group',  # Grouped bars for comparison
            #     title=f"Comparison: Aho vs Regular ({y_col})"
            # )

        return fig