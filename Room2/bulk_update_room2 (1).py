import http.client
import urllib as ul
import urllib.request
import urllib3
import json
import time
import datetime
import os
import psutil
import csv
#import mac_input



writeAPIkeyentry = "VRLVOUVOQ4Q5TL1I" # Replace YOUR-CHANNEL-WRITEAPIKEY with your channel write API key
writeAPIkeyexit  = "XCADPV5H310NBZC0"
channelIDentry = "1247696" # Replace YOUR-CHANNELID with your channel ID
channelIDexit  = "1245307"

    
def new_entry(entry_user):
    
    string=entry_user.split("=")
    params = ul.parse.urlencode({'field1': string[0],'field2': string[1],'field3':"2",'key':writeAPIkeyentry }) 
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()       
        data = response.read()
        conn.close()
        return 1
    except:
        print("connection failed")
        
def new_exit(exit_user):
    string=exit_user.split("=")
    params = ul.parse.urlencode({'field1': string[0],'field2': string[1],'field3':"2",'key':writeAPIkeyexit }) 
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()       
        data = response.read()
        conn.close()
        return 1
    except:
        print("connection failed")

if __name__ == "__main__":  # To ensure that this is run directly and does not run when imported
    #mac_array=[]
    while(1):
        while(os.stat("entry.txt").st_size==0):
            pass
        f=open("entry.txt","r")
        writedata=f.read()
        f.close()
        choice=writedata[-1]
        writedata=writedata[:-1]
        if(choice=="1"):    
            new_entry(writedata)
        if(choice=="2"):
            new_exit(writedata)
        f=open("entry.txt","w")
        f.truncate(0)
        f.close()
        #print(mac_array)
    
        
    #mac_input.input_mac_update
    #new_entry(mac_address)
    
    '''
    while 1:
        # If update interval time has crossed 15 seconds update the message buffer with data
        if time.time() - lastUpdateTime >= updateInterval:
            
            updatesJson()
    '''
