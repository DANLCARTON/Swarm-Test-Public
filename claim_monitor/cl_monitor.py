'''
CCM
Copyright (c) 2021 Gaëtan Robillard and Jolan Goulin
BSD Simplified License.
For information on usage and redistribution, and for a DISCLAIMER OF ALL
WARRANTIES, see the file, "LICENSE.txt," in this distribution.
'''

# CLAIM MONITOR
# ----------------------------------------------------------------------
# - Monitors Twitter accounts
# - Finds last tweets (saves a date each time the script runs, in /data/date.txt)
# - Updates DB
# List of accounts is available in data/accounts.txt
# ----------------------------------------------------------------------

import cl_utils as u
import connect_api as c
import db
from datetime import datetime
import time
import os
import ml_upd_db as upd
import bt_info as bti

BEARER_TOKEN = bti.getBT()

loopTime = 120 # Main loop/update (default 240)
i = 0
n = 896

# Returns up to nbtweets tweets written by author since date 
# ----------------------------------------------------------------------
def collect(author, nbtweets, date):
    # Connection and requests to twitter API
    # Connect to twitter API and query
    bearer_token = BEARER_TOKEN
    url = c.create_url(author,nbtweets,date)
    headers = c.create_headers(bearer_token)
    json_response = c.connect_to_endpoint(url, headers)
    # Create a counter of new found tweets
    nbNewTweetsdb = 0
    # Display a message if no tweet is found
    if (json_response["meta"]["result_count"]== 0):
        print("No found tweets")
        return (0,0)
    else :
        print("API returned ",json_response["meta"]["result_count"], "tweets") 
        for i in range (len(json_response["data"])): 
            # Create variables to store tweet fields
            tweetId = json_response["data"][i]["id"]
            tweetText = json_response["data"][i]["text"]
            tweetDate = json_response["data"][i]["created_at"]
            print ("tweetId = ", tweetId, "\n")
            print ("tweetText = ", tweetText, "\n")
            print ("tweetDate = ", tweetDate, "\n")
            # Check if tweet already in db
            if (db.isTweetInDB(tweetId) == False):
                # If not add it to db, increase the counter of new tweets
                db.post(tweetId, author, tweetText, tweetDate)
                nbNewTweetsdb = nbNewTweetsdb + 1
        print(author, "tweeted", nbNewTweetsdb, "new tweets")
        # Return the number of found tweets
        return (json_response["meta"]["result_count"], nbNewTweetsdb)

# Author list creation and query parameters 
listAuthors = u.keywords("data/accounts.txt")
nbTweetsToCollect = 100
dayRange = 7
hourRange = 0

# Definition of numbers of tweets found and added to the database
nbFoundTweets = 0
nbTweetsAdd = 0

# Main Loop
# ----------------------------------------------------------------------
while(True):
    date = datetime.now()
    # Choice of date
    # lastDate() searches in date.txt the last run
    # datePreviousDay() searches for the last 24h
    date = u.datePreviousDay()
    # tweet collect loop 
    for Author in listAuthors :
        print('--------------------')
        print(Author)
        nbNewTweets = collect(Author, nbTweetsToCollect, date)
        nbFoundTweets = nbFoundTweets + nbNewTweets[0]
        nbTweetsAdd = nbTweetsAdd + nbNewTweets[1]
    # Display the number of found tweets
    print("--------------------")
    print("--------------------")
    print(date)
    print(nbFoundTweets, "found tweets from API request")
    print(nbTweetsAdd, "new tweet(s) written in DB")
    u.updateDate()
    
    upd.updateDB()

    nbNewTweets = 0
    nbTweetsAdd = 0
    i += 1

    print ("The search for tweets will automatically restart in two minutes.........")
    time.sleep(loopTime)
