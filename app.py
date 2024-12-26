import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State

from layout.input_form import create_input_form,register_callbacks
from layout.graphs import create_graphs , register_callback_graph


# here we initilize our dash app
#suppress_callback_exceptions i will set it to true after finishing code 
#cause it will prevent to show errorrs to user if one happen

app = dash.Dash(__name__ , suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.BOOTSTRAP])


# Layout
app.layout = html.Div(
    children= [
        dcc.Location(id ='url' , refresh=False),
        html.Div(id ='page_content')
    ]
)

@app.callback(
    Output('page_content' , 'children'),
    Input('url' , 'pathname')
)

def display_page(pathname) :
    if pathname == '/filter' :
        return create_input_form()
    if pathname == '/graphs' :
        return create_graphs() 
    else : 
        return create_input_form()
    

register_callbacks(app)
register_callback_graph(app)

# input_form.register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)