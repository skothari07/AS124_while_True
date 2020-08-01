#Importing libraries
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_bootstrap_components as dbc
from datetime import datetime as dt
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import plotly.express as px
import mysql.connector
import pandas as pd
import dash_table
import copy
import pathlib
import sys
import os
import json



####################### Database Credentials ########################################
ENDPOINT="sih2020.cfafpwsc4oxl.us-east-2.rds.amazonaws.com"
PORT="3306"
USR="admin"
REGION="us-east-2"
DBNAME="mysql"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

#####################################################################################

####################### Database connection #########################################
try:
    conn =  mysql.connector.connect(host=ENDPOINT, user=USR, passwd='sih2020agnels', port=PORT, database=DBNAME)
    c = conn.cursor()
    c.execute('SELECT * FROM sih2020.beneficiary_beneficiary_register')
    query_results = c.fetchall()
    #print(query_results)
except Exception as e:
    print("Database connection failed due to {}".format(e))
    
####################################################################################
'''
#get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()'''
#dataframe
df = pd.read_csv('sample_data.csv')
ap = pd.read_csv('small_dataset.csv')

######################### Start Dash ################################################
app = dash.Dash(
    __name__
    , meta_tags=[{"name": "viewport", "content": "width=device-width"}]
    #,assets_folder = str(PATH.joinpath("assets").resolve())
    ,external_stylesheets=[dbc.themes.BOOTSTRAP])
######################################################################################

############################# Layout of the Dashboard ################################

