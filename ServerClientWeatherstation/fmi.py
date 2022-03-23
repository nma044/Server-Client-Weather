# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 15:10:02 2021

@author: Nathaniel
"""

from tkinter import *

import socket

import json 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
connection_adress = (socket.gethostname(), 5431) 
sock.connect(connection_adress)
            
data = []

message = "connection to storage"
sock.sendto(message.encode("utf-8"), connection_adress)

sizeOfMessage = sock.recv(100).decode("utf-8")
print("Number of elements: " + sizeOfMessage)
sizeOfMessage = int(sizeOfMessage) #Number of how many dictionaries that gets sent from the database

for i in range(sizeOfMessage):
    msg = sock.recv(1600)
    data.append(json.loads(msg.decode('utf-8'))) #Decodes and ads the dictionaries to a data-list
    print(msg.decode('utf-8')) #Printing all of the dictionaries to the terminal, see ReadME




root = Tk() #Tkninter
root.resizable(height = None, width = None)

"""
Method for printing data from storage to the GUI
"""
def printDataFromStorage(dataList):
    height = 5
    width = 4
    
    headerList = dataList
    
    for i in range(len(headerList)): #Printing the header of the data
        Label(root, text = headerList[i]).grid(row=3, column=i)
        headerList[i] = headerList[i].upper() #Makes the items in the list upper so they can be compared later
    
    
    labelVar = StringVar()
    
    counter = 0 #Counter for the rows
    
    for i in data:
        dictOfDataList = i #One dictionary
        
        j = 0
        
        for key, value in dictOfDataList.items():            
            if key.upper() in headerList:         
                if key == "location":
                    l = Label(root, text=dictOfDataList.get(key))
                    l.grid(row=counter+4, column=j)
                    j+=1
                            
                if key == "month":
                    l = Label(root, text=dictOfDataList.get(key))
                    l.grid(row=counter+4, column=j)
                    j+=1
                            
                if key == "temp":
                    l = Label(root, text=dictOfDataList.get(key))
                    l.grid(row=counter+4, column=j)
                    j+=1
                            
                if key == "rain":
                    l = Label(root, text=dictOfDataList.get(key))
                    l.grid(row=counter+4, column=j)
                    
        counter+=1

"""
Method that gets called when the button is pressed
Calls printDataFromStorage with the data thats going to be printed
"""
def sendButton():
    if(cbv1.get()==0 and cbv2.get()==0 and cbv3.get()==0 and cbv4.get()==0): #Checking that some buttons were checked 
        infoLabelText = StringVar()
        infoLabel = Label(root, textvariable = infoLabelText, pady=15, font=("Arial", 10))
        infoLabel.grid(row=3, columnspan=5)
        
        print("No buttons checked")
        infoLabelText.set("No options were requested")
        
    else:
        print("Checked")
        dataDict = {"Location": cbv1.get(), #Cbv: checkButtonValue, 0 if not checked and 1 if checked
                    "Month": cbv2.get(),
                    "Temp": cbv3.get(),
                    "Rain": cbv4.get()
                    }
        
        dataToRequest = []
        
        for key, value in dataDict.items(): #Adds the key that was checked in the checkboxes
            if value!=0:
                dataToRequest.append(key)
            

        print("-------")
        print(dataToRequest)
        printDataFromStorage(dataToRequest)

Label(text = "FMI storage-management", pady=15, font=("Arial", 20)).grid(row=0, columnspan=5)
Label(text = "A GUI for retriving data from the storage", pady=15, font=("Arial", 11)).grid(row=1, columnspan=5)

cbv1 = IntVar()
cbv2 = IntVar()
cbv3 = IntVar()
cbv4 = IntVar()

Checkbutton(root, text="Location", variable=cbv1).grid(row=2, column=0)
Checkbutton(root, text="Month", variable=cbv2).grid(row=2, column=1)
Checkbutton(root, text="Temp", variable=cbv3).grid(row=2, column=2)
Checkbutton(root, text="Rain", variable=cbv4).grid(row=2, column=3)


Button(root, text = "Request data", pady=10, command=sendButton, bg="grey").grid(row=2, column=4)


root.mainloop()