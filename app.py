""" import winwifi """
import socket
import time
import json
from os import path
from datetime import datetime
import subprocess

currentIP = 0
errors = 0

def is_connected():
    global currentIP
    global errors
    try:
        if(currentIP+1>len(upsArr)-1):
            currentIP = 0
        else:
            currentIP+=1
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(settings['no_internet_timeout'])
        sock.connect((upsArr[currentIP], 53))
        errors=0
        return True
    except OSError:
        pass
    print(getDateTime(),"No internet connection to ", upsArr[currentIP], " was found")
    if(errors+1>=2):
        errors=0
        return False
    errors+=1
    return True

def disconnect():
    print(getDateTime(), "Disconnecting from WiFi", settings['wifi_name'])
    """ winwifi.WinWiFi.disconnect() """
    subprocess.run("netsh wlan disconnect", capture_output=True, text=True, timeout=1).stdout
    print(getDateTime(), "Disconnected from WiFi", settings['wifi_name'])

def connect():
    print(getDateTime(), "Connecting to WiFi", settings['wifi_name'])
    """ winwifi.WinWiFi.connect(settings['wifi_name']) """
    cmd = "netsh wlan connect name={0} ssid={0}".format(settings['wifi_name'])
    subprocess.run(cmd, capture_output=True, text=True, timeout=1).stdout
    print(getDateTime(), "Connected to WiFi", settings['wifi_name'])

def reconnect():
    disconnect()
    connect()

def getDateTime():
    return datetime.now().strftime("%H:%M:%S")


if(path.exists('settings.json')==False):
    print('Type exact name of your WiFi:')
    userInput_wifiName = str(input())
    settingsFile = open('settings.json', 'a')
    settingsStr = '''{
    "wifi_name": "'''+userInput_wifiName+'''",
    "check_internet_interval": 3, 
    "no_internet_timeout": 3
}'''
    settingsFile.write(settingsStr)
    settingsFile.close()
    print('\n\nSettings file was created.\nTo change your WiFi name in the future go to settings.json in the program\'s directory and replace the current WiFi name with the new one.\n\n')

with open('cdn_list.json') as cdnFile:
    upsArr = json.load(cdnFile)
with open('settings.json') as f:
    settings = json.load(f)


print("\n\n")
print("Checking connection on WiFi", settings['wifi_name'], "every", settings['check_internet_interval'], "seconds", "\n\n")
while True:
    if(is_connected()==False):
        print("\n")
        print(getDateTime(),"Connection wasn't found")
        time1 = time.time()
        reconnect()
        print(getDateTime(), "Successfully reconnected to WiFi", settings['wifi_name'], "in ", (time.time()-time1), " seconds")
        print(getDateTime(), "Waiting 60 seconds to check for internet again.\n\n")
        time.sleep(60)
    time.sleep(settings['check_internet_interval'])
