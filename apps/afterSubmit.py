import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from app import app
from requests import get
from dash import dash_table

#----------------------------------------
def getIpAdress():
    ip = get("https://api.ipify.org").text
    return ip
theIp = getIpAdress()  
#-------------------------------------
layout = html.H4("Welcome to the Tahiri Lab", className="card-title")