import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
from app import app
import os
import pipeline_user
from requests import get
from apps import beforeSubmit, afterSubmit

#----------------------------------------
def getIpAdress():
    ip = get("https://api.ipify.org").text
    return ip
theIp = getIpAdress()  
#-----------------------------------------
 #create user's file
user_input = 'user/'  + theIp +'/input' 
user_output = 'user/'  + theIp +'/output' 
if not os.path.exists(user_input):
    os.makedirs(user_input)
if not os.path.exists(user_output):
    os.makedirs(user_output)
csv_file = user_input + '/donnees.csv'
seq_file = user_input + '/upload_gene.fasta'
if os.path.exists(csv_file):
  os.remove(csv_file)

if os.path.exists(seq_file):
  os.remove(seq_file)

# create a csv table for gene parameters
genes_csv = 'user/' + theIp + '/input/parameters.csv'
if not os.path.exists(genes_csv):
    with open(genes_csv, 'w') as f:
        f.write("Gene,Bootstrap value threshold,Robinson and Foulds distance threshold,Sliding Window Size,Step Size\n")
#-------------------------------------------
meteo_csv = 'user/' + theIp + '/input/meteo.csv'
if not os.path.exists(meteo_csv):
    pd.DataFrame(list()).to_csv(meteo_csv)
#------------------------
card3 = dbc.Card(
    [
        dbc.CardImg(src="/assets/trees-img.jpg", top=True),
        dbc.CardBody(
            [
                html.H4("Submit & Run iPhyloGeo", className="card-title"),
               
                html.Button(id= "run_button", children="Run"),
            ]
        ),
    ],
    #style={"width": "45%"},
),


#------------------------
layout = dbc.Container([
    # Befor submit
    html.Div(id = "log"),
    html.Br(),
    dbc.Row([
           
            dbc.Col([
                html.Div(card3),
            ],xs=12, sm=12, md=12, lg=5, xl=5),

         ],justify='around'),

], fluid=True)

#---------------------------   
@app.callback(Output('log', 'children'),
              Input('run_button','n_clicks'),
              )

def save_meteoTable(n):
    if n is None:
        return beforeSubmit.layout
    else:
        return afterSubmit.layout