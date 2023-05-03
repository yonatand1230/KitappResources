from urllib import response
from firebase import firebase
from datetime import date
from datetime import datetime
from dotenv import load_dotenv
from urllib.request import urlopen
import json, requests, os
 
load_dotenv() # init dotenv to use .env files

# define Firebase URL
fbUrl = os.getenv("fbUrl") # need to configure an .env file with the FB url
fb = firebase.FirebaseApplication(fbUrl, None)


# Read Remote .JSON
print('reading json...')
jsonUrl = 'https://raw.githubusercontent.com/yonatand1230/KitappResources/master/updateFB/halachot.json'
response = urlopen(jsonUrl)
halachot = json.loads(response.read())

# Check Date
print('getting date...')
day = str(date.today())[-2:]
month = str(date.today())[5:7]
print(day, month)

# Find Halacha For Today
print('getting halacha...')
current = halachot.get(month).get(day)

# Prepare Data For Upload
print('preparing for upload...')
upload = {
    'Yomit': current
}

# Upload Data to Database
result = fb.patch('', upload)
print(result)
print('uploaded!')
