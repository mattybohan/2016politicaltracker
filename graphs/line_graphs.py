#!/usr/bin/env python2.7

# -------------------------------------------------------------------
#           Election 2016 Political Sentiment Tracker v1.0
# -------------------------------------------------------------------
#
#	     "Track opinions of candidates of 2016 Presidential 
#		   candidates by sentiment analysis of social media."
#
#                    Created by Matthew Bohan
#
#
# -------------------------------------------------------------------
#                    	      system specific 
# -------------------------------------------------------------------
# This code is specific to this use case. Remove for your application.

import sys
sys.path.append('/home3/mtbohanc/python/Python-2.7.11/Lib/site-packages')


# -------------------------------------------------------------------
#                       	import modules 
# -------------------------------------------------------------------

# modules related to MySQL

import re
import string
import mysql.connector
from mysql.connector import errorcode

# modules related to time

import datetime

# modules related to plotting with Plotly

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *


# -------------------------------------------------------------------
#                       	functions
# -------------------------------------------------------------------


def average(lst):
	return sum(lst)/float(len(lst))

def ProcessData(table_name):

	#log into sql (insert your config here)

	config = {
	'user': 'insert_user', # insert your info
	'password': 'insert_password', # insert your info
	'host': 'insert_host', # insert your info
	'database': 'insert_database', # insert your info
	'raise_on_warnings': True,              
	'use_pure': False,
	}	

	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor(buffered=True)
	
	s = ' '
	query  = ("SELECT time_entered, comp, neg, pos, neut FROM"), str(table_name), ("WHERE time_entered BETWEEN %s AND %s")
	query = s.join(query)
	time = 	(datetime.datetime.now() - datetime.timedelta(minutes=6), datetime.datetime.now())
	cursor.execute(query, time)
	results =  cursor.fetchall()

	t = []
	comp = []
	neg = []
	pos = []
	neu = []

	for x in results:
		if x[1] != 0.0: # this sorts out results that Vader could not compute
			t.append(x[0])
			comp.append(x[1])
			neg.append(x[2])
			pos.append(x[3])
			neu.append(x[4])
		
	comp = average(comp)
	neg = average(neg)
	pos = average(pos)
	neu = average(neu)
	t = t[-1]
	
	cursor.close()
        cnx.close()

	return t, comp, neg, pos, neu



trump_t, trump_comp, trump_neg, trump_pos, trump_neu = ProcessData('donaldtrump')
clinton_t, clinton_comp, clinton_neg, clinton_pos, clinton_neu = ProcessData('hillaryclinton')
cruz_t, cruz_comp, cruz_neg, cruz_pos, cruz_neu = ProcessData('tedcruz')
sanders_t, sanders_comp, sanders_neg, sanders_pos, sanders_neu = ProcessData('berniesanders')


# Figure 1: negative sentiment of twitter uses towards 2016 election cadidates

# create traces
trace0 = go.Scatter(
    x = trump_t,
    y = trump_neg,
    hoverinfo='name',
    line=Line(
    	color='rgb(152, 0, 0)',
    	shape='spline',
	width=1
    ),
    marker=Marker(
	size=4
    ),
    mode='lines+markers',
    name="Donald Trump",
    opacity=0.7,
    uid='292df6',
    xsrc='mattybohan:385:aaa1e5',
    ysrc='mattybohan:385:f72ea3'
)

trace1 = go.Scatter(
    x = trump_t,
    y = cruz_neg,
    hoverinfo='name',
    line=Line(
        color='rgb(214, 39, 40)',
        shape='spline',
        width=1
    ),
    marker=Marker(
        size=4
    ),
    mode='lines+markers',
    name="Ted Cruz",
    opacity=0.7,
    uid='ead7c5',
    xsrc='mattybohan:385:59ea96',
    ysrc='mattybohan:385:6ae495'
)

trace2 = go.Scatter(
    x = trump_t,
    y = clinton_neg,
    hoverinfo='name',
    line=Line(
        color='rgb(31, 119, 180)',
        shape='spline',
        width=1
    ),
    marker=Marker(
        size=4
    ),
    mode='lines+markers',
    name="Hillary Clinton",
    opacity=0.7,
    uid='5d510f',
    xsrc='mattybohan:385:758725',
    ysrc='mattybohan:385:03c2f9'
)

trace3 = go.Scatter(
    x = trump_t,
    y = sanders_neg,
    hoverinfo='name',
    line=Line(
        color='rgb(23, 190, 207)',
        shape='spline',
        width=1
    ),
    marker=Marker(
        size=4
    ),
    mode='lines+markers',
    name="Bernie Sanders",
    opacity=0.7,
    uid='9c7101',
    xsrc='mattybohan:385:96805a',
    ysrc='mattybohan:385:0c1b31'
)

