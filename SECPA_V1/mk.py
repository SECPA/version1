import urllib.request
import json
import requests
import pandas
df=pandas.read_csv("./csv/dataset1.csv")
x=requests.get("https://api.thingspeak.com/channels/1342740/feeds.json?api_key=2PRTTEP676NB37QI&results=2").json()
y=x['feeds'][1]['field3'];

print(y)