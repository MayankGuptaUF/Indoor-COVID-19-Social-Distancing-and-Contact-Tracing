import datetime
import urllib.request
import json
channel_room  = "1250275"
read_occ ="POJZ8GDIVWDBVT5O"

global b
b=datetime.datetime.today().replace(microsecond=0)

def occupancy():
    
    conn = urllib.request.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                           % (channel_room,read_occ))

    response = conn.read()
    data=json.loads(response.decode('utf-8'))
    if(data!=-1):
        room1=int(data['field1'])
        conn.close()
        return room1
    else:
        return 0
    
if __name__ == "__main__":
    filename="new_mac_id.txt"
    while(1):
        input_mac=input("Enter MAC_Address: followed by entry1 or exit2 \n")
        d=str(datetime.datetime.today().replace(microsecond=0))
        a=datetime.datetime.today().replace(microsecond=0)
        entry=input_mac[:-1]+"="+d+input_mac[-1]
        room1=occupancy()
        c=a-b
        print(entry)
        if((input_mac[-1]!='1' and room1<5) and c.seconds<15):
            print("A person just entered or exited. Please wait 15 seconds before retrying to maintain social distancing guidelines")
        if((input_mac[-1]=='1' and room1>=5) or c.seconds<15):
            if(c.seconds<15):
                print("A person just entered or exited. Please wait 15 seconds before retrying to maintain social distancing guidelines")
            else:
                print("Room is currently at max capacity check the Thingsview app")
        else:
            fd=open(filename,"w")
            
            if(input_mac=='clear'):
                fd.truncate(0)
                fd.close()
                break
            
            fd.write(entry)
            fd.close()
            b=datetime.datetime.today().replace(microsecond=0)