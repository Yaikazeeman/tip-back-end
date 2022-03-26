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

def get_kpi4_data():
    url_3 = "https://ge81ee28f924217-db202201141801.adb.eu-amsterdam-1.oraclecloudapps.com/ords/tip/kpi3/inccrit/"
    response = urlopen(url_3)
    monthly_raised_3 = json.loads(response.read())['items']
    monthly_raised_sorted_3 = sorted(monthly_raised_3, key=sort_by_month)

    months_3 = []
    data_3 = []
    priority_3 = []
    for element in monthly_raised_sorted_3:
        if element['month'] == '2021-01':
            months_3.append('January')
            data_3.append(element['incidenct_code'])
            priority_3.append(element['priority'])
        elif element['month'] == '2021-02':
            months_3.append('February')
            data_3.append(element['incidenct_code'])
            priority_3.append(element['priority'])
        elif element['month'] == '2021-03':
            months_3.append('March')
            data_3.append(element['incidenct_code'])
            priority_3.append(element['priority'])
        elif element['month'] == '2021-04':
            months_3.append('April')
            data_3.append(element['incidenct_code'])
            priority_3.append(element['priority'])

    return pd.DataFrame({'Months': months_3, 'Data': data_3, 'Priority': priority_3})

def render_kpi4(df):
    return html.Div(
        children=[
            html.H2(children="Total Inc. in backlog per priority"),
            dcc.Graph(
                id="backlog-graph",
                figure=px.bar(df, x="Months", y="Data", color="Priority",  barmode="group"),
            
            ),
        ], className="backlog-page"
    )