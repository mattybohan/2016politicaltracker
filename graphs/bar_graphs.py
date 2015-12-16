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
	query  = ("SELECT time_entered, comp, neg, pos, neut FROM"), str(table_name)
	query = s.join(query)
	cursor.execute(query)
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

# -------------------------------------------------------------------
#                       	implementation 
# -------------------------------------------------------------------

# process data and store in respective variables

trump_t, trump_comp, trump_neg, trump_pos, trump_neu = ProcessData('donaldtrump')
clinton_t, clinton_comp, clinton_neg, clinton_pos, clinton_neu = ProcessData('hillaryclinton')
cruz_t, cruz_comp, cruz_neg, cruz_pos, cruz_neu = ProcessData('tedcruz')
sanders_t, sanders_comp, sanders_neg, sanders_pos, sanders_neu = ProcessData('berniesanders')


# create bar chart - sentiment comparison

data = Data([
    Bar(
        x=['Donald Trump', 'Ted Cruz', 'Hillary Clinton', 'Bernie Sanders'],
        y=[0.03277936946902653, 0.039895284717533265, 0.004863510023367316, 0.10885975404145493],
        marker=Marker(
            color=['rgb(152, 0, 0)', 'rgb(214, 39, 40)', 'rgb(31, 119, 180)', 'rgb(23, 190, 207)'],
            colorsrc='mattybohan:469:c6ba54'
        ),
        name='y',
        opacity=0.65,
        uid='ef2d44',
        xsrc='mattybohan:469:60cad9',
        ysrc='mattybohan:469:0e6fc4'
    )
])
layout = Layout(
    autosize=True,
    font=Font(
        family='Raleway, sans-serif',
        size=18
    ),
    height=472,
    title='Twitter Feels: The Bern?',
    titlefont=dict(
        size=24
    ),
    width=966,
    xaxis=XAxis(
        autorange=True,
        range=[-0.5, 3.5],
        type='category'
    ),
    yaxis=YAxis(
        autorange=True,
        range=[0, 0.11458921478047887],
        title='Sentiment',
        type='linear'
    )
)
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig)
