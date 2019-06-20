import os
import sys
import re
import pymysql
import time
import json
import requests as req
import datetime


with open('/home/ubuntu/BinanceProject/config.json', 'r') as f:
    config = json.load(f)

hostname = config['DATABASE']['HOST']
username = config['DATABASE']['USER']
password = config['DATABASE']['PASSWORD']
database = config['DATABASE']['DBNAME']

symbol = config['TOKEN']['PAIR']
token = config['TOKEN']['BASE']

conn = pymysql.connect(
host=hostname, user=username, passwd=password, db=database)
cur = conn.cursor()
cursor = conn.cursor()


def insertTransactionstoDB(data):
    try:
        print(data)
        cursor = conn.cursor()
        query = "select transactionHash from Transactions where transactionHash = %s and side = %s"
        result = cursor.execute(query,(data["transactionHash"], int(data["side"])))
        #print(result)
        if(result > 0 ):
            return

        query = "INSERT INTO `Transactions` (`Order ID`, `SYMBOL`,`transactionHash`,`Owner`,`Price`,`quantity`,`side`,`total`,`orderCreateTime`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        result = cursor.execute(query, (data["orderId"],data["symbol"],data["transactionHash"],data["owner"],data["price"],data["cumulateQuantity"],int(data["side"]),float(data["price"])*float(data["cumulateQuantity"]),datetime.datetime.strptime(data["transactionTime"], '%Y-%m-%dT%H:%M:%S.%fZ')
        ))

        conn.commit()
        #time.sleep(10)
        #print("Record inserted succssfully")
    except Exception as ex:
        print("Exception in inserting record" + ex)
    finally:
        #conn.commit()
        cursor.close

def gettransactionsFromDex(add):
    millis = int(round(time.time() * 1000) - (80*60*60*1000))
    ordersDataBuy = req.get('https://dex.binance.org/api/v1/orders/closed?address='+add+'&start='+str(millis)+'&symbol='+symbol+'&limit=500').json()
    #print(ordersDataBuy)
    orders = ordersDataBuy['order']
    for o in orders:
        #print(o);
        try:
            if(o['status'] == 'PartialFill' or o['status'] == 'FullyFill'):
                insertTransactionstoDB(o);
        except Exception as ex:
            print("Exception in inserting record" + ex)


def gettradersAddressesFromDatabase():
    try:
        sql_select_Query = "select * from Addresses where token='" + token  + "'"
        cursor = conn.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        addressDBSet = set()
        for row in records:
           #print("Address  ", row[1], )
           addressDBSet.add(row[1])
        cursor.close()
        return addressDBSet
    except Exception as ex:
        print ("Error while connecting to MySQL", ex)


    finally:
        cursor.close()


RecrodstoInsert=gettradersAddressesFromDatabase()

for add in RecrodstoInsert:
    time.sleep(1)
    gettransactionsFromDex(add)
