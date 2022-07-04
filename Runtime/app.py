from ast import Pass
from tracemalloc import start
from flask import Flask, render_template, request
import time
import json
import sqlite3

conn = sqlite3.connect('ni.db')
conn = sqlite3.connect('di.db')
c= conn.cursor()

app = Flask(__name__)
@app.route('/')
def home():
   return render_template('index.html')


@app.route('/range',methods=['POST','GET'])
def nirange():
    conn = sqlite3.connect('ni.db')
    c= conn.cursor()
    idr1=str(request.form['range1'])
    idr2=str(request.form['range2'])
    c.execute("select * from ni where id between '"+idr1+"' and '"+idr2+"'order by id;") 
    range=c.fetchall()
    c.execute("select min(id), max(id) as l_id from ni where id between '"+idr1+"' and '"+idr2+"';") 
    range2=c.fetchall()
    return render_template('/nirange.html',r=range, s=range2)


@app.route('/filter', methods=['POST','GET'])
def dirange():
    conn = sqlite3.connect('di.db')
    c= conn.cursor()
    rid1=str(request.form['id1'])
    rid2=str(request.form['id2'])
    c.execute("select * from di where id between '"+rid1+"' and '"+rid2+"';")
    rangeid=c.fetchall()
    return render_template('/dirange.html', d=rangeid)



@app.route('/matches', methods=['POST','GET'])
def datamatch():
    conn = sqlite3.connect('di.db')
    c= conn.cursor()
    code=str(request.form['code'])
    match=str(request.form['number'])
    start=time.time()
    c.execute("select * from di where code ='"+code+"' limit '"+match+"';")
    matches=c.fetchall()
    end=time.time()
    total=end-start
    return render_template('/matches.html', m=matches, t=total)
    

@app.route('/timetaken', methods=['POST','GET'])
def takentime():
    conn = sqlite3.connect('ni.db')
    c= conn.cursor()
    uservalue=str(request.form['time'])
    start=time.time()
    for i in range(1, int(uservalue)):
        c.execute("Select * from ni")
        query= c.fetchall()
    end=time.time()
    total=end-start
    return render_template('/timetaken.html', q=query, k=total) 
    


if __name__ == '__main__':
    app.debug=True
    app.run()