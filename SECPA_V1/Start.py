from flask import Flask, render_template, request
import pandas
from sklearn import linear_model
import urllib.request
import json
import requests
import time
import smtplib, ssl

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "secpainfo@gmail.com"
receiver_email = "muthu.111714@sxcce.edu.in"
password = "SECPA@123"

app=Flask(__name__)


@app.route('/')

def index():
    return render_template('index.html')

@app.route("/startup")
def start():
    return render_template('startserver.html')



@app.route("/startcheckup")
def server():
    
    predictedval=requests.get("https://api.thingspeak.com/channels/1347065/fields/1.json?api_key=934WUGFO0N5VVEXR&results=2").json()
    pre=predictedval['feeds'][1]['field1'];
    duration=requests.get("https://api.thingspeak.com/channels/1361952/feeds.json?api_key=NSVQ2ZSBG5S2AWAQ&results=2").json()
    dur=duration['feeds'][1]['field1']
    entry=duration['feeds'][1]['entry_id']
    t_ent=int(entry)
    #dur=int(dur)*60
    dur=0
    alert=0
    while True:
        if(dur<=0):
            duration=requests.get("https://api.thingspeak.com/channels/1361952/feeds.json?api_key=NSVQ2ZSBG5S2AWAQ&results=2").json()
            entry=int(duration['feeds'][1]['entry_id'])
            print(entry,t_ent)
            if(entry!=t_ent) :
                dur=int(duration['feeds'][1]['field1'])
                t_ent=entry
                print(entry)
                alert=0
                continue
            x=requests.get("https://api.thingspeak.com/channels/1342740/fields/1.json?results=2").json()
            act=float(x['feeds'][1]['field1']);
            if(alert==0 and act>=1):
                print("--------alert---------")
                message = """
                Subject: SECPA Duration Alert

                Since the duration is over the energy is used in the room. Take necassary action."""
                context = ssl.create_default_context()
                with smtplib.SMTP(smtp_server, port) as server:
                    server.ehlo()  # Can be omitted
                    server.starttls(context=context)
                    server.ehlo()  # Can be omitted
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message)
                alert=1
            
        x=requests.get("https://api.thingspeak.com/channels/1342740/fields/1.json?results=2").json()
        act=x['feeds'][1]['field1'];
        if(int(dur)>0 and float(act)>float(pre)):
            print("high")
            message = """
            Subject: SECPA Duration Alert

            The Energy usage is exceed than the predicted value. Please take necessary action."""
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
            dur-=1
            continue
        
        time.sleep(1)
@app.route("/home")
def home():
    df=pandas.read_csv("./csv/actvspre.csv")
    df = df. sort_values(by=["Duration"], ascending=True)
    actual=list(df['actualval'])
    predict=list(df['predictval'])
    duration=list(df['Duration'])
    return render_template("pass.html",actual=actual,predict=predict,duration=duration,length=len(duration))

@app.route('/',methods=['POST'])
def getvalue():
    stud=request.form['stud']
    duration=request.form['duration']
    df=pandas.read_csv("./csv/dataset.csv")
    x=df[['no_of_student','duration']]
    y=df['energy_consumed']
    regr = linear_model.LinearRegression()
    regr.fit(x, y)
    predictenergy=regr.predict([[stud,34]])
    pred=abs(float(predictenergy))
    data=urllib.request.urlopen( "https://api.thingspeak.com/update?api_key=FQQ0DE3Z6IIMRVJ2&field1="+str(pred))
    data.read()
    data=urllib.request.urlopen( "https://api.thingspeak.com/update?api_key=YPLB5WPW91C2793T&field1="+str(duration))
    data.read()
    return render_template('index.html',predict=pred)
    

if __name__ == '__main__':
    app.run(debug=True)
getvalue()