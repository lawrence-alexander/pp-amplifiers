#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time
from requests_oauthlib import OAuth1
import argparse

"""Blocks and optionally reports a list of Twitter accounts
   based on a text file containing either user names or user IDs
   @LawrenceA_UK
"""

# Tokens and keys
client_key = ''
client_secret =''
maintoken = ''

token = ''
token_secret =''


# Auth setup
oauth = OAuth1(client_key,client_secret,token,token_secret)

#
# This function takes in username or user ID as string, block only option as bool, and returns HTTP status code
#
def report_block(screen_name_id, report, block): 
            # Build appropriate URL for ID or username
            screen_name_id=str(screen_name_id) 
            # Distinguish block only/block and report and build appropriate request URL
            if report == False:
                        
                        if screen_name_id.isdigit()==False:    
                                    api_url = "https://api.twitter.com/1.1/blocks/create.json?screen_name=%s" % (screen_name_id)
                        else:
                                    api_url = "https://api.twitter.com/1.1/blocks/create.json?user_id=%s" % (screen_name_id)                            
                        
            else:
                        if screen_name_id.isdigit()==False:    
                                    api_url = "https://api.twitter.com/1.1/users/report_spam.json?screen_name=%s&perform_block=%s" % (screen_name_id, str(block).lower())
                        else:
                                    api_url = "https://api.twitter.com/1.1/users/report_spam.json?user_id=%s&perform_block=%s" % (screen_name_id, str(block).lower())           
            
            response = requests.post(api_url, auth=oauth) 
            
            time.sleep(20)
            return (response.status_code)

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, required=True)
parser.add_argument('--report', action='store_true')
parser.add_argument('--block', action='store_true')
args = parser.parse_args()

# Load blocklist from text file

try:
            username_file = open(args.file, 'r')
            username_list = username_file.readlines()   
            username_file.close()

except:  
            print ("Error loading input file")    
            username_list = []

for tweeter in username_list:
            tweeter=tweeter.strip() 
            status = report_block(screen_name_id=tweeter,report=args.report, block=args.block)
            
            if status == 200:
                        if args.report == True:
                                    print("Report successful for account: %s" % tweeter)
                        else:
                                    print("Operation successful for account: %s" % tweeter)
            else:
                        print("Error code %d returned for account %s" % (status, tweeter))
                       
