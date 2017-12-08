import urllib2
import json
import logging
import time

vzip = 'localhost'
froniusip = '192.168.82.81'
uuid_gesamt = '429cc1e0-3899-11e7-8e5f-31c9198ccb1b'
gesamtleistung = str(0)
froniusurl = 'http://' + str(froniusip) + '/solar_api/v1/GetInverterRealtimeData.cgi?Scope=Device&DeviceId=1&DataCollection=CommonInverterData'

logging.basicConfig(filename='fronius_PAC.log',level=logging.WARNING)

def sendleistung():
    logging.debug("sendleistung erreicht")
    global vzip, uuid_gesamt, gesamtleistung
    f = urllib2.urlopen("http://" + vzip + "/middleware.php/data/" + uuid_gesamt + ".json?operation=add&value=" + gesamtleistung)
    logging.debug("Leistung: " + gesamtleistung + "W")
    time.sleep(1)
    print(gesamtleistung)

def checkleistung():
    logging.debug("checkleistung erreicht")
    global gesamtleistung, sendleistung
    if gesamtleistung > 100:
        sendleistung()
    else:
        gesamtleistung = str(0)
        sendleistung()
    time.sleep(10)

while True:
    logging.debug("While erreicht")
    try:
        data = json.load(urllib2.urlopen(froniusurl))
#    except:
#        checkleistung()
#    try:
        statuscode = data["Body"]["Data"]["DeviceStatus"]["StatusCode"]
        if statuscode == 7:
            gesamtleistung = str(data["Body"]["Data"]["PAC"]["Value"])
        else:
            gesamtleistung = str(0)
        sendleistung()
    except:
        logging.debug("exception erreicht")
        checkleistung()
