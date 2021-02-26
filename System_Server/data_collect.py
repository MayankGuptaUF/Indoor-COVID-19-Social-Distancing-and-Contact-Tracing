#!/usr/bin/env python
import urllib.request,json
import datetime
import requests
import xlrd
import smtplib
import http
import email.utils
from email.mime.text import MIMEText

Readkeyentry = 'Z9983R52J9A6QDWF'
Readkeyexit  = '9V4AZCGZ1ZNEJ9MZ'
Readkeycorona = 'EKZFB2CRXCMAS07T'
Writekeyocc  = 'FGKJ8XKK7UAJU8XN'
CHANNEL_IDentry = "1247696"
CHANNEL_IDexit  = "1245307"
CHANNEL_IDcorona = "1211686"
mydata={}
mydata['api_key']= "NZBN9O93DSAI7U8B"
global dictkeyroom1
dictkeyroom1={}
global dictkeyroom2
dictkeyroom2={}

global positive_list
positive_list=[]

def entry():
	conn = urllib.request.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" % (CHANNEL_IDentry,Readkeyentry))
	response = conn.read()
	#print("http status code=%s" % (conn.getcode()))
	data=json.loads(response.decode('utf-8'))
	conn.close()
	if(data!=-1):
		if(data['field3']=='1'):
			if(data['field1'] not in dictkeyroom1):
				dictkeyroom1[data['field1']]=[data['field2']]
				print("new entry1")				
				print(dictkeyroom1)
				occupancy()
			if(data['field1'] in dictkeyroom1 and data['field2'] not in dictkeyroom1[data['field1']]):
				dictkeyroom1[data['field1']].append(data['field2'])
				print("new entry append1")
				print(dictkeyroom1)
				occupancy()
		if(data['field3']=='2'):
			if(data['field1'] not in dictkeyroom2):
				dictkeyroom2[data['field1']]=[data['field2']]
				print("new entry2")
				print(dictkeyroom2)
				occupancy()
			if(data['field1'] in dictkeyroom2 and data['field2'] not in dictkeyroom2[data['field1']]):
				dictkeyroom2[data['field1']].append(data['field2'])
				print("new entry append 2")
				print(dictkeyroom2)
				occupancy()
def exit():
	conn = urllib.request.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" % (CHANNEL_IDexit,Readkeyexit))
	response = conn.read()
	#print("http status code=%s" % (conn.getcode()))
	data=json.loads(response.decode('utf-8'))
	conn.close()
	if(data!=-1):
		if(data['field3']=='1'):
			if(data['field1'] not in dictkeyroom1):
				dictkeyroom1[data['field1']]=[data['field2']]
				print("new exit1")
				print(dictkeyroom1)
				occupancy()
			if(data['field1'] in dictkeyroom1 and data['field2'] not in dictkeyroom1[data['field1']]):
				dictkeyroom1[data['field1']].append(data['field2'])
				print("new exit append 1")
				print(dictkeyroom1)
				occupancy()
		if(data['field3']=='2'):
			if(data['field1'] not in dictkeyroom2):
				dictkeyroom2[data['field1']]=[data['field2']]
				print("new exit 2")
				print(dictkeyroom2)
				occupancy()
			if(data['field1'] in dictkeyroom2 and data['field2'] not in dictkeyroom2[data['field1']]):
				dictkeyroom2[data['field1']].append(data['field2'])
				print("new exit append 2")
				print(dictkeyroom2)
				occupancy()

def corona_positive():
	conn = urllib.request.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" % (CHANNEL_IDcorona,Readkeycorona))
	response = conn.read()
	#print("http status code=%s" % (conn.getcode()))
	data=json.loads(response.decode('utf-8'))
	conn.close()
	if(data!=-1):
		
		if(data['field1'] not in positive_list):
			check_room1(data['field1'])
			check_room2(data['field1'])
			print(positive_list)
			r=requests.delete("https://api.thingspeak.com/channels/1211686/feeds",params=mydata)
			if(len(positive_list)!=0):
				send_email()
					
def check_room1(mac_address):
	
	if(mac_address in dictkeyroom1):
			infected=dictkeyroom1[mac_address]
			if(len(infected)%2!=0):
				now = datetime.datetime.today().replace(microsecond=0)
				infected.append(str(now))
	
			
	else:
		return
	
	if(len(infected)>1):
		for i in range(0,len(infected),2):
			
			old_mac=[]
			cen=datetime.datetime.strptime(infected[i],'%Y-%m-%d %H:%M:%S')
			cex=datetime.datetime.strptime(infected[i+1],'%Y-%m-%d %H:%M:%S')
			ellapse=datetime.datetime.today().replace(microsecond=0)-datetime.timedelta(days=14)
			stale=0
			if(ellapse>cen or ellapse>cex):
				remove1=infected[i]
				remove2=infected[i+1]
				old_mac.append(remove1)
				old_mac.append(remove2)
				stale=1

			for key in dictkeyroom1:
				old_entry=[]
				if(key!=mac_address and key not in positive_list and stale==0):
					timevic=dictkeyroom1[key]
					
					if(len(timevic)%2!=0):
						now = datetime.datetime.today().replace(microsecond=0)
						timevic.append(str(now))
					for i in range(0,len(timevic),2):
						nen=datetime.datetime.strptime(timevic[i],'%Y-%m-%d %H:%M:%S')
						nex=datetime.datetime.strptime(timevic[i+1],'%Y-%m-%d %H:%M:%S')
						test_short=nen>cex
						ellapse_vic=datetime.datetime.today().replace(microsecond=0)-datetime.timedelta(days=14)
						stale_vic=0
						if(ellapse_vic>nen or ellapse_vic>nex):
							remove_vic1=timevic[i]
							remove_vic2=timevic[i+1]
							old_entry.append(remove_vic1)
							old_entry.append(remove_vic2)
							stale_vic=1
						if(test_short is True):
							break
						
						test1=nen>cen and cex>=nex
						test2=cen>nen and nex>=cex
						test3=cen>nen and cex>=nex
						test4=nen>cen and nex>cen
						if(((test1 or test2 or test3 or test4)==True) and stale_vic==0):
							if(key not in positive_list):
								
								positive_list.append(key)
							break
			if(len(old_entry)!=0):
				k=dictkeyroom1[key]
				for i in range(len(old_entry)):
					if(old_entry[i] in k):
						k.remove(old_entry[i])
				dictkeyroom1.pop(key)
				if(len(k)>0):
					dictkeyroom1[key]=k
		if(len(old_mac)!=0):
				m=dictkeyroom1[mac_address]
				for i in range(len(old_mac)):
					if(old_mac[i] in m):
						m.remove(old_mac[i])
					
				dictkeyroom1.pop(mac_address)
				if(len(m)>0):
					dictkeyroom1[mac_address]=m
						
		print(positive_list)
		
		

