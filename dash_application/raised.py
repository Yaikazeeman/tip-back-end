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

def get_raised_data():
    pass

def render_raised(df):
    pass