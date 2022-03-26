import json
import dash
from urllib.request import urlopen
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px

def sort_by_month(d):
    '''a helper function for sorting'''
    return d['month']

def get_kpi3_data():
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

    return pd.DataFrame({'Months': month_ms, 'Data': data_ms})

def render_kpi3(df):
    return html.Div(
        children=[
            html.Div(
                children=[
                    
                ]
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="example-graph",
                        figure=px.bar(df, x="Months", y="Data", barmode="group"),
                    ),
                ]
            )

        ], className="kpi-container"
    )