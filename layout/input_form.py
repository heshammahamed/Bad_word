from dash import html, dcc, Input, Output, State
import dash
import dash_bootstrap_components as dbc
from layout.nav_bar import create_nav_bar
import base64
import io
import os
import shutil
import tempfile


import subprocess
 
def create_input_form() : 
    return html.Div (
        children=[
            create_nav_bar(),

            dbc.Container(
            dbc.Row(
                children=[
                     dbc.Col(
                          dbc.Row(
                               children=[
                                    dbc.Col(html.P("Big File",className="fs-1"),width='auto'),
                                    dbc.Col(dbc.Container(dcc.Upload(id="big_file" , children=dbc.Button("select", color="primary",style={"width" : "100%"}, className=["py-0","fs-2"])),fluid=True),width="5"),
                               ],align="center",justify='between'
                          ),width='5'
                     ),
                     dbc.Col(
                          dbc.Row(
                               children=[
                                    dbc.Col(html.P("Bad File",className="fs-1"),width='auto'),
                                    dbc.Col(dbc.Container(dcc.Upload(id="bad_test" , children=dbc.Button("select", color="primary",style={"width" : "100%"}, className=["py-0","fs-2"])),fluid=True),width="5"),
                               ],align="center",justify='between'
                          ),width='5'
                     ),
                ],align="center",justify='between'
            ),
            className='mt-5',
            ),
            dbc.Container(
            dbc.Row(
                children=[
                    dbc.Col(html.P("Chunk Size",className="fs-1"),width='auto'),
                    dbc.Col(dcc.Slider(id="slider", min=10000, max=150000, step=10000, value=5),width='10')
                ],align="center",justify='between'
            ),
            className='mt-5',
            ),
            dbc.Container(
                dbc.Row(
                    children=[
                         dbc.Col(html.P("Filter Mode",className="fs-1"),width='4'),
                         dbc.Col(
                            dbc.RadioItems(id="filter_mode",
                                options=[
                                            {"label": "AhoCorasick", "value": "AhoCorasick"},
                                            {"label": "Regex", "value": "Regex"},
                                ],inline=True,label_style={"fontSize" : "30px" ,"marginRight" : "90px"},input_style={"marginTop": "15px"}
                            ),width='8'
                         )
                    ],align="center"
                ),
                className='mt-5',
            ),
            dbc.Container(
                dbc.Row(
                    children=[
                         dbc.Col(html.P("process mode",className="fs-1"),width='4'),
                         dbc.Col(
                            dbc.RadioItems(id="process_mode",
                                options=[
                                            {"label": "Hybird", "value": "Hybird"},
                                            {"label": "MultiProcessing", "value": "MultiProcessing"},
                                            {"label": "ProcessesPool", "value": "ProcessesPool"},
                                            {"label": "MultiThreading", "value": "MultiThreading"},
                                ],inline=True,label_style={"fontSize" : "25px","marginRight" : "10px"},input_style={"marginTop": "15px"}
                            ),width='8'
                         )
                    ],align="center"
                ),
                className='mt-5',
            ),
            dbc.Container(
                dbc.Button(id="run", children="Run", color="primary", style={"width": "150px"}, className=["py-0", "fs-2"]),
                style={"margin" : "50px auto" , "width" : "14%"}
            ),

            dbc.Modal(
                [
                    dbc.ModalHeader("Process Status"),
                    dbc.ModalBody(id="modal-body", children="The process is running..."),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close-modal", className="ms-auto", n_clicks=0)
                    ),
                ],
                id="process-modal",
                is_open=False,
            ),

        ]
    )


def save_files(big_file , bad_file) : 
    big_content_type, big_content_string = big_file.split(',')
    bad_content_type, bad_content_string = bad_file.split(',')
    big_decoded = base64.b64decode(big_content_string)
    bad_decoded = base64.b64decode(bad_content_string)
    temp_dir = tempfile.mkdtemp()  
    big_file_path = os.path.join(temp_dir,"test.rar") 
    bad_file_path = os.path.join(temp_dir,"bad_file.csv")  

    with open(big_file_path, "wb") as f:
        f.write(big_decoded)

    with open(bad_file_path, "wb") as f:
        f.write(bad_decoded)

    return [temp_dir,big_file_path , bad_file_path]

def register_callbacks(app):
    @app.callback(
        Output("process-modal", "is_open"),
        Output("modal-body", "children",allow_duplicate=True),
        [Input("run", "n_clicks"), Input("close-modal", "n_clicks")],
        [State("process-modal", "is_open")],
        prevent_initial_call=True,
    )
    def toggle_modal(run_clicks, close_clicks, is_open):
        ctx = dash.callback_context
        if not ctx.triggered:
            return is_open, ""
        if ctx.triggered[0]["prop_id"] == "run.n_clicks":
            return True, "The subprocess is running..."
        if ctx.triggered[0]["prop_id"] == "close-modal.n_clicks":
            return False, ""

    @app.callback(
        Output("modal-body", "children"),
        Input("run", "n_clicks"),
        State("big_file", "contents"),
        State("bad_test", "contents"),
        State("slider", "value"),
        State("filter_mode", "value"),
        State("process_mode", "value"),
        prevent_initial_call=True,
    )
    def run_backend(run_clicks, big_file, bad_file, slider, filter_mode, process_mode):
        venv_bath = r"E:\T1_com301_fall2024\venv\Scripts\activate.bat"
        files = save_files(big_file, bad_file)
        backend_code_dir = os.path.join(os.getcwd(), "code")
        command = [
            venv_bath,
            "&&",
            "python",
            "./main.py",
            "-d",
            files[1],
            "-b",
            files[2],
            "-s",
            str(slider),
            "-f",
            str(filter_mode),
            "-p",
            str(process_mode),
            "-c",
            "1,2,3",
        ]

        try:
            subprocess.run(command, cwd=backend_code_dir, check=True)
            shutil.rmtree(files[0])
            return "Subprocess finished successfully!"
        except subprocess.CalledProcessError:
            return "Subprocess failed!"

