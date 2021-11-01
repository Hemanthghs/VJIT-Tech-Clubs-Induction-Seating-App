from flask import Flask, request, render_template
import csv

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find', methods=['POST'])
def check():
    roll_no = request.form['roll']
    result = find_member(roll_list,roll_no)
    nr=0
    if(result == 0):
        nr = 1
    return render_template('index.html',data=result,nr=nr)

@app.route('/verified',methods=['POST'])
def verify():
    print(request.form['submit_a'])
    return render_template('index.html')
    


if __name__ == '__main__':
    app.run(debug=True)