# Indoor COVID-19 Social Distancing and Contact Tracing
A Project build using a Raspberry Pi 3, which makes use of MAC Addresses to identify people who might have come in contact with an infected person.

README:

The Code is divided into follwoing folders-

1) Room1 
2) Room2
3) System_Server

Room1
Room1 contains the code for Raspberry Pi for room 1. This room allows us to make the dummy entries using the mac_input file.
In addition to that it contains bulk_update, which updates the entries and checks the server for room occupancy.
There we also had a file called delete.py which clears all the fields of the Thingspeak Server for all entries and exits.
Room2 
Room2 is similiar to room 1 , but it runs by using actual MAC Addresses based on Devices connected.

System_Server

This is the actual Server where the data processing and updates happen using the data_collect file.
To send an email you would need to enter your Email and Password by making an edit into the program where SMTP is used in line 276.

This collects all the data from Thingspeak Server, and in addition to that sends back data about each room's occupancy. 
Also, it listens continously and whenever there is an update about User getting a positive report sends an email to all people who came in contact with that person.
Also there is an excel file which stores all the email ID's of people mapped with the MAC Address.

![Raspberry Pi Module](https://user-images.githubusercontent.com/54408300/109353182-fe571e00-7849-11eb-80d2-0dbbc07bbc9e.jpeg)
![Contact List of a User](https://user-images.githubusercontent.com/54408300/109353253-1e86dd00-784a-11eb-9027-ebb6dbf8f9f8.jpeg)
![Email Update](https://user-images.githubusercontent.com/54408300/109353078-db2c6e80-7849-11eb-8aac-66a05884ae07.jpeg)

