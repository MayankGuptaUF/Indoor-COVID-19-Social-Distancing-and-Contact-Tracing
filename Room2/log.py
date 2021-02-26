from datetime import datetime

if __name__ == '__main__':
    list_of_devices = ['44:18:fd:6c:a7:86','7c:ab:60:a6:a1:08']
    entry_list = []
    exit_list = []
    logfile = open("/var/lib/misc/dnsmasq.leases","r")
    entry_open = open("entry.txt","w")
    #exit_open = open("exit.txt","w")
    loglines = logfile.readlines()
    for line in loglines:
        mac = line.split()
        entry_list.append(mac[1])
        
    for _ in list_of_devices:
        if _ in entry_list:
            now = datetime.now()
            entry_open.write(_)
            entry_open.write("=")
            entry_open.write(now.strftime("%Y-%m-%d %H:%M:%S"))
            #entry_open.write(" ")
            entry_open.write("1")
            #entry_open.write("\n")
            
        else:
            now = datetime.now()
            entry_open.write(_)
            entry_open.write("=")
            entry_open.write(now.strftime("%Y-%m-%d %H:%M:%S"))
            #entry_open.write(" ")
            entry_open.write("2")
            entry_open.write("\n")
        
        