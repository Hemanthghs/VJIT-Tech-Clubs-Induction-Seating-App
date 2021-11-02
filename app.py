from flask import Flask, request, render_template
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

##############################
seating_ids = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10', 'a11', 'a12', 'a13', 'a14', 'a15', 'a16', 'a17', 'a18', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12', 'b13', 'b14', 'b15', 'b16', 'b17', 'b18', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13', 'c14', 'c15', 'c16', 'c17', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13', 'd14', 'd15', 'd16', 'd17', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12', 'e13', 'e14', 'e15', 'e16', 'e17', 'e18', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'g9', 'g10', 'g11', 'g12', 'g13', 'g14', 'g15', 'g16', 'g17', 'g18', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8', 'i9', 'i10', 'i11', 'i12', 'i13', 'i14', 'i15', 'i16', 'i17', 'i18', 'j1', 'j2', 'j3', 'j4', 'j5', 'j6', 'j7', 'j8', 'j9', 'j10', 'j11', 'j12', 'j13', 'j14', 'j15', 'j16', 'j17', 'j18', 'k1', 'k2', 'k3', 'k4', 'k5', 'k6', 'k7', 'k8', 'k9', 'k10', 'k11', 'k12', 'k13', 'k14', 'k15', 'k16', 'k17', 'k18', 'l1', 'l2', 'l3', 'l4', 'l5', 'l6', 'l7', 'l8', 'l9', 'l10', 'l11', 'l12', 'l13', 'l14', 'l15', 'l16', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'm10', 'm11', 'm12', 'm13', 'm14', 'm15', 'm16', 'm17', 'm18', 'm19', 'm20']
##############################





app = Flask(__name__)
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
            result.append(seating_ids[list(df1.index[df1["Rolls"]==dic["id"]])[0]])
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
                    result.append(seating_ids[i])
                    return render_template("index.html",data=result)
                    # return render_template('index.html',data=result)
            


    else:
        print("Your seat:",list(df1.index[df1["Rolls"]==dic["id"]])[0])
        
        return render_template("index.html",data=result,allocated=seating_ids[list(df1.index[df1["Rolls"]==dic["id"]])[0]])
    
    
    
    return render_template('index.html')


@app.route('/allocated')
def get_allocated():
    df1=pd.read_csv("final.csv")
    # print(seating_ids)
    # print(list(df1["Rolls"]))
    # print(list(df1["Branch"]))
    # return render_template("allocated.html",seats=seating_ids,roll_list=list(df1["Rolls"]),branchs=list(df1["Branch"]))
    return render_template("allocated.html",alloc=[seating_ids,list(df1["Rolls"]),list(df1["Branch"])])


if __name__ == '__main__':
    # app.run(host="0.0.0.0")
    app.run()
    