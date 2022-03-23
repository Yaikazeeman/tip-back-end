
from email.utils import decode_rfc2231
import json
from urllib.request import urlopen
import dash
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask_login.utils import login_required
import plotly.express as px
import pandas as pd
from urllib import response
from datetime import datetime


def sort_by_month(d):
    '''a helper function for sorting'''
    return d['month']


url = "https://ge81ee28f924217-db202201141801.adb.eu-amsterdam-1.oraclecloudapps.com/ords/tip/kpi1/incvol/"
response = urlopen(url)
monthly_raised = json.loads(response.read())['items']
monthly_raised_sorted = sorted(monthly_raised, key=sort_by_month)

months = []
data = []
for element in monthly_raised_sorted:
    if element['month'] == '202101':
        months.append('Januari')
        data.append(element['incidences_number'])
    elif element['month'] == '202102':
        months.append('February')
        data.append(element['incidences_number'])
    elif element['month'] == '202103':
        months.append('March')
        data.append(element['incidences_number'])
    elif element['month'] == '202104':
        months.append('April')
        data.append(element['incidences_number'])

df = pd.DataFrame({'Months': months, 'Data': data})
#####################################

url_ms = "https://ge81ee28f924217-db202201141801.adb.eu-amsterdam-1.oraclecloudapps.com/ords/tip/kpi2/incsolved/"
response = urlopen(url_ms)
monthly_solved = json.loads(response.read())['items']
monthly_solved_sorted = sorted(monthly_solved, key=sort_by_month)


month_ms = []
data_ms = []
for element in monthly_solved_sorted:
    if element['month'] == '202101':
        month_ms.append('Januari')
        data_ms.append(element['incidences_code'])
    elif element['month'] == '202102':
        month_ms.append('February')
        data_ms.append(element['incidences_code'])
    elif element['month'] == '202103':
        month_ms.append('March')
        data_ms.append(element['incidences_code'])
    elif element['month'] == '202104':
        month_ms.append('April')
        data_ms.append(element['incidences_code'])

df_ms = pd.DataFrame({'Months': month_ms, 'Data': data_ms})

#############################

url_sla = "https://ge81ee28f924217-db202201141801.adb.eu-amsterdam-1.oraclecloudapps.com/ords/tip/kpi5/inc-closed/"
response = urlopen(url_sla)
monthly_sla = json.loads(response.read())['items']

solution_time_arr = []
INC_ID_arr = []
for ele in monthly_sla:
    creation_time = datetime.strptime(ele['created_date_time'], "%Y-%m-%d %H:%M:%S") 
    resolution_time = datetime.strptime(ele['resolution_date_time'], "%Y-%m-%d %H:%M:%S")
    duration = resolution_time - creation_time
    duration_in_m = int(duration.total_seconds() / 60)
    solution_time_arr.append(duration_in_m)
    INC_ID_arr.append(ele["incident_code"])
print(solution_time_arr)

not_meeting_sla = []
not_meeting_sla_id = []
meeting_sla = []
meeting_sla_id = []
for i in range(len(solution_time_arr)):
    if solution_time_arr[i] > 240:
        not_meeting_sla.append(solution_time_arr[i])
        not_meeting_sla_id.append(INC_ID_arr[i])
    else:
        meeting_sla.append(solution_time_arr[i])
        meeting_sla_id.append(INC_ID_arr[i])

average_time_not_meeting = round(sum(not_meeting_sla)/len(not_meeting_sla))
percentage_not_SLA = round((len(not_meeting_sla)/ len(solution_time_arr))*100, 1)

average_time_meeting = round(sum(meeting_sla)/len(meeting_sla))

df_sla = pd.DataFrame({'INC': not_meeting_sla_id, 'Minutes': not_meeting_sla})
#############################


def render_kpi1():
    return html.Div(
        children=[
            html.H1(children="KPI 1"),
            html.Div(
                children="""
            INC raised by month
        """
            ),
            dcc.Graph(
                id="example-graph",
                figure=px.bar(df, x="Months", y="Data", barmode="group"),
            
            ),
        ]
    )

def render_kpi2():
    return html.Div(
        children=[
            html.H1(children="KPI 2"),
            html.Div(
                children="""
            INC closed by month
        """
            ),
            dcc.Graph(
                id="example-graph",
                figure=px.bar(df_ms, x="Months", y="Data", barmode="group"),
            
            ),
        ]
    )

def render_kpi5():
    return  html.Div(children=[html.H1(children="KPI 5"),
            html.Div(
                children="""
            Not meeting SLA
        """
            ),
            dcc.Graph(
                id="example-graph",
                figure=px.bar(df_sla, x="INC", y="Minutes", barmode="group"),
            
            ),
            html.Div(
                children=[
                    html.P(children="Number of P1 not meeting SLA"),
                    html.H3(children=len(not_meeting_sla)),
                    html.P(children="Percentage of P1 not meeting SLA"),
                    html.H3(children=str(percentage_not_SLA) + "%"),
                    html.P(children="Total of P1 incidence"),
                    html.H3(children=len(INC_ID_arr)),
                    html.P(children="average time in minutes not meeting SLA"),
                    html.H3(children=average_time_not_meeting),
                    html.P(children="average time in minutes meeting SLA"),
                    html.H3(children=average_time_meeting)
                ]
            )])

def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="__name__" , url_base_pathname="/dash/")

    @dash_app.callback(Output('tabs-content-classes', 'children'),Input('tabs', 'value'))
    def render_content(tab):
        if tab == 'tab-1':
            return render_kpi1()
        elif tab == 'tab-2':
            return render_kpi2()
        elif tab == 'tab-3':
            return "no kpi3 yet"
        elif tab == 'tab-4':
            return render_kpi5()

    
    dash_app.layout = html.Div( 
        children=[
            html.Div(children=[
                html.H1("IBERIA Dashboard", style={'textAlign': 'center', 'color': 'white'})
            ], style={'margin': 0 , "padding": "1%" , 'background-color': "#D7192D" }),
            html.Div(children=[
                html.Div(children=[
                    dcc.Tabs(
                        id="tabs",
                        value='tab-1',
                        parent_className='custom-tabs',
                        className='custom-tabs-container',
                        children=[
                            dcc.Tab(
                                label='KPI 1',
                                value='tab-1',
                                className='custom-tab',
                                selected_className='custom-tab--selected'
                            ),
                            dcc.Tab(  
                                label='KPI 2',
                                value='tab-2',
                                className='custom-tab',
                                selected_className='custom-tab--selected'
                            ),
                            dcc.Tab(
                                label='KPI 3',
                                value='tab-3', className='custom-tab',
                                selected_className='custom-tab--selected'
                            ),
                            dcc.Tab(
                                label='KPI 4',
                                value='tab-4',
                                className='custom-tab',
                                selected_className='custom-tab--selected'
                            ),
                        ]
                    ),
                ], style={'width': '70%'}),
                html.Div(children=[
                    html.Label('Select Month'),
                    dcc.Dropdown(['January', 'February', 'March', 'April'], 'January' )
                    ], style={'width': '20%'}
                )
            ], style={'display': 'flex', 'justify-content': 'space-between'}),

            html.Div(id='tabs-content-classes')
        ], style={"margin": 0}
    )




    for view_function in dash_app.server.view_functions:
        if view_function.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_function] = login_required(
                dash_app.server.view_functions[view_function]
            )

    return dash_app




