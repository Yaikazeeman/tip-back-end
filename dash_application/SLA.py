import json
import dash
from urllib.request import urlopen
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
from datetime import datetime;

def render_SLA():
        
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

    return  html.Div(children=[
            html.Div(children=[
                html.Div(
                    children=[
                        html.Div(children=[
                            html.P(children="Number of P1 not meeting SLA"),
                            html.H3(children=len(not_meeting_sla))
                        ]),
                        html.Div(children=[
                            html.P(children="Percentage of P1 not meeting SLA"),
                            html.H3(children=str(percentage_not_SLA) + "%")
                        ]),
                        html.Div(children=[
                            html.P(children="Total of P1 incidence"),
                            html.H3(children=len(INC_ID_arr))
                        ]),
                        html.Div(children=[
                            html.P(children="Total of P1 incidence"),
                            html.H3(children=len(INC_ID_arr))
                        ]),
                        html.Div(children=[
                            html.P(children="average time in minutes not meeting SLA"),
                            html.H3(children=average_time_not_meeting),
                        ]),
                        html.Div(children=[
                            html.P(children="average time in minutes meeting SLA"),
                            html.H3(children=average_time_meeting)
                        ])
                    ], className="sla_container"
                ),
                dcc.Graph(
                    id="sla-graph",
                    figure=px.bar(df_sla, x="INC", y="Minutes", barmode="group"),
                
                )
            ], className="sla-page")
        ])