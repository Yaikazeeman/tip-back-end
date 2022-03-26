
from email.utils import decode_rfc2231
import json
from urllib.request import urlopen
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask_login.utils import login_required
import plotly.express as px
import pandas as pd
from urllib import response
from datetime import datetime;
from dash_application import overview, solved, raised, SLA, backlog


def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="__name__" , url_base_pathname="/dash/")

    @dash_app.callback(Output('tabs-content-classes', 'children'),Input('tabs', 'value'))
    def render_content(tab):
        if tab == 'tab-1':
            return overview.get_kpi1_data()
        elif tab == 'tab-2':
            return overview.get_kpi1_data()
        elif tab == 'tab-3':
            return solved.render_kpi3(solved.get_kpi3_data()) 
        elif tab == 'tab-4':
            return backlog.render_kpi4(backlog.get_kpi4_data())
        elif tab == 'tab-5':
            return SLA.render_SLA()

    
    dash_app.layout = html.Div( 
        children=[
            html.Div(children=[
                html.Img(src="./assets/logo-iberia.svg"),
                 html.H1("IBERIA Dashboard", className="header-text"),
                html.A(children="Logout", href="/logout" ,className="logout")
            ], className="header"),
            html.Div(children=[
                html.Div(children=[
                    dcc.Tabs(
                        id="tabs", 
                        value='tab-1',
                        parent_className='custom-tabs',
                        className='custom-tabs-container',
                        children=[ 
                            dcc.Tab(
                                label='Overview',
                                value='tab-1',
                                className='custom-tab',
                                selected_className='custom-tab--selected'
                            ),
                            dcc.Tab(  
                                label='INC. Raised',
                                value='tab-2',
                                className='custom-tab',
                                selected_className='custom-tab--selected'
                            ),
                            dcc.Tab(
                                label='INC. Closed',
                                value='tab-3', className='custom-tab',
                                selected_className='custom-tab--selected'
                            ),
                            dcc.Tab(
                                label='INC. Backlog',
                                value='tab-4', className='custom-tab',
                                selected_className='custom-tab--selected'
                            ),
                            dcc.Tab(
                                label='SLA',
                                value='tab-5',
                                className='custom-tab',
                                selected_className='custom-tab--selected'
                            ),
                        ]
                    ),
                ],className="tabs-container"),
                # html.Div(children=[
                #     html.Label('Select Month'),
                #     dcc.Dropdown(['January', 'February', 'March', 'April'], 'January' )
                #     ], className='dropdown'
                # )
            ], className="tabs-outer-container"),

            html.Div(id='tabs-content-classes')
        ], className="dashboard-page"
    )




    for view_function in dash_app.server.view_functions:
        if view_function.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_function] = login_required(
                dash_app.server.view_functions[view_function]
            )

    return dash_app