app.title = 'Poshan Analytics'
app.layout = html.Div(children=[
		html.Div(children = [ 
		dbc.NavbarSimple(
		    children=[
			dbc.NavItem(dbc.NavLink("Web Portal", href="#")),
		    ],
		    brand="Poshan Abhiyaan Dashboard",
		    brand_href="http://poshanabhiyaan.gov.in/#/",
		    color="#1c9eff",
		    dark=True,)],style={'width': '100%'}
		    ),
	    	html.Div( children = [
	    	html.Label('Select State / Union Territory:'),
	    	dcc.Dropdown(id = 'dropdown-state',
		    options=[
			{'label': 'Andhra Pradesh', 'value': 'Andhra Pradesh'},
			{'label': 'Arunachal Pradesh', 'value': 'Arunachal Pradesh'},
			{'label': 'Assam', 'value': 'Assam'},
			{'label': 'Bihar', 'value': 'Bihar'},
			{'label': 'Chhattisgarh', 'value': 'Chhattisgarh'},
			{'label': 'Goa', 'value': 'Goa'},
			{'label': 'Gujarat', 'value': 'Gujarat'},
			{'label': 'Haryana', 'value': 'Haryana'},
			{'label': 'Himachal Pradesh', 'value': 'Himachal Pradesh'},
			{'label': 'Jharkhand', 'value': 'Jharkhand'},
			{'label': 'Karnataka', 'value': 'Karnataka'},
			{'label': 'Kerala', 'value': 'Kerala'},
			{'label': 'Madhya Pradesh', 'value': 'Madhya Pradesh'},
			{'label': 'Maharashtra', 'value': 'Maharashtra'},
			{'label': 'Manipur', 'value': 'Manipur'},
			{'label': 'Meghalaya', 'value': 'Meghalaya'},
			{'label': 'Mizoram', 'value': 'Mizoram'},
			{'label': 'Nagaland', 'value': 'Nagaland'},
			{'label': 'Odisha', 'value': 'Odisha'},
			{'label': 'Punjab', 'value': 'Punjab'},
			{'label': 'Rajasthan', 'value': 'Rajasthan'},
			{'label': 'Sikkim', 'value': 'Sikkim'},
			{'label': 'Tamil Nadu', 'value': 'Tamil Nadu'},
			{'label': 'Telangana', 'value': 'Telangana'},
			{'label': 'Tripura', 'value': 'Tripura'},
			{'label': 'Uttar Pradesh', 'value': 'Uttar Pradesh'},
			{'label': 'Uttarakhand', 'value': 'Uttarakhand'},
			{'label': 'West Bengal', 'value': 'West Bengal'},
			{'label': 'Andaman and Nicobar Islands', 'value': 'Andaman and Nicobar Islands'},
			{'label': 'Chandigarh', 'value': 'Chandigarh'},
			{'label': 'Dadra and Nagar Haveli and Daman and Diu', 'value': 'Dadra and Nagar Haveli and Daman and Diu'},
			{'label': 'Delhi', 'value': 'Delhi'},
			{'label': 'Jammu and Kashmir', 'value': 'Jammu and Kashmir'},
			{'label': 'Ladakh', 'value': 'Ladakh'},
			{'label': 'Lakshadweep', 'value': 'Lakshadweep'},
			{'label': 'Puducherry', 'value': 'Puducherry'},			
		    ],
		    multi=False,
		    value=""
		)],style={'width': '30%','margin': '2% 5px 0px 3%'}
		),
	    	html.Div( children = [
	    	html.Label('Select Type:'),
	    	dcc.Dropdown(id = 'dropdown-status',
		    options=[
			{'label': 'Lactating Mother', 'value': 'Lactating mother'},
			{'label': 'Pregnant Women', 'value': 'Pregnant woman'},
			{'label': 'Children', 'value': 'Child'}
		    ],
		    multi=False,
		    value=""
		)],style={'width': '25%','margin': '2% 5px 0px 2%'}
		),
		html.Div(children = [
		html.Label('Pick Range :'),
		html.Br(),
		dcc.DatePickerRange(
		    id='date-picker-range',
		    start_date=dt(2020, 5, 3),
		    clearable=True,
		    end_date_placeholder_text='Select a date!'
		)],style={'width':'25%','margin': '1.8% 0px 0px 2%'}),
		html.Div([
		dbc.Card([
                dbc.CardBody(
                    [
                        html.H4(id='card_title_1', children=['Total Beneficiaries'], className='card-title',
                                style={'textAlign': 'center','color': '#0074D9'}),
                        html.P(id='card_text_1', style={'textAlign': 'center','color': '#0074D9'}),
                        
                    ])]),dcc.Interval(id="update-counter",interval=10000),
		],style={'width':'10%','margin': '10px 10px 0px 0px'}),
		
		html.Div( children = [
		dcc.Graph(id='map'),
		dcc.Interval(id="update-map",interval=100000),
		],style={'width':'100%','margin': '10px 10px 10px 10px'}),
		
		html.Div([
	        dash_table.DataTable(id='datatable-interactivity',
		columns=[
		    {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
		],
		data=df.to_dict('records'),
		editable=False,
		filter_action="native",
		sort_action="native",
		sort_mode="multi",
		column_selectable="single",
		row_selectable="multi",
		row_deletable=False,
		selected_columns=[],
		selected_rows=[],
		page_action="native",
		page_current= 0,
		page_size= 10,
	    )],style={'width': '100%','margin': '10px 5% 10px 5%'}),
	    html.Div([dcc.Graph(id='boxplot-status'),dcc.Interval(id="update-boxplot-status",interval=10000)],style={'margin': '2% 5% 0px 10%'}),
	    html.Div([dcc.Graph(id='bmi-count'),dcc.Interval(id="update-bmi-count",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	   
		
],style={'display': 'flex','flex-direction': 'row','flex-wrap': 'wrap','overflow': 'hidden'})

##########################################################################################################


########################################### Callbacks ####################################################

#Card to show total count
@app.callback(Output("card_text_1", "children"),
              [Input('update-counter', 'n_intervals')])
def total_count(input_data):
    try:
    	count = pd.read_sql_query('SELECT u_user_id FROM sih2020.beneficiary_beneficiary_register',conn)
    except:
    	print("Something is wrong here")
    return count['u_user_id'].nunique()
    

#Map
@app.callback(Output('map', 'figure'),
              [Input('update-map', 'n_intervals')])
def map_count(input_data):
    fig1 = px.choropleth(
        ap,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='status',
        range_color=(0, 12),
        color_continuous_scale='Viridis'
    )
    #fig1.update_geos(fitbounds="locations", visible=False)
    #count = pd.read_sql_query('SELECT u_user_id FROM sih2020.beneficiary_beneficiary_register',conn)
    return fig1


# Box Plot of BMI for different classes of beneficiaries
@app.callback(
    Output('boxplot-status', 'figure'),
    [Input('update-boxplot-status', 'n_intervals')])
def update_figure(selected_year):
    #filtered_df = df[df.year == selected_year] 
    fig2 = px.box(df, x="status", y="bmi", title="Box Plot of BMI for different classes of beneficiaries")
    fig2.update_layout(transition_duration=500)
    return fig2

# Histogram of count for different BMI levels   
@app.callback(
    Output('bmi-count', 'figure'),
    [Input('update-bmi-count', 'n_intervals')])
def update_figure(n_intervals):
    fig3 = px.histogram(df, x="bmi", color="status", title="Histogram of count for different BMI levels")
    fig3.update_layout(transition_duration=500)
    return fig3


#Dash Table
@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]
        
#########################################################################################################    

if __name__ == '__main__':
    app.run_server(debug=True)
