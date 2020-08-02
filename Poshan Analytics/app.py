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
op = pd.read_csv("sampdata.csv")

######################### Start Dash ################################################
app = dash.Dash(
    __name__
    , meta_tags=[{"name": "viewport", "content": "width=device-width"}]
    #,assets_folder = str(PATH.joinpath("assets").resolve())
    ,external_stylesheets=[dbc.themes.BOOTSTRAP])
######################################################################################

ben_bmi = pd.read_sql_query('SELECT * FROM sih2020.beneficiary_userbmi',conn)
ben_reg = pd.read_sql_query('SELECT * FROM sih2020.beneficiary_beneficiary_register',conn)

print(ben_bmi.u_user_id.dtype)
print(ben_reg.u_phno.dtype)
ben = ben_reg.merge(ben_bmi, left_on='u_phno', right_on='u_user_id')
print(ben)

ben_state_count =pd.read_sql_query('SELECT * FROM sih2020.beneficiary_states',conn)
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
		    color="#001524",
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
			{'label': 'Delhi', 'value': 'National Capital Territory of Delhi'},
			{'label': 'Jammu and Kashmir', 'value': 'Jammu and Kashmir'},
			{'label': 'Puducherry', 'value': 'Puducherry'},			
		    ],
		    multi=False,
		    value=""
		)],style={'width': '50%','margin': '2% 5px 0px 3%'}
		),
	    	
		html.Div(children = [
		html.Label('Pick Range :'),
		html.Br(),
		dcc.DatePickerRange(
		    id='my-date-picker-range',
		    clearable=True,
		    end_date_placeholder_text='Select a date!'
		)],style={'width':'30%','margin': '1.8% 0px 0px 2%'}),
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
	        dash_table.DataTable(id='table-multicol-sorting',
		columns=[
		{"name": i, "id": i} for i in ben_bmi.columns
	    ],
	    page_current=0,
	    page_size=10,
	    page_action='custom',
	    sort_action='custom',
	    sort_mode='multi',
	    sort_by=[]
	    )],style={'width': '100%','margin': '10px 5% 10px 5%'}),
	    html.Div([dcc.Graph(id='ration'),dcc.Interval(id="update-ration",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	    html.Div([dcc.Graph(id='education'),dcc.Interval(id="update-education",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	    html.Div([dcc.Graph(id='yellow-bmi'),dcc.Interval(id="update-yellow-bmi",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	    html.Div([dcc.Graph(id='orange-bmi'),dcc.Interval(id="update-orange-bmi",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	    html.Div([dcc.Graph(id='white-bmi'),dcc.Interval(id="update-white-bmi",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	    html.Div([dcc.Graph(id='boxplot-type'),dcc.Interval(id="update-boxplot-type",interval=10000)],style={'margin': '2% 5% 0px 10%'}),
	    html.Div([dcc.Graph(id='bmi-count'),dcc.Interval(id="update-bmi-count",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	    html.Div([dcc.Graph(id='pie-bmi-women'),dcc.Interval(id="update-pie-bmi-women",interval=10000)],style={'margin': '2% 5% 0px 10%'}),
	    html.Div([dcc.Graph(id='pie-bmi-child1'),dcc.Interval(id="update-pie-bmi-child1",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	    html.Div([dcc.Graph(id='pie-bmi-child2'),dcc.Interval(id="update-pie-bmi-child2",interval=10000)],style={'margin': '2% 5% 0px 10%'}),
	    html.Div([dcc.Graph(id='comparison-women'),dcc.Interval(id="update-comparison-women",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	    html.Div([dcc.Graph(id='comparison-child1'),dcc.Interval(id="update-comparison-child1",interval=10000)],style={'margin': '2% 5% 0px 10%'}),
	    html.Div([dcc.Graph(id='comparison-child2'),dcc.Interval(id="update-comparison-child2",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	   
		
],style={'display': 'flex','flex-direction': 'row','flex-wrap': 'wrap','overflow': 'hidden'})

##########################################################################################################


########################################### Callbacks ####################################################

#Card to show total count
@app.callback(Output("card_text_1", "children"),
              [Input('update-counter', 'n_intervals')])
def total_count(input_data):
    return ben_reg['u_user_id'].nunique()
    

#Map
@app.callback(Output('map', 'figure'),
              [Input('update-map', 'n_intervals')])
def map_count(input_data):
    fig1 = px.choropleth(
        ben_state_count,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='s_states',
        color='s_count',
        color_continuous_scale='Blues',
        labels={'s_count':'No. of Beneficiary','s_states':'State'},
    )
    fig1.update_geos(fitbounds="locations", visible=False)
    fig1.update_layout(height=800)
    return fig1


# Box Plot of BMI for different classes of beneficiaries
@app.callback(
    Output('boxplot-type', 'figure'),
    [Input('update-boxplot-type', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
    fig2 = px.box(df, x="status", y="bmi", title="Box Plot of BMI for different classes of beneficiaries")
    fig2.update_layout(transition_duration=500)
    return fig2

# Histogram of count for different BMI levels   
@app.callback(
    Output('bmi-count', 'figure'),
    [Input('update-bmi-count', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
    fig3 = px.histogram(df, x="bmi", color="status", title="Histogram of count for different BMI levels")
    fig3.update_layout(transition_duration=500)
    return fig3


# For percentage of women in different BMI categories
@app.callback(
    Output('pie-bmi-women', 'figure'),
    [Input('update-pie-bmi-women', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
    standard_bmi = df[(df.bmi >= 18.25) & (df.bmi <= 25) & (df.age >= 18)]
    severely_thin = df[(df.bmi < 16) & (df.age >= 18)]
    moderately_thin = df[(df.bmi >= 16) & (df.bmi < 18.5) & (df.age >= 18)]
    overweight = df[(df.bmi > 25) & (df.age >= 18)]
    df1 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin', 'overweight'],
       'count':[len(standard_bmi), len(severely_thin), len(moderately_thin), len(overweight)]}
    df1 = pd.DataFrame(df1,columns=['bmi_class','count'])
    df1['percentage'] = (df1['count']/df1['count'].sum()) * 100
    fig4 = px.pie(df1, values='percentage', names='bmi_class', title='Percentage of Women in different BMI Categories')
    fig4.update_traces(hole=.4, hoverinfo="label+percent+name")
    fig4.update_layout(transition_duration=500)
    return fig4
    
# For percentage of Children (0-3 yrs) in different BMI categories
@app.callback(
    Output('pie-bmi-child1', 'figure'),
    [Input('update-pie-bmi-child1', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
    standardbmi = df[(df.bmi >= 12) & (df.bmi <= 15) & (df.age <= 3)]
    severelythin = df[(df.bmi <= 7) & (df.age <= 3)]
    moderatelythin = df[(df.bmi > 7) & (df.bmi < 12) & (df.age <= 3)]
    Overweight = df[(df.bmi > 15) & (df.age <= 3)]
    df2 = {'bmi_class':['standardbmi', 'severelythin', 'moderatelythin', 'Overweight'],
       'count':[len(standardbmi), len(severelythin), len(moderatelythin), len(Overweight)]}
    df2 = pd.DataFrame(df2,columns=['bmi_class','count'])
    df2['percentage'] = (df2['count']/df2['count'].sum()) * 100
    fig5 = px.pie(df2, values='percentage', names='bmi_class', title='Percentage of Children (0-3 yrs) in different BMI Categories')
    fig5.update_layout(transition_duration=500)
    return fig5
    
    
# For percentage of Children (4-6 yrs) in different BMI categories  
@app.callback(
    Output('pie-bmi-child2', 'figure'),
    [Input('update-pie-bmi-child2', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
    standardBMI = df[(df.bmi >= 13.5) & (df.bmi <= 16.5) & (df.age > 3) & (df.age <= 6)] # For percentage of Children (4-6 yrs) in different BMI categories
    SeverelyThin = df[(df.bmi >= 7) & (df.bmi <= 8) & (df.age > 3) & (df.age <= 6)]
    ModeratelyThin = df[(df.bmi > 8) & (df.bmi < 13.5) & (df.age > 3) & (df.age <= 6)]
    OverWeight = df[(df.bmi > 16.5) & (df.age > 3) & (df.age <= 6)]
    df3 = {'bmi_class':['standardBMI', 'SeverelyThin', 'ModeratelyThin', 'OverWeight'],
       'count':[len(standardBMI), len(SeverelyThin), len(ModeratelyThin), len(OverWeight)]}
    df3 = pd.DataFrame(df3,columns=['bmi_class','count'])
    df3['percentage'] = (df3['count']/df3['count'].sum()) * 100
    fig6 = px.pie(df3, values='percentage', names='bmi_class', title='Percentage of Children (4-6 yrs) in different BMI Categories')
    fig6.update_layout(transition_duration=500)
    return fig6
    
    
# For comparison of BMI values of women before and after dosage
@app.callback(
    Output('comparison-women', 'figure'),
    [Input('update-comparison-women', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
    standard_bmi1 = ap[(ap.bmi1 >= 18.25) & (ap.bmi1 <= 25) & (ap.age >= 18)]
    x = len(standard_bmi1)
    severely_thin1 = ap[(ap.bmi1 < 16) & (ap.age >= 18)]
    y = len(severely_thin1)
    moderately_thin1 = ap[(ap.bmi1 >= 16) & (ap.bmi1 < 18.5) & (ap.age >= 18)]
    z = len(moderately_thin1)
    overweight1 = ap[(ap.bmi1 > 25) & (ap.age >= 18)]
    standard_bmi2 = ap[(ap.bmi2 >= 18.25) & (ap.bmi2 <= 25) & (ap.age >= 18)]
    x1 = len(standard_bmi2)
    severely_thin2 = ap[(ap.bmi2 < 16) & (ap.age >= 18)]
    y1 = len(severely_thin2)
    moderately_thin2 = ap[(ap.bmi2 >= 16) & (ap.bmi2 < 18.5) & (ap.age >= 18)]
    z1 = len(moderately_thin2)
    overweight2 = ap[(ap.bmi2 > 25) & (ap.age >= 18)]
    bmiclass=['standard_bmi', 'severely_thin', 'moderately_thin']

    fig7 = go.Figure(data=[
        go.Bar(name='after_1_appt', x=bmiclass, y=[x, y, z]),
        go.Bar(name='after_2_appt', x=bmiclass, y=[x1, y1, z1])
    ])
    fig7.update_layout(title_text='Comparison of BMI values of women before and after dosage', yaxis_title_text='Count', barmode='group')
    fig7.update_layout(transition_duration=500)
    return fig7
    

# For comparison of BMI values of Children (0-3) before and after dosage
@app.callback(
    Output('comparison-child1', 'figure'),
    [Input('update-comparison-child1', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
    standardbmi1 = ap[(ap.bmi1 >= 12) & (ap.bmi1 <= 15) & (ap.age <= 3)]
    g = len(standardbmi1)
    severelythin1 = ap[(ap.bmi1 <= 7) & (ap.age <= 3)]
    h = len(severelythin1)
    moderatelythin1 = ap[(ap.bmi1 > 7) & (ap.bmi1 < 12) & (ap.age <= 3)]
    j = len(moderatelythin1)
    standardbmi2 = ap[(ap.bmi2 >= 12) & (ap.bmi2 <= 15) & (ap.age <= 3)]
    G = len(standardbmi2)
    severelythin2 = ap[(ap.bmi2 <= 7) & (ap.age <= 3)]
    H = len(severelythin2)
    moderatelythin2 = ap[(ap.bmi2 > 7) & (ap.bmi2 < 12) & (ap.age <= 3)]
    J = len(moderatelythin2)
    bmiclass=['standard_bmi', 'severely_thin', 'moderately_thin']

    fig8 = go.Figure(data=[
        go.Bar(name='after_1_appt', x=bmiclass, y=[g, h, j]),
        go.Bar(name='after_2_appt', x=bmiclass, y=[G, H, J])
    ])
    fig8.update_layout(title_text='Comparison of BMI values of Children (0-3) before and after dosage', yaxis_title_text='Count', barmode='group')
    fig8.update_layout(transition_duration=500)
    return fig8
    
    
    
    
# For comparison of BMI values of Children (4-6) before and after dosage
@app.callback(
    Output('comparison-child2', 'figure'),
    [Input('update-comparison-child2', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
    standardBMI1 = ap[(ap.bmi1 >= 13.5) & (ap.bmi1 <= 16.5) & (ap.age > 3) & (ap.age <= 6)]
    b = len(standardBMI1)
    SeverelyThin1 = ap[(ap.bmi1 >= 7) & (ap.bmi1 <= 8) & (ap.age > 3) & (ap.age <= 6)]
    n = len(SeverelyThin1)
    ModeratelyThin1 = ap[(ap.bmi1 > 8) & (ap.bmi1 < 13.5) & (ap.age > 3) & (ap.age <= 6)]
    m = len(ModeratelyThin1)
    standardBMI2 = ap[(ap.bmi2 >= 13.5) & (ap.bmi2 <= 16.5) & (ap.age > 3) & (ap.age <= 6)]
    B = len(standardBMI2)
    SeverelyThin2 = ap[(ap.bmi2 >= 7) & (ap.bmi2 <= 8) & (ap.age > 3) & (ap.age <= 6)]
    N = len(SeverelyThin2)
    ModeratelyThin2 = ap[(ap.bmi2 > 8) & (ap.bmi2 < 13.5) & (ap.age > 3) & (ap.age <= 6)]
    M = len(ModeratelyThin2)
    bmiclass=['standard_bmi', 'severely_thin', 'moderately_thin']
    
    fig9 = go.Figure(data=[
        go.Bar(name='after_1_appt', x=bmiclass, y=[b, n, m]),
        go.Bar(name='after_2_appt', x=bmiclass, y=[B, N, M])
    ])
    fig9.update_layout(title_text='Comparison of BMI values of Children (4-6) before and after dosage', yaxis_title_text='Count', barmode='group')
    fig9.update_layout(transition_duration=500)
    return fig9   
  
  
# Pie chart for educaation
@app.callback(
    Output('education', 'figure'),
    [Input('update-education', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
    tenth = op[(op.u_edu == '10th pass')]
    below_tenth = op[(op.u_edu == 'Below 10th')]
    twelveth = op[(op.u_edu == '12th pass')]
    grad = op[(op.u_edu == 'Graduate')]
    op1 = {'edu_class':['10th Pass', '12th Pass', 'Graduate','Below 10th'],
       'count':[len(tenth), len(twelveth), len(grad),len(below_tenth)]}
    op1 = pd.DataFrame(op1,columns=['edu_class','count'])
    op1['percentage'] = (op1['count']/op1['count'].sum()) * 100
    fig14 = px.pie(op1, values='percentage', names='edu_class', title="Beneficiary's Education background")
    fig14.update_layout(transition_duration=500)
    return fig14 
 
 
 
  
#Pie chart for percentage of beneficiaries of different financial background
@app.callback(
    Output('ration', 'figure'),
    [Input('update-ration', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
  
    yellow = op[(op.u_ration == 'Yellow')]
    orange = op[(op.u_ration == 'Orange')]
    white = op[(op.u_ration == 'White')]
    op1 = {'ration_class':['Yellow - below poverty line', 'Orange - annual income Rs.15,000 to Rs.1 Lakh', 'White - annual income over Rs.1 Lakh'],
       'count':[len(yellow), len(orange), len(white)]}
    op1 = pd.DataFrame(op1,columns=['ration_class','count'])
    op1['percentage'] = (op1['count']/op1['count'].sum()) * 100
    fig10 = px.pie(op1, values='percentage', names='ration_class', title="Beneficiary's financial background")
    fig10.update_layout(transition_duration=500)
    return fig10
    
# Pie chart for percentage of beneficiaries in different BMI categories who belong to below poverty line class
@app.callback(
    Output('yellow-bmi', 'figure'),
    [Input('update-yellow-bmi', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):   
    
    standard_bmii = op[(op.currentbmi >= 18.25) & (op.currentbmi <= 25) & (op.u_ration == "Yellow")]
    severely_thinn = op[(op.currentbmi < 16) & (op.u_ration == "Yellow")]
    moderately_thinn = op[(op.currentbmi >= 16) & (op.currentbmi < 18.5) & (op.u_ration == "Yellow")]
    op1 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin'],
       'count':[len(standard_bmii), len(severely_thinn), len(moderately_thinn)]}
    op1 = pd.DataFrame(op1,columns=['bmi_class','count'])
    op1['percentage'] = (op1['count']/op1['count'].sum()) * 100
    fig11 = px.pie(op1, values='percentage', names='bmi_class', title='Beneficiaries in different BMI categories who belong to below poverty line class')
    fig11.update_layout(transition_duration=500)
    return fig11
    
# Piechart for percentage of beneficiaries in different BMI categories whose annual income falls between 15,000 rs. to 1 lakh rs.    
@app.callback(
    Output('orange-bmi', 'figure'),
    [Input('update-orange-bmi', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date): 
    sstandard_bmi = op[(op.currentbmi >= 18.25) & (op.currentbmi <= 25) & (op.u_ration == "Orange")]
    sseverely_thin = op[(op.currentbmi < 16) & (op.u_ration == "Orange")]
    mmoderately_thin = op[(op.currentbmi >= 16) & (op.currentbmi < 18.5) & (op.u_ration == "Orange")]
    op1 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin'],
       'count':[len(sstandard_bmi), len(sseverely_thin), len(mmoderately_thin)]}
    op1 = pd.DataFrame(op1,columns=['bmi_class','count'])
    op1['percentage'] = (op1['count']/op1['count'].sum()) * 100
    fig12 = px.pie(op1,  values="percentage",names="bmi_class", title='Beneficiary- BMI categories v/s annual income between Rs.15K to Rs.1 lakh')
    fig12.update_layout(transition_duration=500)
    return fig12
     
    
#Piechart for percentage of beneficiaries in different BMI categories whose annual income is above 1 lakh rs.    
@app.callback(
    Output('white-bmi', 'figure'),
    [Input('update-white-bmi', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date): 
    sstandard_bmii = op[(op.currentbmi >= 18.25) & (op.currentbmi <= 25) & (op.u_ration == "White")]
    sseverely_thinn = op[(op.currentbmi < 16) & (op.u_ration == "White")]
    mmoderately_thinn = op[(op.currentbmi >= 16) & (op.currentbmi < 18.5) & (op.u_ration == "White")]
    op1 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin'],
       'count':[len(sstandard_bmii), len(sseverely_thinn), len(mmoderately_thinn)]}
    op1 = pd.DataFrame(op1,columns=['bmi_class','count'])
    op1['percentage'] = (op1['count']/op1['count'].sum()) * 100
    fig13 = px.pie(op1,  values="percentage",names="bmi_class", title='Beneficiary- BMI categories v/s annual income above Rs.1 lakh')
    fig13.update_layout(transition_duration=500)
    return fig13   
    

#Dash Table
@app.callback(
    Output('table-multicol-sorting', "data"),
    [Input('table-multicol-sorting', "page_current"),
     Input('table-multicol-sorting', "page_size"),
     Input('table-multicol-sorting', "sort_by")])
def update_table(page_current, page_size, sort_by):
    print(sort_by)
    if len(sort_by):
        dff = ben_bmi.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    else:
        # No sort is applied
        dff = ben_bmi

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')
        
#########################################################################################################    

if __name__ == '__main__':
    app.run_server(debug=True)
