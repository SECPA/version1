from flask import Flask, render_template, request
import pandas
app=Flask(__name__)

@app.route('/')

def index():
    return render_template('graph.html')

@app.route('/',methods=['POST'])
def getvalue():
    stud=request.form['stud']
    temp=34
    df=pandas.read_csv("dataset1.csv")
    x=df[['No_of_Stud','Room_temp']]
    y=df['Energy_cons']
    regr = linear_model.LinearRegression()
    regr.fit(x, y)
    predictenergy=regr.predict([[stud,34]])
    return render_template('pass.html',predict=predictenergy)
    

if __name__ == '__main__':
    app.run(debug=True)
getvalue()