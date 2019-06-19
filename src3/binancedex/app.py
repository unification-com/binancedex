from flask import Flask
from flask import Flask, render_template, jsonify, redirect, request, url_for
from datetime import datetime
import os
import sys
import re
import pymysql
import time
import requests as req
import datetime
import json
from collections import OrderedDict

with open('config.json', 'r') as f:
    config = json.load(f)

hostname = config['DATABASE']['HOST']
username = config['DATABASE']['USER']
password = config['DATABASE']['PASSWORD']
database = config['DATABASE']['DBNAME']

marketPair = config['TOKEN']['PAIR']


app = Flask(__name__)

def extractTime(jsonObj):
    try:
        return int(jsonObj['timestamp'])
    except:
        return 0


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/gettraders")
def getTraders():
    conn = pymysql.connect(host=hostname, user=username, passwd=password, db=database)
    cur = conn.cursor()
    cur.execute("SELECT Owner, side, DATE(ordercreatetime) AS dated, SUM(total) AS value FROM Transactions WHERE symbol = '" + marketPair + "' GROUP BY Owner, side, DATE(ordercreatetime) ORDER BY value desc, dated DESC")
    row_headers=[x[0] for x in cur.description]
    myresult = cur.fetchall()
    json_data=[]
    resultDict = {}
    for result in myresult:
        key = result[0]
        dt = datetime.datetime(result[2].year,result[2].month,result[2].day,0,0,0).timestamp() * 1000
        if key not in resultDict:
            dataArray = []
            if(result[1] == 1) :
                dataArray.append({'dated':(result[2]).strftime("%d-%m-%Y"),'bought':result[3], 'sold':0.0,'timestamp':dt})
            else :
                dataArray.append({'dated':(result[2]).strftime("%d-%m-%Y"),'bought':0.0, 'sold':result[3],'timestamp':dt})
            resultDict.update({key:dataArray})
        
        else:
            dArray = resultDict[key]
            match = False
            for a in dArray:
                if(a['dated'] == (result[2]).strftime("%d-%m-%Y")):
                    match = True
                    if(result[1]== 1):                        
                        a.update({'bought':result[3]})
                    else:
                        a.update({'sold':result[3]})
            
            if not match :                
                if(result[1] == 1) :
                    dArray.append({'dated':(result[2]).strftime("%d-%m-%Y"),'bought':result[3], 'sold':0.0,'timestamp':dt})
                else :
                    dArray.append({'dated':(result[2]).strftime("%d-%m-%Y"),'bought':0.0, 'sold':result[3],'timestamp':dt})
                

                
        json_data.append(dict(zip(row_headers,result)))
    
    #print(resultDict)
    cur.execute("SELECT Owner, SUM(total) AS value FROM Transactions WHERE symbol = '" + marketPair + "' GROUP BY Owner ORDER BY value desc")
    myresult = cur.fetchall()
    finalResult = []
    for d in myresult:
        finalResult.append({d[0]:sorted(resultDict[d[0]],key=lambda i:i['timestamp'])})

    return jsonify(finalResult)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
