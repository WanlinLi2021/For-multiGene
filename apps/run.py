import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from app import app
from requests import get
from dash import dash_table
import os 

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
# get all the newick files produced 
os.chdir('user/' + theIp + '/output/')
tree_path = os.listdir()
tree_files = []
for item in tree_path:
    if item.endswith("_newick"):
        tree_files.append(item)
os.chdir('../../..')
#-------------------------------------
layout = html.H4("This is run page", className="card-title")