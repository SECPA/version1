import urllib.request
import json
import requests


a="345.23"
data=urllib.request.urlopen( "https://api.thingspeak.com/update?api_key=F3YWHZ30J06XM7XG&field1="+str(a))
data.read()
temp=0
while True:

    x=requests.get("https://api.thingspeak.com/channels/1338770/fields/1.json?api_key=FAKNV5MMSWE00PIQ&results=2").json()
    y=x['feeds'][1]['field1'];
    
    if (y!=temp):
        print(y)
        temp=y
    