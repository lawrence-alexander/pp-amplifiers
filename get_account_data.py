#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time
import csv
import datetime
import argparse
from requests_oauthlib import OAuth1

"""Get account status and metadata for list of accounts
   based on a text file of user names or user IDs
   @LawrenceA_UK
"""
# Tokens and keys

client_key = ''
client_secret =''
token = ''
token_secret =''

# Base for Twitter calls

base_twitter_url = "https://api.twitter.com/1.1/"

# Auth setup

oauth = OAuth1(client_key,client_secret,token,token_secret)

twitter_users=""
output_filename = ""

try:
        username_file = open(twitter_users, 'r')
        username_list = username_file.readlines()   
        username_file.close()

except:  
        print ("Error loading input file")    
        username_list = []

#
# Function to return Twitter user ID from a user name, or vice versa
#

def twitter_user_lookup(screen_name_id): 
        screen_name_id=str(screen_name_id) 
        
        # Distinguish block only/block and report and build appropriate request URL
        if screen_name_id.isdigit()==False:  
                
                api_url = "https://api.twitter.com/1.1/users/lookup.json?screen_name=%s" % (screen_name_id)
        else:
                api_url = "https://api.twitter.com/1.1/users/lookup.json?user_id=%s" % (screen_name_id)   

        # Pause to handle Twitter rate limiting      
        time.sleep(1)
        
        # Get user details
        response = requests.get(api_url, auth=oauth)
        
        try:
                user_profiles = json.loads (response.content)
                for user_profile in user_profiles:
                        screen_name = user_profile['screen_name']
                        user_id = user_profile ['id_str']
                        followers_count = user_profile['followers_count']
                        friends_count = user_profile['friends_count']
                        status_count = user_profile['statuses_count']
                        ff_tweets = round((followers_count+friends_count)/status_count,3)
                        
                        
        except:
                user_id = 0
                ff_tweets = 0
                screen_name = screen_name_id
                
        # If user account is absent (i.e, returns 404) discover whether suspended or deleted        
        if response.status_code == 404:
                api_url = 'https://api.twitter.com/1.1/users/show.json?screen_name=%s' % screen_name_id
                response = requests.get(api_url, auth=oauth)
                gone_type = json.loads(response.content)
                absence_code = gone_type['errors'][0]['code']
                absence_reason = gone_type['errors'][0]['message']
        else:
                absence_code = 0
                absence_reason = "none"
        return (response.status_code, user_id, ff_tweets, absence_code, absence_reason, screen_name)  


for account in username_list:

        account=account.strip()
        account_data=twitter_user_lookup(screen_name_id=account) 
        status_code=account_data[0]
        user_id = account_data[1]
        ff_tweets =  account_data[2]
        timestamp = str(datetime.datetime.now())
        absence_code = account_data[3]
        absence_reason = account_data[4]
        screen_name = account_data[5]
        
        twitter_url = "https://twitter.com/i/user/%s" % (user_id)
        if output_filename[-1]== 'v':
        
                with open(output_filename, 'a') as fl:	
                        
                        writer = csv.writer(fl,dialect='excel')
                        writer.writerow([timestamp, screen_name, user_id, str(ff_tweets), str(status_code),str(absence_code),absence_reason,twitter_url]) 
                        print("[.] Account %s returned status %s" % (account, str(status_code)))
        else:
                with open(output_filename, 'a') as fl:
                        if user_id !=0:
                                fl.write(user_id + "\n")
                        print("[.] Account %s returned status %s" % (account, str(status_code)))
                     
        fl.close() 



