import requests
import time 
from datetime import datetime
# # payload = {'arduino': "" , 'error': "", 'make_request': "", 'on_off': "", 'pin': "", 'plant_id': "", "timestamp": ""}
# r = requests.get('http://localhost:5000/requests/1')
# print(r.text)

##########################################
# Date format conversion test 
##########################################

def convertTimeFormat(date):
    dateT = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    dateO = datetime.strftime(dateT, "%Y-%m-%d+%H%%3A%M%%3A%S")
    print(dateO)
    return dateO

date = datetime.now().strftime("%Y-%m-%d+%H%%3A%M%%3A%S")
print(date)

timeT = '2020-04-30 04:10:38'
timeC = '2020-04-30+04%3A10%3A38'
timeO = convertTimeFormat(timeT)

if timeO == timeC:
    print("They match!")
else: 
    print("Nope") 