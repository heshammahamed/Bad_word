from dash import html, dcc
import dash_bootstrap_components as dbc
from layout.nav_bar import create_nav_bar

# we need 15 graph for each methode 
# each one is beside the other

#elemnts

#html.P()
#dbc.Ratio()
#dbcCheckList()
#dbcButton()

#layout 
#dbc.Row()
#dbc.Col()

def create_graphs() : 
    return html.Div (
        children=[
            create_nav_bar(),
            dbc.Container(
                children = [
                            html.H1("graph page" , style={"textAlign" : "center"})
                        ],
                style={"marginTop" : "20px"}                        
            )
            ],
    )