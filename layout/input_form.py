from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from layout.nav_bar import create_nav_bar
import base64
import io
import os
import tempfile

import subprocess
 

# elememts 

#html.P()

# dcc.Upload()
#dcc.Slider()

#dbc.Button()
#dbc.Ratio()



#layout comp

#dbc.Row()
#dbc.Col()

def create_input_form() : 
    return html.Div (
        children=[
            create_nav_bar(),
            dbc.Container(
                children = [
                            html.H1("filter page" , style={"textAlign" : "center"})
                        ],
                style={"marginTop" : "20px"}                        
            )
            ],
    )



       
