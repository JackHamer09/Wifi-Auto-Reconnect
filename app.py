import winwifi
import socket
import time
import json
import os.path
from os import path
from datetime import datetime

def is_connected():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(settings['no_internet_timeout'])
        sock.connect(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False

def disconnect():
    print("Disconnecting from WiFi", settings['wifi_name'])
    winwifi.WinWiFi.disconnect()

def connect():
    print("Connecting to WiFi", settings['wifi_name'])
    winwifi.WinWiFi.connect(settings['wifi_name'])
    print("Connected to WiFi", settings['wifi_name'], "and waiting 60 seconds to check for internet again.\n")
    time.sleep(60)

def reconnect():
    disconnect()
    connect()


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

with open('settings.json') as f:
    settings = json.load(f)


print("Checking connection on WiFi", settings['wifi_name'], "every", settings['check_internet_interval'], "seconds")
while True:
    if(is_connected()==False):
        print("\nConnection wasn't found at ", datetime.now().strftime("%H:%M:%S"))
        reconnect()
    time.sleep(settings['check_internet_interval'])