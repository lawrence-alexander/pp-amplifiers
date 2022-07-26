import botometer
import time
import csv

rapidapi_key = ''

twitter_app_auth = {
    'consumer_key': '',
    'consumer_secret': '',
    'access_token': '',
    'access_token_secret': '',
  }

twitter_users = ""
output_filename = ""

bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)


try:
    username_file = open(twitter_users, 'r')
    username_list = username_file.readlines()   
    username_file.close()
    
except:  
    print ("Error loading input file")    
    username_list = []

for account in username_list:
    
    account=account.strip()
    try:
        result = bom.check_account(account)    
        universal_overall_raw_score = result['raw_scores']['universal']['overall']
        cap_universal = result['cap']['universal']
        print("[.] Success for account: " + account)
    except:
        print("[!] Not found: " + account)
        universal_overall_raw_score = 5
        cap_universal = 5
      
    with open(output_filename, 'a') as fl:			
        writer = csv.writer(fl,dialect='excel')
        writer.writerow([account,str(universal_overall_raw_score),str(cap_universal)]) 
    fl.close() 
    
    