data = [trace0, trace1, trace2, trace3]

layout = Layout(
    annotations=Annotations([
        Annotation(
            x=1450136683053.9868,
            y=0.3,
            font=Font(
                size=20
            ),
            showarrow=False,
            text=''
        )
    ]),
    autosize=True,
    font=Font(
        family='Raleway, sans-serif',
        size=14
    ),
    height=522,
    legend=Legend(
        traceorder='normal',
        xanchor='auto',
        yanchor='auto'
    ),
    margin=Margin(
        pad=10
    ),
    title='Negative Sentiment of Twitter Users Towards 2016 Election Candidates',
    titlefont=dict(
        family='Raleway, sans-serif',
        size=24
    ),
    width=971,
    xaxis=XAxis(
        anchor='y',
        autorange=True,
        range=[1450136674525.2932, 1450140132910.5642],
        side='bottom',
        type='date'
    ),
    yaxis=YAxis(
        autorange=False,
        gridwidth=0.1,
        range=[0, 0.3],
        showgrid=True,
        title='Negative Sentiment',
        type='linear',
        zerolinewidth=1
    )
)
fig = Figure(data=data, layout=layout)
    
plot_url = py.plot(fig, filename='neg-overview', fileopt='extend')



# Figure 2: overall sentiment of twitter uses towards 2016 election cadidates

# create traces
trace0 = go.Scatter(
    x = trump_t,
    y = trump_comp,
    hoverinfo='name',
    line=Line(
        color='rgb(152, 0, 0)',
        shape='spline',
        width=1
    ),
    marker=Marker(
        size=4
    ),
    mode='lines+markers',
    name='Donald Trump',
    opacity=0.7,
    uid='bf0113',
    xsrc='mattybohan:429:3b2262',
    ysrc='mattybohan:429:9d3437'
)

trace1 = go.Scatter(
    x = trump_t,
    y = cruz_comp,
    hoverinfo='name',
    line=Line(
        color='rgb(214, 39, 40)',
        shape='spline',
        width=1
    ),
    marker=Marker(
        size=4
    ),
    mode='lines+markers',
    name='Ted Cruz',
    opacity=0.7,
    uid='aa54b7',
    xsrc='mattybohan:429:3b2262',
    ysrc='mattybohan:429:f97409'
)

trace2 = go.Scatter(
    x = trump_t,
    y = clinton_comp,
    hoverinfo='name',
    line=Line(
        color='rgb(31, 119, 180)',
        shape='spline',
        width=1
    ),
    marker=Marker(
        size=4
    ),
    mode='lines+markers',
    name='Hillary Clinton',
    opacity=0.7,
    uid='0b980f',
    xsrc='mattybohan:429:3b2262',
    ysrc='mattybohan:429:872e72'
)

trace3 = go.Scatter(
    x = trump_t,
    y = sanders_comp,
    hoverinfo='name',
    line=Line(
        color='rgb(23, 190, 207)',
        shape='spline',
        width=1
    ),
    marker=Marker(
        size=4
    ),
    mode='lines+markers',
    name='Bernie Sanders',
    uid='36fc1f',
    opacity=0.7,
    xsrc='mattybohan:429:3b2262',
    ysrc='mattybohan:429:ec36aa'
)

data = [trace0, trace1, trace2, trace3]

layout = Layout(
    annotations=Annotations([
        Annotation(
            x=1450136683053.9868,
            y=0.3,
            font=Font(
                size=20
            ),
            showarrow=False,
            text=''
        )
    ]),
    autosize=True,
    font=Font(
        family='Raleway, sans-serif',
        size=14
    ),
    height=522,
    legend=Legend(
        traceorder='normal',
        xanchor='auto',
        yanchor='auto'
    ),
    margin=Margin(
        pad=10
    ),
    title='How Twitter Feels About the 2016 Election Candidates',
    titlefont=dict(
        family='Raleway, sans-serif',
        size=24
    ),
    width=971,
    xaxis=XAxis(
        anchor='y',
        autorange=True,
        range=[1450126430599.9355, 1450160911924.8994],
        side='bottom',
        type='date'
    ),
    yaxis=YAxis(
        autorange=True,
        gridwidth=0.1,
        range=[-0.5, 0.5],
        showgrid=True,
        title='Sentiment',
        type='linear',
        zerolinewidth=1
    )
)

fig = Figure(data=data, layout=layout)
    
plot_url = py.plot(fig, filename='overview', fileopt='extend')
