import dash_bootstrap_components as dbc

def create_nav_bar () : 
    return dbc.NavbarSimple (
                children=[
                    dbc.NavItem(dbc.NavLink("Filter" ,href="/" ,style={"fontSize": "20px"})),
                    dbc.NavItem(dbc.NavLink("Graphs" ,href= "/graphs",style={"fontSize": "20px"}))
                    ],
                brand="Aho vs Regex",
                brand_href="/",
                color="primary",
                dark=True,
                sticky=True,
                brand_style={"fontSize" : "30px"}
            ) 

