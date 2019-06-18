import os
import sys
import re
import pymysql
import requests as req

hostname = 'localhost'
username = 'root'
password = 'Binance@123'
database = 'binance'

conn = pymysql.connect(
host=hostname, user=username, passwd=password, db=database)
cur = conn.cursor()
cursor = conn.cursor()
print('done')

token = 'ANKR-E97'

def gettradersAddressesFromDatabase():
    try:
        sql_select_Query = "select * from Addresses where token='"+ token +"'"
        conn = pymysql.connect(
        host=hostname, user=username, passwd=password, db=database)
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
        conn.close()

# Insert New Record into database
def insertRecordIntoDatabase(token,address):
    try:
        conn = pymysql.connect(
        host=hostname, user=username, passwd=password, db=database)
        cursor = conn.cursor()
        query = "INSERT INTO `Addresses` (`token`, `Address`) VALUES (%s,%s)"
        cursor.execute(query, (token,
            address
        ))

        conn.commit()
        print("Record inserted succssfully")
    except Exception as ex:
        print("Exception in inserting record" + ex)
    finally:
        cursor.close

def gettradersAddressesFromDex():
    addressData = req.get('https://explorer.binance.org/api/v1/asset-holders?page=1&rows=5&asset='+ token).json()
    assetsHolders = addressData['addressHolders']
    totelCount=addressData['totalNum']
    addressData = req.get('https://explorer.binance.org/api/v1/asset-holders?page=1&rows='+str(totelCount)+'&asset='+token).json()
    assetsHolders = addressData['addressHolders']
    addressSet = set()
    for d in assetsHolders:
        addressSet.add(d['address'])
    return addressSet


addressDexSet=gettradersAddressesFromDex()
addressDBSet=gettradersAddressesFromDatabase()
RecrodstoInsert=addressDexSet-addressDBSet;
#print(RecrodstoInsert)
for d in RecrodstoInsert:
	insertRecordIntoDatabase(token,d)
