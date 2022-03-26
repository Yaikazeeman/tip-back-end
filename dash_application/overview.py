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

def get_kpi1_data():
    url = "https://ge81ee28f924217-db202201141801.adb.eu-amsterdam-1.oraclecloudapps.com/ords/tip/kpi1/incvol/"
    response = urlopen(url)
    monthly_raised = json.loads(response.read())['items']
    monthly_raised_sorted = sorted(monthly_raised, key=sort_by_month)

    months = []
    data = []
    priority = []
    for element in monthly_raised_sorted:
        if element['month'] == '202101':
            months.append('January')
            data.append(element['incidences_number'])
            priority.append(element['priority'])
        elif element['month'] == '202102':
            months.append('February')
            data.append(element['incidences_number'])
            priority.append(element['priority'])
        elif element['month'] == '202103':
            months.append('March')
            data.append(element['incidences_number'])
            priority.append(element['priority'])
        elif element['month'] == '202104':
            months.append('April')
            data.append(element['incidences_number'])
            priority.append(element['priority'])

    df = pd.DataFrame({'Months': months, 'Data': data, 'Color': priority})

    return html.Div(
        children=[
            dcc.Graph(
                id="example-graph",
                figure=px.bar(df, x="Months", y="Data", color="Color",  barmode="group"),
            
            ),
        ]
    )