def check_room2(mac_address):
	if(mac_address in dictkeyroom2):
			infected=dictkeyroom2[mac_address]
			if(len(infected)%2!=0):
				now = datetime.datetime.today().replace(microsecond=0)
				infected.append(str(now))
	
			
	else:
		return
	
	if(len(infected)>1):
		for i in range(0,len(infected),2):
			
			old_mac=[]
			cen=datetime.datetime.strptime(infected[i],'%Y-%m-%d %H:%M:%S')
			cex=datetime.datetime.strptime(infected[i+1],'%Y-%m-%d %H:%M:%S')
			ellapse=datetime.datetime.today().replace(microsecond=0)-datetime.timedelta(days=14)
			stale=0
			if(ellapse>cen or ellapse>cex):
				remove1=infected[i]
				remove2=infected[i+1]
				old_mac.append(remove1)
				old_mac.append(remove2)
				stale=1

			for key in dictkeyroom2:
				old_entry=[]
				if(key!=mac_address and key not in positive_list and stale==0):
					timevic=dictkeyroom2[key]
					
					if(len(timevic)%2!=0):
						now = datetime.datetime.today().replace(microsecond=0)
						timevic.append(str(now))
					for i in range(0,len(timevic),2):
						nen=datetime.datetime.strptime(timevic[i],'%Y-%m-%d %H:%M:%S')
						nex=datetime.datetime.strptime(timevic[i+1],'%Y-%m-%d %H:%M:%S')
						test_short=nen>cex
						ellapse_vic=datetime.datetime.today().replace(microsecond=0)-datetime.timedelta(days=14)
						stale_vic=0
						if(ellapse_vic>nen or ellapse_vic>nex):
							remove_vic1=timevic[i]
							remove_vic2=timevic[i+1]
							old_entry.append(remove_vic1)
							old_entry.append(remove_vic2)
							stale_vic=1
						if(test_short is True):
							break
						
						test1=nen>cen and cex>=nex
						test2=cen>nen and nex>=cex
						test3=cen>nen and cex>=nex
						test4=nen>cen and nex>cen
						if(((test1 or test2 or test3 or test4)==True) and stale_vic==0):
							if(key not in positive_list):
								
								positive_list.append(key)
							break
			if(len(old_entry)!=0):
				k=dictkeyroom2[key]
				for i in range(len(old_entry)):
					if(old_entry[i] in k):
						k.remove(old_entry[i])
				dictkeyroom2.pop(key)
				if(len(k)>0):
					dictkeyroom2[key]=k
		if(len(old_mac)!=0):
				m=dictkeyroom2[mac_address]
				for i in range(len(old_mac)):
					if(old_mac[i] in m):
						m.remove(old_mac[i])
					
				dictkeyroom2.pop(mac_address)
				if(len(m)>0):
					dictkeyroom2[mac_address]=m
						
		print(positive_list)
def send_email():
	
	loc = ("Untitled.xlsx")
	email_list=[]
	wb = xlrd.open_workbook(loc)
	sheet = wb.sheet_by_index(0)

	for i in range(sheet.nrows):
		if(sheet.cell_value(i, 0) in positive_list):
			email_list.append(sheet.cell_value(i,1))
	TO = ','.join(email_list)
	
	if(TO!=''):
		s = smtplib.SMTP('smtp.gmail.com', 587)
		s.starttls()
		s.login("ENTER YOUR EMAIL", "ENTER YOUR PASSWORD")
		message = "You have been in close contact with a person who tested positive for COVID-19.Visit CDC website at https://www.cdc.gov/coronavirus/2019-ncov/if-you-are-sick/quarantine.html"
		msg = MIMEText(message)
		k=datetime.datetime.now().replace(microsecond=0,second=0)
		msg['Subject'] = 'Urgent:COVID-19 Update at '+str(k)[5:-3]
		s.sendmail("mayankuf@gmail.com", TO.split(",") , msg.as_string())
				
		s.quit()

def occupancy():
	
	countroom1=0
	countroom2=0
	for key, value in dictkeyroom1.items():
		if(len(value)%2!=0):
			countroom1=countroom1+1
	for key, value in dictkeyroom2.items():
		if(len(value)%2!=0):
			countroom2=countroom2+1
	print(countroom1,countroom2)
	params = urllib.parse.urlencode({'field1': countroom1,'field2':countroom2,'key':Writekeyocc }) 
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
if __name__ == '__main__':
	
	while(1):
		entry()
		exit()
		corona_positive()
	
	
	

