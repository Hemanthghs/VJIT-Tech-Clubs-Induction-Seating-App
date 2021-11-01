from flask import Flask, request, render_template, redirect, url_for
from flask_ngrok import run_with_ngrok
import csv
import pandas as pd
import numpy as np


##############################
with open('data/data.csv','r') as file:
    reader = csv.reader(file)
    print(reader)
    data_list = []
    for r in reader:
        data_list.append(r)

roll_list = []
for i in data_list[1:]:
    roll_list.append(i[3])
    
def find_member(roll_list, roll):
    # index=0
    for i in roll_list:
        # count=count+1
        if(i==roll):
            return data_list[roll_list.index(roll)+1]
    else:
        return 0
##############################


app = Flask(__name__)
# run_with_ngrok(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find', methods=['POST'])
def check():
    global result
    roll_no = request.form['roll']
    result = find_member(roll_list,roll_no)
    print(result)
    
    if result!=0:
        dic = {
        "id":result[3],
        "Branch" : result[5]
        }
    
    df1=pd.read_csv("final.csv")
    if "Unnamed: 0" in list(df1.columns):
        df1 = df1.drop(['Unnamed: 0'],axis=1)
    if result!=0:
        if dic["id"] in list(df1["Rolls"]):
            result.append(list(df1.index[df1["Rolls"]==dic["id"]])[0])
        else:
            result.append("Not allocated yet")
    nr=0
    if(result == 0):
        nr = 1
    return render_template('index.html',data=result,nr=nr)

@app.route('/verified',methods=['POST'])
def verify():
    print(request.form['submit_a'])
    dic = {
    "id":result[3],
    "Branch" : result[5]
    }
    
        
    df1=pd.read_csv("final.csv")
    if "Unnamed: 0" in list(df1.columns):
        df1 = df1.drop(['Unnamed: 0'],axis=1)



    if dic["id"] not in list(df1["Rolls"]):
        if "empty" not in list(df1[df1['Branch']==dic["Branch"].lower()]['Rolls']):
                print(dic["Branch"],"is full")
                return render_template("index.html",full=str(dic["Branch"] + " is full"))
        else:
            for i in list(df1.index[df1['Branch']==dic["Branch"].lower()]):

                if df1["Rolls"][i] == "empty":
                    df1["Rolls"][i] = dic["id"]
                    print(i)
                    df1.to_csv("final.csv",index=False)
                    return render_template("index.html",allocated=i)
                    # return render_template('index.html',data=result)
            


    else:
        print("YOU HECK, DON'T FK***n MESS WITH ME. Your seat:",list(df1.index[df1["Rolls"]==dic["id"]])[0])
        
        return render_template("index.html",allocated=list(df1.index[df1["Rolls"]==dic["id"]])[0])
    
    
    
    return render_template('index.html')
    


if __name__ == '__main__':
    app.run(host="0.0.0.0")