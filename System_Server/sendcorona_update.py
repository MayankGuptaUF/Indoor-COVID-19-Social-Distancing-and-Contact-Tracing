import http.client
import urllib as ul
import urllib3
import json
import time
import datetime
import os



writeAPIkey="1995JMUIIF6P488K"
def corona_to_db(entry_user):
    
	params = ul.parse.urlencode({'field1': entry_user,'key':writeAPIkey }) 
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
		input_pos=input("Enter MAC_Address of positive person\n")
		corona_to_db(input_pos)
	
