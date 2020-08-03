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

ENDPOINT="sih2020v2.co9od6laqqv8.ap-south-1.rds.amazonaws.com"
PORT="3306"
USR="admin"
REGION="ap-south-1"
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
#dataframe
ap = pd.read_csv('small_dataset.csv')

######################### Start Dash ################################################
app = dash.Dash(
    __name__
    , meta_tags=[{"name": "viewport", "content": "width=device-width"}]
    ,external_stylesheets=[dbc.themes.BOOTSTRAP])
######################################################################################

ben_reg = pd.read_sql_query('SELECT * FROM sih2020.beneficiary_beneficiary_register',conn)
ben_bmi = pd.read_sql_query('SELECT * FROM sih2020.beneficiary_userbmi',conn)

ben = ben_reg.merge(ben_bmi, left_on='u_phno', right_on='u_user_id')
ben.drop(['id_x','u_fname', 'u_sname','u_user_id_x','u_verified','id_y','u_status','u_verified','u_father','u_mother'],axis = 1, inplace = True)
print(ben)
ben_state_count =pd.read_sql_query('SELECT * FROM sih2020.beneficiary_states',conn)

############################# Layout of the Dashboard ################################

app.title = 'Poshan Analytics'
app.layout = html.Div(children=[
		html.Div(children = [ 
		dbc.NavbarSimple(
		    children=[
			dbc.NavItem(dbc.NavLink("Web Portal", href="http://ec2-13-233-253-221.ap-south-1.compute.amazonaws.com:8000/")),
		    ],
		    brand="Real-Time Poshan Analytics",
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
		    min_date_allowed=ben['bmdate'].min(),
		    max_date_allowed=ben['bmdate'].max(),
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
		{"name": i, "id": i} for i in ben_state_count.columns
	    ],
	    page_current=0,
	    page_size=10,
	    page_action='custom',
	    sort_action='custom',
	    sort_mode='multi',
	    sort_by=[],
	    style_cell={'textAlign': 'left'},
	    style_as_list_view=True,
	    )],style={'width': '90%','margin': '10px 5% 10px 5%'}),
	    html.Div([dcc.Graph(id='boxplot-type'),dcc.Interval(id="update-boxplot-type",interval=10000)],style={'margin': '2% 5% 0px 10%'}),
	    html.Div([dcc.Graph(id='bmi-count'),dcc.Interval(id="update-bmi-count",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	    html.Div([dcc.Graph(id='ration'),dcc.Interval(id="update-ration",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	    html.Div([dcc.Graph(id='education'),dcc.Interval(id="update-education",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	    html.Div([dcc.Graph(id='yellow-bmi'),dcc.Interval(id="update-yellow-bmi",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	    html.Div([dcc.Graph(id='orange-bmi'),dcc.Interval(id="update-orange-bmi",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	    html.Div([dcc.Graph(id='white-bmi'),dcc.Interval(id="update-white-bmi",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	    html.Div([dcc.Graph(id='pie-bmi-women'),dcc.Interval(id="update-pie-bmi-women",interval=10000)],style={'margin': '2% 5% 0px 10%'}),
	    html.Div([dcc.Graph(id='pie-bmi-child1'),dcc.Interval(id="update-pie-bmi-child1",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	    html.Div([dcc.Graph(id='comparison-women'),dcc.Interval(id="update-comparison-women",interval=10000)],style={'margin': '2% 5% 0px 5%'}),
	    html.Div([dcc.Graph(id='comparison-child1'),dcc.Interval(id="update-comparison-child1",interval=10000)],style={'margin': '2% 5% 0px 10%'}),		
],style={'display': 'flex','flex-direction': 'row','flex-wrap': 'wrap','overflow': 'hidden'})

##########################################################################################################


########################################### Callbacks ####################################################

#Card to show total count
@app.callback(Output("card_text_1", "children"),
              [Input('update-counter', 'n_intervals')])
def total_count(input_data):
    return ben_reg.u_adhar.nunique()
    

#Map
@app.callback(Output('map', 'figure'),
              [Input('update-map', 'n_intervals')])
def map_count(input_data):
    fig = px.choropleth(
        ben_state_count,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='s_states',
        color='s_count',
        color_continuous_scale='Blues',
        labels={'s_count':'No. of Beneficiaries','s_states':'State'},)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=800)
    return fig
    
#Dash Table
@app.callback(
    Output('table-multicol-sorting', "data"),
    [Input('table-multicol-sorting', "page_current"),
     Input('table-multicol-sorting', "page_size"),
     Input('table-multicol-sorting', "sort_by")])
def update_table(page_current, page_size, sort_by):
    print(sort_by)
    if len(sort_by):
        dff = ben_state_count.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    else:
        # No sort is applied
        dff = ben_state_count

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')


# Box Plot of BMI for different classes of beneficiaries
@app.callback(
    Output('boxplot-type', 'figure'),
    [Input('update-boxplot-type', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
    try:
        start_date= dt.strptime(start_date, '%Y-%m-%d').date()
        end_date = dt.strptime(end_date, '%Y-%m-%d').date()
    except Exception as e:
        print("{}".format(e))
    if(selected_state and start_date and end_date):
        mask = (ben['u_states'] == selected_state) & (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        fig1 = px.box(ben, x=ben[mask]['u_type'], y=ben[mask]['currentbmi'], title="Box Plot of BMI for 1:Mother , 0:Children")
        fig1.update_layout(transition_duration=500)
        
    elif(selected_state):
        mask=(ben['u_states'] == selected_state)
        fig1 = px.box(ben, x=ben[mask]['u_type'], y=ben[mask]['currentbmi'],title="Box Plot of BMI for 1:Mother , 0:Children")
        fig1.update_layout(transition_duration=500)
    elif(start_date and end_date):
        mask = (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        fig1 = px.box(ben, x=ben[mask]['u_type'], y=ben[mask]['currentbmi'], title="Box Plot of BMI for 1:Mother , 0:Children")
        fig1.update_layout(transition_duration=500)    
    else :
        fig1 = px.box(ben, x=ben.u_type, y=ben.currentbmi,title="Box Plot of BMI for 1:Mother , 0:Children")
        fig1.update_layout(transition_duration=500)
    return fig1

# Histogram of count for different BMI levels   
@app.callback(
    Output('bmi-count', 'figure'),
    [Input('update-bmi-count', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
    try:
        start_date= dt.strptime(start_date, '%Y-%m-%d').date()
        end_date = dt.strptime(end_date, '%Y-%m-%d').date()
    except Exception as e:
        print("{}".format(e))
    if(selected_state and start_date and end_date):
        mask = (ben['u_states'] == selected_state) & (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        fig2 = px.histogram(ben, x=ben[mask]['currentbmi'], color=ben[mask]['u_type'], title="Histogram : BMI Distribution and Count")
        fig2.update_layout(transition_duration=500)
        
    elif(selected_state):
        mask=(ben['u_states'] == selected_state)
        fig2 = px.histogram(ben, x=ben[mask]['currentbmi'], color=ben[mask]['u_type'], title="Histogram : BMI Distribution and Count")
        fig2.update_layout(transition_duration=500)
    elif(start_date and end_date):
        mask = (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        fig2 = px.histogram(ben, x=ben[mask]['currentbmi'], color=ben[mask]['u_type'], title="Histogram : BMI Distribution and Count")
        fig2.update_layout(transition_duration=500)
    else:
        fig2 = px.histogram(ben, x=ben['currentbmi'], color=ben['u_type'], title="Histogram : BMI Distribution and Count")
        fig2.update_layout(transition_duration=500)


    return fig2
    
    
#Pie chart for percentage of beneficiaries of different financial background
@app.callback(
    Output('ration', 'figure'),
    [Input('update-ration', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
    try:
        start_date= dt.strptime(start_date, '%Y-%m-%d').date()
        end_date = dt.strptime(end_date, '%Y-%m-%d').date()
    except Exception as e:
        print("{}".format(e))
    if(selected_state and start_date and end_date):
        mask = (ben['u_states'] == selected_state) & (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        yellow = ben[mask][(ben.u_ration == 'Yellow')]
        print (yellow)
        print(ben)
        orange = ben[mask][(ben.u_ration == 'Orange')]
        white = ben[mask][(ben.u_ration == 'White')]
        op1 = {'ration_class':['Yellow - below poverty line', 'Orange - annual income Rs.15,000 to Rs.1 Lakh', 'White - annual income over Rs.1 Lakh'],
           'count':[len(yellow), len(orange), len(white)]}
        op1 = pd.DataFrame(op1,columns=['ration_class','count'])
        op1['percentage'] = (op1['count']/op1['count'].sum()) * 100
        fig3 = px.pie(op1, values='percentage', names='ration_class', title="Beneficiary's financial background")
        fig3.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig3.update_layout(transition_duration=500)
        
    elif(selected_state):
        mask=(ben['u_states'] == selected_state)
        yellow = ben[mask][(ben.u_ration == 'Yellow')]
        orange = ben[mask][(ben.u_ration == 'Orange')]
        white = ben[mask][(ben.u_ration == 'White')]
        op1 = {'ration_class':['Yellow - below poverty line', 'Orange - annual income Rs.15,000 to Rs.1 Lakh', 'White - annual income over Rs.1 Lakh'],
           'count':[len(yellow), len(orange), len(white)]}
        op1 = pd.DataFrame(op1,columns=['ration_class','count'])
        op1['percentage'] = (op1['count']/op1['count'].sum()) * 100
        fig3 = px.pie(op1, values='percentage', names='ration_class', title="Beneficiary's financial background")
        fig3.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig3.update_layout(transition_duration=500)
    elif(start_date and end_date):
        mask = (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        yellow = ben[mask][(ben.u_ration == 'Yellow')]
        orange = ben[mask][(ben.u_ration == 'Orange')]
        white = ben[mask][(ben.u_ration == 'White')]
        op1 = {'ration_class':['Yellow - below poverty line', 'Orange - annual income Rs.15,000 to Rs.1 Lakh', 'White - annual income over Rs.1 Lakh'],
           'count':[len(yellow), len(orange), len(white)]}
        op1 = pd.DataFrame(op1,columns=['ration_class','count'])
        op1['percentage'] = (op1['count']/op1['count'].sum()) * 100
        fig3 = px.pie(op1, values='percentage', names='ration_class', title="Beneficiary's financial background")
        fig3.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig3.update_layout(transition_duration=500)
    else:
        yellow = ben[(ben.u_ration == 'Yellow')]
        orange = ben[(ben.u_ration == 'Orange')]
        white = ben[(ben.u_ration == 'White')]
        op1 = {'ration_class':['Yellow - below poverty line', 'Orange - annual income Rs.15,000 to Rs.1 Lakh', 'White - annual income over Rs.1 Lakh'],
           'count':[len(yellow), len(orange), len(white)]}
        op1 = pd.DataFrame(op1,columns=['ration_class','count'])
        op1['percentage'] = (op1['count']/op1['count'].sum()) * 100
        fig3 = px.pie(op1, values='percentage', names='ration_class', title="Beneficiary's financial background")
        fig3.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig3.update_layout(transition_duration=500)

    return fig3
    
    
    
# Pie chart for education
@app.callback(
    Output('education', 'figure'),
    [Input('update-education', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
    try:
        start_date= dt.strptime(start_date, '%Y-%m-%d').date()
        end_date = dt.strptime(end_date, '%Y-%m-%d').date()
    except Exception as e:
        print("{}".format(e))
    if(selected_state and start_date and end_date):
        mask = (ben['u_states'] == selected_state) & (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        tenth = ben[mask][(ben.u_edu == '10th pass')]
        below_tenth = ben[mask][(ben.u_edu == 'Below 10th')]
        twelveth = ben[mask][(ben.u_edu == '12th pass')]
        grad = ben[mask][(ben.u_edu == 'Graduate')]
        op2 = {'edu_class':['10th Pass', '12th Pass', 'Graduate','Below 10th'],
           'count':[len(tenth), len(twelveth), len(grad),len(below_tenth)]}
        op2 = pd.DataFrame(op2,columns=['edu_class','count'])
        op2['percentage'] = (op2['count']/op2['count'].sum()) * 100
        fig4 = px.pie(op2, values='percentage', names='edu_class', title="Beneficiary's Education background")
        fig4.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig4.update_layout(transition_duration=500)
        
    elif(selected_state):
        mask=(ben['u_states'] == selected_state)
        tenth = ben[mask][(ben.u_edu == '10th pass')]
        below_tenth = ben[mask][(ben.u_edu == 'Below 10th')]
        twelveth = ben[mask][(ben.u_edu == '12th pass')]
        grad = ben[mask][(ben.u_edu == 'Graduate')]
        op2 = {'edu_class':['10th Pass', '12th Pass', 'Graduate','Below 10th'],
           'count':[len(tenth), len(twelveth), len(grad),len(below_tenth)]}
        op2 = pd.DataFrame(op2,columns=['edu_class','count'])
        op2['percentage'] = (op2['count']/op2['count'].sum()) * 100
        fig4 = px.pie(op2, values='percentage', names='edu_class', title="Beneficiary's Education background")
        fig4.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig4.update_layout(transition_duration=500)
    elif(start_date and end_date):
        mask = (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        tenth = ben[mask][(ben.u_edu == '10th pass')]
        below_tenth = ben[mask][(ben.u_edu == 'Below 10th')]
        twelveth = ben[mask][(ben.u_edu == '12th pass')]
        grad = ben[mask][(ben.u_edu == 'Graduate')]
        op2 = {'edu_class':['10th Pass', '12th Pass', 'Graduate','Below 10th'],
           'count':[len(tenth), len(twelveth), len(grad),len(below_tenth)]}
        op2 = pd.DataFrame(op2,columns=['edu_class','count'])
        op2['percentage'] = (op2['count']/op2['count'].sum()) * 100
        fig4 = px.pie(op2, values='percentage', names='edu_class', title="Beneficiary's Education background")
        fig4.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig4.update_layout(transition_duration=500)
    else:
        tenth = ben[(ben.u_edu == '10th pass')]
        below_tenth = ben[(ben.u_edu == 'Below 10th')]
        twelveth = ben[(ben.u_edu == '12th pass')]
        grad = ben[(ben.u_edu == 'Graduate')]
        op2 = {'edu_class':['10th Pass', '12th Pass', 'Graduate','Below 10th'],
           'count':[len(tenth), len(twelveth), len(grad),len(below_tenth)]}
        op2 = pd.DataFrame(op2,columns=['edu_class','count'])
        op2['percentage'] = (op2['count']/op2['count'].sum()) * 100
        fig4 = px.pie(op2, values='percentage', names='edu_class', title="Beneficiary's Education background")
        fig4.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig4.update_layout(transition_duration=500)
    return fig4 
    
    
# Pie chart for percentage of beneficiaries in different BMI categories who belong to below poverty line class
@app.callback(
    Output('yellow-bmi', 'figure'),
    [Input('update-yellow-bmi', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):   
    try:
        start_date= dt.strptime(start_date, '%Y-%m-%d').date()
        end_date = dt.strptime(end_date, '%Y-%m-%d').date()
    except Exception as e:
        print("{}".format(e))
        
    if(selected_state and start_date and end_date):
        mask = (ben['u_states'] == selected_state) & (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        standard_bmii = ben[mask][(ben.currentbmi >= 18.25) & (ben.currentbmi <= 25) & (ben.u_ration == "Yellow")]
        severely_thinn = ben[mask][(ben.currentbmi < 16) & (ben.u_ration == "Yellow")]
        moderately_thinn = ben[mask][(ben.currentbmi >= 16) & (ben.currentbmi < 18.5) & (ben.u_ration == "Yellow")]
        op3 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin'],
           'count':[len(standard_bmii), len(severely_thinn), len(moderately_thinn)]}
        op3 = pd.DataFrame(op3,columns=['bmi_class','count'])
        op3['percentage'] = (op3['count']/op3['count'].sum()) * 100
        fig5 = px.pie(op3, values='percentage', names='bmi_class', title='Different BMI categories of Beneficiaries who belong to below poverty line class')
        fig5.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig5.update_layout(transition_duration=500)
        
    elif(selected_state):
        mask=(ben['u_states'] == selected_state)
        standard_bmii = ben[mask][(ben.currentbmi >= 18.25) & (ben.currentbmi <= 25) & (ben.u_ration == "Yellow")]
        severely_thinn = ben[mask][(ben.currentbmi < 16) & (ben.u_ration == "Yellow")]
        moderately_thinn = ben[mask][(ben.currentbmi >= 16) & (ben.currentbmi < 18.5) & (ben.u_ration == "Yellow")]
        op3 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin'],
           'count':[len(standard_bmii), len(severely_thinn), len(moderately_thinn)]}
        op3 = pd.DataFrame(op3,columns=['bmi_class','count'])
        op3['percentage'] = (op3['count']/op3['count'].sum()) * 100
        fig5 = px.pie(op3, values='percentage', names='bmi_class', title='Different BMI categories of Beneficiaries who belong to below poverty line class')
        fig5.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig5.update_layout(transition_duration=500)
    elif(start_date and end_date):
        mask = (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        standard_bmii = ben[mask][(ben.currentbmi >= 18.25) & (ben.currentbmi <= 25) & (ben.u_ration == "Yellow")]
        severely_thinn = ben[mask][(ben.currentbmi < 16) & (ben.u_ration == "Yellow")]
        moderately_thinn = ben[mask][(ben.currentbmi >= 16) & (ben.currentbmi < 18.5) & (ben.u_ration == "Yellow")]
        op3 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin'],
           'count':[len(standard_bmii), len(severely_thinn), len(moderately_thinn)]}
        op3 = pd.DataFrame(op3,columns=['bmi_class','count'])
        op3['percentage'] = (op3['count']/op3['count'].sum()) * 100
        fig5 = px.pie(op3, values='percentage', names='bmi_class', title='Different BMI categories of Beneficiaries who belong to below poverty line class')
        fig5.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig5.update_layout(transition_duration=500)
    else:
        standard_bmii = ben[(ben.currentbmi >= 18.25) & (ben.currentbmi <= 25) & (ben.u_ration == "Yellow")]
        severely_thinn = ben[(ben.currentbmi < 16) & (ben.u_ration == "Yellow")]
        moderately_thinn = ben[(ben.currentbmi >= 16) & (ben.currentbmi < 18.5) & (ben.u_ration == "Yellow")]
        op3 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin'],
           'count':[len(standard_bmii), len(severely_thinn), len(moderately_thinn)]}
        op3 = pd.DataFrame(op3,columns=['bmi_class','count'])
        op3['percentage'] = (op3['count']/op3['count'].sum()) * 100
        fig5 = px.pie(op3, values='percentage', names='bmi_class', title='Different BMI categories of Beneficiaries who belong to below poverty line class')
        fig5.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig5.update_layout(transition_duration=500)
    
    return fig5
    
# Piechart for percentage of beneficiaries in different BMI categories whose annual income falls between 15,000 rs. to 1 lakh rs.    
@app.callback(
    Output('orange-bmi', 'figure'),
    [Input('update-orange-bmi', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date): 
    try:
        start_date= dt.strptime(start_date, '%Y-%m-%d').date()
        end_date = dt.strptime(end_date, '%Y-%m-%d').date()
    except Exception as e:
        print("{}".format(e))
    if(selected_state and start_date and end_date):
        mask = (ben['u_states'] == selected_state) & (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        sstandard_bmi = ben[mask][(ben.currentbmi >= 18.25) & (ben.currentbmi <= 25) & (ben.u_ration == "Orange")]
        sseverely_thin = ben[mask][(ben.currentbmi < 16) & (ben.u_ration == "Orange")]
        mmoderately_thin = ben[mask][(ben.currentbmi >= 16) & (ben.currentbmi < 18.5) & (ben.u_ration == "Orange")]
        op4 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin'],
           'count':[len(sstandard_bmi), len(sseverely_thin), len(mmoderately_thin)]}
        op4 = pd.DataFrame(op4,columns=['bmi_class','count'])
        op4['percentage'] = (op4['count']/op4['count'].sum()) * 100
        fig6 = px.pie(op4,  values="percentage",names="bmi_class", title='Beneficiary- BMI categories v/s annual income between Rs.15K to Rs.1 lakh')
        fig6.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig6.update_layout(transition_duration=500)
        
    elif(selected_state):
        mask=(ben['u_states'] == selected_state)
        sstandard_bmi = ben[mask][(ben.currentbmi >= 18.25) & (ben.currentbmi <= 25) & (ben.u_ration == "Orange")]
        sseverely_thin = ben[mask][(ben.currentbmi < 16) & (ben.u_ration == "Orange")]
        mmoderately_thin = ben[mask][(ben.currentbmi >= 16) & (ben.currentbmi < 18.5) & (ben.u_ration == "Orange")]
        op4 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin'],
           'count':[len(sstandard_bmi), len(sseverely_thin), len(mmoderately_thin)]}
        op4 = pd.DataFrame(op4,columns=['bmi_class','count'])
        op4['percentage'] = (op4['count']/op4['count'].sum()) * 100
        fig6 = px.pie(op4,  values="percentage",names="bmi_class", title='Beneficiary- BMI categories v/s annual income between Rs.15K to Rs.1 lakh')
        fig6.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig6.update_layout(transition_duration=500)
    elif(start_date and end_date):
        mask = (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        sstandard_bmi = ben[mask][(ben.currentbmi >= 18.25) & (ben.currentbmi <= 25) & (ben.u_ration == "Orange")]
        sseverely_thin = ben[mask][(ben.currentbmi < 16) & (ben.u_ration == "Orange")]
        mmoderately_thin = ben[mask][(ben.currentbmi >= 16) & (ben.currentbmi < 18.5) & (ben.u_ration == "Orange")]
        op4 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin'],
           'count':[len(sstandard_bmi), len(sseverely_thin), len(mmoderately_thin)]}
        op4 = pd.DataFrame(op4,columns=['bmi_class','count'])
        op4['percentage'] = (op4['count']/op4['count'].sum()) * 100
        fig6 = px.pie(op4,  values="percentage",names="bmi_class", title='Beneficiary- BMI categories v/s annual income between Rs.15K to Rs.1 lakh')
        fig6.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig6.update_layout(transition_duration=500)
    else:
        sstandard_bmi = ben[(ben.currentbmi >= 18.25) & (ben.currentbmi <= 25) & (ben.u_ration == "Orange")]
        sseverely_thin = ben[(ben.currentbmi < 16) & (ben.u_ration == "Orange")]
        mmoderately_thin = ben[(ben.currentbmi >= 16) & (ben.currentbmi < 18.5) & (ben.u_ration == "Orange")]
        op4 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin'],
           'count':[len(sstandard_bmi), len(sseverely_thin), len(mmoderately_thin)]}
        op4 = pd.DataFrame(op4,columns=['bmi_class','count'])
        op4['percentage'] = (op4['count']/op4['count'].sum()) * 100
        fig6 = px.pie(op4,  values="percentage",names="bmi_class", title='Beneficiary- BMI categories v/s annual income between Rs.15K to Rs.1 lakh')
        fig6.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig6.update_layout(transition_duration=500)
    return fig6
     
    
#Piechart for percentage of beneficiaries in different BMI categories whose annual income is above 1 lakh rs.    
@app.callback(
    Output('white-bmi', 'figure'),
    [Input('update-white-bmi', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date): 
    try:
        start_date= dt.strptime(start_date, '%Y-%m-%d').date()
        end_date = dt.strptime(end_date, '%Y-%m-%d').date()
    except Exception as e:
        print("{}".format(e))
    if(selected_state and start_date and end_date):
        mask = (ben['u_states'] == selected_state) & (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        sstandard_bmii = ben[mask][(ben.currentbmi >= 18.25) & (ben.currentbmi <= 25) & (ben.u_ration == "White")]
        sseverely_thinn = ben[mask][(ben.currentbmi < 16) & (ben.u_ration == "White")]
        mmoderately_thinn = ben[mask][(ben.currentbmi >= 16) & (ben.currentbmi < 18.5) & (ben.u_ration == "White")]
        op5 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin'],
           'count':[len(sstandard_bmii), len(sseverely_thinn), len(mmoderately_thinn)]}
        op5 = pd.DataFrame(op5,columns=['bmi_class','count'])
        op5['percentage'] = (op5['count']/op5['count'].sum()) * 100
        fig7 = px.pie(op5,  values="percentage",names="bmi_class", title='Beneficiary- BMI categories v/s annual income above Rs.1 lakh')
        fig7.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig7.update_layout(transition_duration=500)
        
    elif(selected_state):
        mask=(ben['u_states'] == selected_state)
        sstandard_bmii = ben[mask][(ben.currentbmi >= 18.25) & (ben.currentbmi <= 25) & (ben.u_ration == "White")]
        sseverely_thinn = ben[mask][(ben.currentbmi < 16) & (ben.u_ration == "White")]
        mmoderately_thinn = ben[mask][(ben.currentbmi >= 16) & (ben.currentbmi < 18.5) & (ben.u_ration == "White")]
        op5 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin'],
           'count':[len(sstandard_bmii), len(sseverely_thinn), len(mmoderately_thinn)]}
        op5 = pd.DataFrame(op5,columns=['bmi_class','count'])
        op5['percentage'] = (op5['count']/op5['count'].sum()) * 100
        fig7 = px.pie(op5,  values="percentage",names="bmi_class", title='Beneficiary- BMI categories v/s annual income above Rs.1 lakh')
        fig7.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig7.update_layout(transition_duration=500)
    elif(start_date and end_date):
        mask = (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        sstandard_bmii = ben[mask][(ben.currentbmi >= 18.25) & (ben.currentbmi <= 25) & (ben.u_ration == "White")]
        sseverely_thinn = ben[mask][(ben.currentbmi < 16) & (ben.u_ration == "White")]
        mmoderately_thinn = ben[mask][(ben.currentbmi >= 16) & (ben.currentbmi < 18.5) & (ben.u_ration == "White")]
        op5 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin'],
           'count':[len(sstandard_bmii), len(sseverely_thinn), len(mmoderately_thinn)]}
        op5 = pd.DataFrame(op5,columns=['bmi_class','count'])
        op5['percentage'] = (op5['count']/op5['count'].sum()) * 100
        fig7 = px.pie(op5,  values="percentage",names="bmi_class", title='Beneficiary- BMI categories v/s annual income above Rs.1 lakh')
        fig7.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig7.update_layout(transition_duration=500)
    else:
        sstandard_bmii = ben[(ben.currentbmi >= 18.25) & (ben.currentbmi <= 25) & (ben.u_ration == "White")]
        sseverely_thinn = ben[(ben.currentbmi < 16) & (ben.u_ration == "White")]
        mmoderately_thinn = ben[(ben.currentbmi >= 16) & (ben.currentbmi < 18.5) & (ben.u_ration == "White")]
        op5 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin'],
           'count':[len(sstandard_bmii), len(sseverely_thinn), len(mmoderately_thinn)]}
        op5 = pd.DataFrame(op5,columns=['bmi_class','count'])
        op5['percentage'] = (op5['count']/op5['count'].sum()) * 100
        fig7 = px.pie(op5,  values="percentage",names="bmi_class", title='Beneficiary- BMI categories v/s annual income above Rs.1 lakh')
        fig7.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig7.update_layout(transition_duration=500)
    return fig7   



# For percentage of women in different BMI categories
@app.callback(
    Output('pie-bmi-women', 'figure'),
    [Input('update-pie-bmi-women', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
    try:
        start_date= dt.strptime(start_date, '%Y-%m-%d').date()
        end_date = dt.strptime(end_date, '%Y-%m-%d').date()
    except Exception as e:
        print("{}".format(e))
    if(selected_state and start_date and end_date):
        mask = (ben['u_states'] == selected_state) & (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        standard_bmi = ben[mask][(ben.currentbmi >= 18.25) & (ben.currentbmi <= 25) & (ben.u_type == 1)]
        severely_thin = ben[mask][(ben.currentbmi < 16) & (ben.u_type == 1)]
        moderately_thin = ben[mask][(ben.currentbmi >= 16) & (ben.currentbmi < 18.5) & (ben.u_type == 1)]
        overweight = ben[(ben.currentbmi > 25) & (ben.u_type == 1)]
        df1 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin', 'overweight'],
           'count':[len(standard_bmi), len(severely_thin), len(moderately_thin), len(overweight)]}
        df1 = pd.DataFrame(df1,columns=['bmi_class','count'])
        df1['percentage'] = (df1['count']/df1['count'].sum()) * 100
        fig8 = px.pie(df1, values='percentage', names='bmi_class', title='Percentage of Women in different BMI Categories')
        fig8.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig8.update_layout(transition_duration=500)
        
    elif(selected_state):
        mask=(ben['u_states'] == selected_state)
        standard_bmi = ben[mask][(ben.currentbmi >= 18.25) & (ben.currentbmi <= 25) & (ben.u_type == 1)]
        severely_thin = ben[mask][(ben.currentbmi < 16) & (ben.u_type == 1)]
        moderately_thin = ben[mask][(ben.currentbmi >= 16) & (ben.currentbmi < 18.5) & (ben.u_type == 1)]
        overweight = ben[(ben.currentbmi > 25) & (ben.u_type == 1)]
        df1 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin', 'overweight'],
           'count':[len(standard_bmi), len(severely_thin), len(moderately_thin), len(overweight)]}
        df1 = pd.DataFrame(df1,columns=['bmi_class','count'])
        df1['percentage'] = (df1['count']/df1['count'].sum()) * 100
        fig8 = px.pie(df1, values='percentage', names='bmi_class', title='Percentage of Women in different BMI Categories')
        fig8.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig8.update_layout(transition_duration=500)
    elif(start_date and end_date):
        mask = (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        standard_bmi = ben[mask][(ben.currentbmi >= 18.25) & (ben.currentbmi <= 25) & (ben.u_type == 1)]
        severely_thin = ben[mask][(ben.currentbmi < 16) & (ben.u_type == 1)]
        moderately_thin = ben[mask][(ben.currentbmi >= 16) & (ben.currentbmi < 18.5) & (ben.u_type == 1)]
        overweight = ben[(ben.currentbmi > 25) & (ben.u_type == 1)]
        df1 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin', 'overweight'],
           'count':[len(standard_bmi), len(severely_thin), len(moderately_thin), len(overweight)]}
        df1 = pd.DataFrame(df1,columns=['bmi_class','count'])
        df1['percentage'] = (df1['count']/df1['count'].sum()) * 100
        fig8 = px.pie(df1, values='percentage', names='bmi_class', title='Percentage of Women in different BMI Categories')
        fig8.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig8.update_layout(transition_duration=500)
    else:
        standard_bmi = ben[(ben.currentbmi >= 18.25) & (ben.currentbmi <= 25) & (ben.u_type == 1)]
        severely_thin = ben[(ben.currentbmi < 16) & (ben.u_type == 1)]
        moderately_thin = ben[(ben.currentbmi >= 16) & (ben.currentbmi < 18.5) & (ben.u_type == 1)]
        overweight = ben[(ben.currentbmi > 25) & (ben.u_type == 1)]
        df1 = {'bmi_class':['standard_bmi', 'severely_thin', 'moderately_thin', 'overweight'],
           'count':[len(standard_bmi), len(severely_thin), len(moderately_thin), len(overweight)]}
        df1 = pd.DataFrame(df1,columns=['bmi_class','count'])
        df1['percentage'] = (df1['count']/df1['count'].sum()) * 100
        fig8 = px.pie(df1, values='percentage', names='bmi_class', title='Percentage of Women in different BMI Categories')
        fig8.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig8.update_layout(transition_duration=500)
    return fig8
    
# For percentage of Children (0-3 yrs) in different BMI categories
@app.callback(
    Output('pie-bmi-child1', 'figure'),
    [Input('update-pie-bmi-child1', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
    try:
        start_date= dt.strptime(start_date, '%Y-%m-%d').date()
        end_date = dt.strptime(end_date, '%Y-%m-%d').date()
    except Exception as e:
        print("{}".format(e))
    if(selected_state and start_date and end_date):
        mask = (ben['u_states'] == selected_state) & (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        standardbmi = ben[mask][(ben.currentbmi >= 12) & (ben.currentbmi <= 15) & (ben.u_type == 0)]
        severelythin = ben[mask][(ben.currentbmi <= 7) & (ben.u_type == 0)]
        moderatelythin = ben[mask][(ben.currentbmi > 7) & (ben.currentbmi < 12) & (ben.u_type == 0)]
        Overweight = ben[mask][(ben.currentbmi > 15) & (ben.u_type == 0)]
        df2 = {'bmi_class':['standardbmi', 'severelythin', 'moderatelythin', 'Overweight'],
           'count':[len(standardbmi), len(severelythin), len(moderatelythin), len(Overweight)]}
        df2 = pd.DataFrame(df2,columns=['bmi_class','count'])
        df2['percentage'] = (df2['count']/df2['count'].sum()) * 100
        fig9 = px.pie(df2, values='percentage', names='bmi_class', title='Percentage of Children in different BMI Categories')
        fig9.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig9.update_layout(transition_duration=500)
        
    elif(selected_state):
        mask=(ben['u_states'] == selected_state)
        standardbmi = ben[mask][(ben.currentbmi >= 12) & (ben.currentbmi <= 15) & (ben.u_type == 0)]
        severelythin = ben[mask][(ben.currentbmi <= 7) & (ben.u_type == 0)]
        moderatelythin = ben[mask][(ben.currentbmi > 7) & (ben.currentbmi < 12) & (ben.u_type == 0)]
        Overweight = ben[mask][(ben.currentbmi > 15) & (ben.u_type == 0)]
        df2 = {'bmi_class':['standardbmi', 'severelythin', 'moderatelythin', 'Overweight'],
           'count':[len(standardbmi), len(severelythin), len(moderatelythin), len(Overweight)]}
        df2 = pd.DataFrame(df2,columns=['bmi_class','count'])
        df2['percentage'] = (df2['count']/df2['count'].sum()) * 100
        fig9 = px.pie(df2, values='percentage', names='bmi_class', title='Percentage of Children in different BMI Categories')
        fig9.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig9.update_layout(transition_duration=500)
    elif(start_date and end_date):
        mask = (ben['bmdate'] >= start_date) & (ben['bmdate'] < end_date)
        standardbmi = ben[mask][(ben.currentbmi >= 12) & (ben.currentbmi <= 15) & (ben.u_type == 0)]
        severelythin = ben[mask][(ben.currentbmi <= 7) & (ben.u_type == 0)]
        moderatelythin = ben[mask][(ben.currentbmi > 7) & (ben.currentbmi < 12) & (ben.u_type == 0)]
        Overweight = ben[mask][(ben.currentbmi > 15) & (ben.u_type == 0)]
        df2 = {'bmi_class':['standardbmi', 'severelythin', 'moderatelythin', 'Overweight'],
           'count':[len(standardbmi), len(severelythin), len(moderatelythin), len(Overweight)]}
        df2 = pd.DataFrame(df2,columns=['bmi_class','count'])
        df2['percentage'] = (df2['count']/df2['count'].sum()) * 100
        fig9 = px.pie(df2, values='percentage', names='bmi_class', title='Percentage of Children in different BMI Categories')
        fig9.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig9.update_layout(transition_duration=500)
    else:
        standardbmi = ben[(ben.currentbmi >= 12) & (ben.currentbmi <= 15) & (ben.u_type == 0)]
        severelythin = ben[(ben.currentbmi <= 7) & (ben.u_type == 0)]
        moderatelythin = ben[(ben.currentbmi > 7) & (ben.currentbmi < 12) & (ben.u_type == 0)]
        Overweight = ben[(ben.currentbmi > 15) & (ben.u_type == 0)]
        df2 = {'bmi_class':['standardbmi', 'severelythin', 'moderatelythin', 'Overweight'],
           'count':[len(standardbmi), len(severelythin), len(moderatelythin), len(Overweight)]}
        df2 = pd.DataFrame(df2,columns=['bmi_class','count'])
        df2['percentage'] = (df2['count']/df2['count'].sum()) * 100
        fig9 = px.pie(df2, values='percentage', names='bmi_class', title='Percentage of Children in different BMI Categories')
        fig9.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig9.update_layout(transition_duration=500)
    return fig9
    
    
    
# For comparison of BMI values of women before and after dosage(This doesn't use live data since less data for demonstration purpose - Future visualization)
@app.callback(
    Output('comparison-women', 'figure'),
    [Input('update-comparison-women', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
    try:
        start_date= dt.strptime(start_date, '%Y-%m-%d').date()
        end_date = dt.strptime(end_date, '%Y-%m-%d').date()
    except Exception as e:
        print("{}".format(e))
   
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

    fig10 = go.Figure(data=[
        go.Bar(name='after_1_appt', x=bmiclass, y=[x, y, z]),
        go.Bar(name='after_2_appt', x=bmiclass, y=[x1, y1, z1])
    ])
    fig10.update_layout(title_text='Comparison of BMI values of women before and after dosage', yaxis_title_text='Count', barmode='group')
    fig10.update_layout(transition_duration=500)
    return fig10
    

# For comparison of BMI values of Children before and after dosagev(This doesn't use live data since less data for demonstration purpose - Future visualization)
@app.callback(
    Output('comparison-child1', 'figure'),
    [Input('update-comparison-child1', 'n_intervals'),
    Input('dropdown-state', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(n_intervals,selected_state,start_date,end_date):
    try:
        start_date= dt.strptime(start_date, '%Y-%m-%d').date()
        end_date = dt.strptime(end_date, '%Y-%m-%d').date()
    except Exception as e:
        print("{}".format(e))
    
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

    fig11 = go.Figure(data=[
        go.Bar(name='after_1_appt', x=bmiclass, y=[g, h, j]),
        go.Bar(name='after_2_appt', x=bmiclass, y=[G, H, J])
    ])
    fig11.update_layout(title_text='Comparison of BMI values of Children before and after dosage', yaxis_title_text='Count', barmode='group')
    fig11.update_layout(transition_duration=500)
    return fig11
    
    
        
#########################################################################################################    

if __name__ == '__main__':
    app.run_server(debug=True)
