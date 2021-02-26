import json
import requests
mydata={}
mydata['api_key']= "NZBN9O93DSAI7U8B"
r=requests.delete("https://api.thingspeak.com/channels/1247696/feeds",params=mydata)
r2=requests.delete("https://api.thingspeak.com/channels/1245307/feeds",params=mydata)
