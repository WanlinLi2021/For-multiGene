import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from app import app
from requests import get
import os 
from dash import dash_table

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
#---------------------------

geneTable = dbc.Container([
     # table of parameters
    dbc.Row([
            dbc.Col([
                html.Br(),
                #html.Hr(),
                html.Div([
                        dash_table.DataTable(
                            id='gene-table',
                            columns=[
                                {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": False}
                                for i in pd.read_csv('user/' + theIp + '/input/parameters.csv').columns ],
                            data=pd.read_csv('user/' + theIp + '/input/parameters.csv').to_dict('records'),  # the contents of the table
                            editable=True,              # allow editing of data inside all cells
                            filter_action="none",     # allow filtering of data by user ('native') or not ('none')
                            sort_action="none",       # enables data to be sorted per-column by user or not ('none')
                            #sort_mode="single",         # sort across 'multi' or 'single' columns
                            #column_selectable="multi",  # allow users to select 'multi' or 'single' columns
                            row_selectable="multi",     # allow users to select 'multi' or 'single' rows
                            row_deletable=True,         # choose if user can delete a row (True) or not (False)
                            selected_columns=[],        # ids of columns that user selects
                            selected_rows=[],           # indices of rows that user selects
                            page_action="native",       # all data is passed to the table up-front or not ('none')
                            page_current=0,             # page number that user is on
                            page_size=10,                # number of rows visible per page
                            style_cell={                # ensure adequate header width when text is shorter than cell's text
                                'minWidth': 95, 'maxWidth': 95, 'width': 95
                            },
                            style_cell_conditional = [ #align text column to left
                                {
                                    'if':{'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['Gene']
                            ],
                            style_data={                # overflow cells' content into multiple lines
                                'whiteSpace': 'normal',
                                'height': 'auto'
                            },
                            style_header={
                                'whiteSpace': 'normal',
                                'height': 'auto'
                            }
                        ),

                        #html.Br(),
                    ]),

            ],xs=12, sm=12, md=12, lg=10, xl=10),

         ],justify='around'),

], fluid=True)

#-----------------------------------------
card1 = dbc.Card(
    [
        dbc.CardImg(src="/assets/climate.jpg", top=True),
        dbc.CardBody(
            [
                html.H4("Add meteorological data", className="card-title"),
                dbc.CardLink("Add dataset", href="addMeteo"),
            ]
        ),
    ],
    #style={"width": "45%"},
),

card2 = dbc.Card(
    [
        dbc.CardImg(src="/assets/dna.jpg", top=True),
        dbc.CardBody(
            [
                html.H4("Add genetic data", className="card-title"),
               
                dbc.CardLink("Add dataset", href="addGene"),
            ]
        ),
    ],
    #style={"width": "45%"},
),
#--------------------------------------------------------
layout = dbc.Container([
    # For Genes parameters
    html.Br(),
    #html.Br(),
    dbc.CardHeader(
            dbc.Button(
                "Genes and parameters to be analyzed",
                color="link",
                id="button-geneTable",
            )
        ),
    dbc.Collapse(
            html.Div(geneTable),
                            
            id = 'forGeneTable', is_open=False,   # the Id of Collapse
                            ),

     # For Meteo parameters
     html.Br(),
     #html.Br(),
    dbc.CardHeader(
            dbc.Button(
                "Meteorological dataset and parameters to be analyzed",
                color="link",
                id="button-meteoTable",
            )
        ),
    dbc.Collapse(
            html.Div(geneTable),
                            
            id = 'forMeteoTable', is_open=False,   # the Id of Collapse
                            ),

    # For Meteo parameters
     html.Br(),
     #html.Br(),
    dbc.CardHeader(
            dbc.Button(
                "Receive analysis results by email",
                color="link",
                id="button-email",
            )
        ),
    dbc.Collapse(
        dbc.Row([
        html.Br(),
        dbc.Col([
            html.H5("Please enter the email address used to receive the analysis results"),
            html.Br()   
        ],# width={'size':3, 'offset':1, 'order':1},
           xs=8, sm=8, md=8, lg=7, xl=7
        ),
       
        dbc.Col([
            html.Br(),
            #html.Br(),
            dcc.Input(id="input_email", type="text", placeholder="Email addeess",debounce=True,),
            html.Br()
        ],# width={'size':3, 'offset':1, 'order':1},
           xs=4, sm=4, md=4, lg=5, xl=5
        ),
    ], justify='around'),  # Horizontal:start,center,end,between,around
                            
            id = 'forEmail', is_open=False,   # the Id of Collapse
                            ),
    #comfirm button ----- gene
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Button(id= "confirm_button", children="Confirm genetic parameters"),
            html.Br(),
            #html.Hr(),
        ],# width={'size':3, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=4, xl=4),
        dbc.Col([
            html.Br(),
            html.Div(id="confirmed"),
            html.Br(),
            #html.Hr(),
        ],# width={'size':3, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=5, xl=5),
        
    ], justify='around'),

    #comfirm button ----- meteo
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Button(id= "confirm_meteo_button", children="Confirm meteorological parameters"),
            html.Br(),
            #html.Hr(),
        ],# width={'size':3, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=4, xl=4),
        dbc.Col([
            html.Br(),
            html.Div(id="confirmed_meteo"),
            html.Br(),
            #html.Hr(),
        ],# width={'size':3, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=5, xl=5),
        
    ], justify='around'),

    html.Br(),
    html.Br(),
    dbc.Row([
            dbc.Col([
                html.Div(card1),
            ],xs=12, sm=12, md=12, lg=5, xl=5),
            dbc.Col([
                html.Div(card2),
            ],xs=12, sm=12, md=12, lg=5, xl=5),
            
         ],justify='around'),
], fluid=True)

    

