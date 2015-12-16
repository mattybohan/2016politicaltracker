#!/usr/bin/env python2.7

# -------------------------------------------------------------------
#           Election 2016 Political Sentiment Tracker v1.0
# -------------------------------------------------------------------
#
#	     "Track opinions of candidates of 2016 Presidental 
#		   candidates by sentiment analysis of social media."
#
#                    Created by Matthew Bohan
#
#
# -------------------------------------------------------------------
#               			system specific 
# -------------------------------------------------------------------
# This code is specific to this use case. Remove for your application.

import sys
sys.path.append('/home3/mtbohanc/python/Python-2.7.11/Lib/site-packages')


# -------------------------------------------------------------------
#               			import modules 
# -------------------------------------------------------------------

# modules related to MySQL and Twitter API

import re
import string
import json
import mysql.connector
from mysql.connector import errorcode
from twython import Twython, TwythonError


# modules related to sentiment analysis

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import time
from time import gmtime, strftime


# -------------------------------------------------------------------
#               			   functions 
# -------------------------------------------------------------------

# 2016Tracker - main function
# input: search term, target MySQL database
# output: most recent 100 tweets matching exactly search term in database

def PoliticalTracker(search_term, db_table):


	# twitter authentication (insert your twitter developer codes here)
	
	twitter = Twython(app_key='insert_yours', # enter your twitter developer info here
	app_secret='insert_yours',
	oauth_token='insert_yours,
	oauth_token_secret='insert_yours')


	# log into sql (insert your config here)
	
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


	# ensure sql database formatted for utf8mb4 to handle emoticons
	
	cursor.execute('SET NAMES utf8mb4')
	cursor.execute("SET CHARACTER SET utf8mb4")
	cursor.execute("SET character_set_connection=utf8mb4")


	# retrieve tweet id for last entry in database
	
	cursor.execute("SELECT tweet_id FROM hillaryclinton ORDER BY id DESC LIMIT 1")
	last_tweet_id = cursor.fetchone()


	# load tweets of search (q) into object called "search_results"
	
	search_results = twitter.search(q=search_term, count=30, since_id=last_tweet_id)
	
	
	# reformat search_results into a dictonary
	
	for entry in search_results:
		d = {}
	
	
	# create instance of Vader sentiment analysis object 
	
	sia = SentimentIntensityAnalyzer()

	
	# walk through search results tweet-by-tweet, perform sentiment analysis, and store
	# results in database
	
	for tweet in reversed(search_results['statuses']):
		
		# store values in variables
		
		user = tweet['user']['screen_name'].encode('utf-8')
		ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
		idvar = tweet['id']
		tweet = tweet['text']		
		
		# perform sentiment analysis user Vader
		
		sentiment = sia.polarity_scores(tweet)
		

		# for each tweet, insert new row into table of sql database

		data_row = (ts, user, idvar, tweet, sentiment['pos'], sentiment['neu'], sentiment['neg'], sentiment['compound'])
		
		s= ' '
		add_row = ("INSERT INTO"), str(db_table), ("(tweet_time, sn, tweet_id, tweet, pos, neut, neg, comp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
		add_row = s.join(add_row)
 
		cursor.execute(add_row, data_row)

	
	# commit database changes and close sql connection
	
	cnx.commit()
	cursor.close()
	cnx.close()

# -------------------------------------------------------------------
#               			   execution 
# -------------------------------------------------------------------

# executes PoliticalTrcker for each candidate

PoliticalTracker("'hillary clinton'", 'hillaryclinton') 
PoliticalTracker("'bernie sanders'", 'berniesanders')
PoliticalTracker("'donald trump'", 'donaldtrump')
PoliticalTracker("'ted cruz'", 'tedcruz')