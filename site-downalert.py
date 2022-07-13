#!/usr/bin/python3
## Get today's date
from datetime import date
## Get today's time
from datetime import datetime

## To connect to mysql
import mysql.connector
## For header info
import requests
## For email notifications
import yagmail
## Generate random valid user agents for request
from fake_useragent import UserAgent

def uptime(url, name, header):
    try:
        response = requests.get(url, headers=header, verify=False)
    except:
        gettime = "n/a"
        status_code_mum: str = "n/a"
        cert_valid = "1"

    return status_code_mum, gettime, cert_valid


    ## For some reason this variable is out of sequence?
    status_code_mum = response.status_code()

    if response.status_code == 200:
        gettime = round(response.elapsed.total_seconds(), 2)
    else:
        gettime = 0

    return status_code_mum, gettime, cert_valid


def writetolog(websiteid, name, status_code_num, gettime, cert_valid):
    now = datetime.now()
    today = date.today()
    getnow = now.strftime('%H:%M')
    getdate = today.strftime('%m/%d/%Y')

    mydb = mysql.connector.connect(port="3306", host="127.0.0.1", user="root", password="Wh@tsApp2017!",
                                   database="pytest")
    cursor = mydb.cursor()

    new_scan = "INSERT INTO uptime (websiteid,date,time,code,speed,cert_valid) VALUES ('" + str(
        websiteid) + "','" + getdate + "','" + getnow + "','" + str(status_code_num) + "','" + str(
        gettime) + "','" + str(cert_valid) + "')"
    print(new_scan)
    cursor.execute(new_scan)

    if status_code_num != 200 or cert_valid == 1:
        body = "Your website: " + url + "Is DOWN! \n\n"
        body += str(response.text.encode('utf8'))
        yag = yagmail.SMTP("bulbs.ie.info@gmail.com", "Beechill2016!")
        yag.send(
            to="mucksie2676@gmail.com",
            subject=name + " is Down or there is a TLS certificate issue!",
            contents=body
        )


mydb = mysql.connector.connect(port="3306", host="127.0.0.1", user="root", password="Wh@tsApp2017!", database="pytest")
new_scan = "SELECT * FROM websites"
cursor = mydb.cursor()
cursor.execute(new_scan)
records = cursor.fetchall()

for row in records:
    websiteid = str(row[0])
    name = str(row[1])
    url = str(row[2])
    # url = "https://expired.badssl.com/" ### For downtime testing
    ua = UserAgent()
    header = {
        'User-Agent': ua.chrome
    }

    status_code_num, gettime, cert_valid = uptime(url, name, header)

    writetolog(websiteid, name, status_code_num, gettime, cert_valid)

    mydb.close()