#----------------------------------------
@app.callback(Output('confirmed', 'children'),
              Input('confirm_button','n_clicks'),
              Input('gene-table', "derived_virtual_data"),
              Input('gene-table', 'derived_virtual_selected_rows'),
              Input('gene-table', 'derived_virtual_selected_row_ids'),
          )

def save_genesTable(n, all_rows_data,slctd_row_indices, slct_rows_names):
    print('***************************************************************************')
    print('Data across all pages pre or post filtering: {}'.format(all_rows_data))
    print('---------------------------------------------')
    print("Indices of selected rows if part of table after filtering:{}".format(slctd_row_indices))
    print("Names of selected rows if part of table after filtering: {}".format(slct_rows_names))
    print('*****************------------------------********************************')
    
    if n is None:
        dff = pd.DataFrame(all_rows_data)
    else:
        dff = pd.DataFrame(all_rows_data)
        colors = ['#7FDBFF' if i in slctd_row_indices else '#0074D9'
              for i in range(len(dff))]
        dff.to_csv('user/' + theIp + '/input/genes_confirmed.csv',index=False)
        print(dff)
        return dcc.Markdown('The genetic parameters have been confirmed',className="card-text"),

@app.callback(Output('confirmed_meteo', 'children'),
              Input('confirm_meteo_button','n_clicks'),
              State('gene-table', "derived_virtual_data"),)

def save_meteoTable(n, all_rows_data):
    dff = pd.DataFrame(all_rows_data)
    if n is None:
        return dash.no_update
    else:
        dff.to_csv('user/' + theIp + '/input/meteo_confirmed.csv',index=False)
        print(dff)
        return dcc.Markdown('The meteorological parameters have been confirmed',className="card-text"),
#-------------------------------------
@app.callback(
    Output("forGeneTable", "is_open"),
    [Input("button-geneTable", "n_clicks")],
    [State("forGeneTable", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("forMeteoTable", "is_open"),
    [Input("button-meteoTable", "n_clicks")],
    [State("forMeteoTable", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("forEmail", "is_open"),
    [Input("button-email", "n_clicks")],
    [State("forEmail", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open