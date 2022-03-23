# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 21:02:30 2021

@author: Nathaniel
"""

import socket
import json
import pymongo
import threading
from time import sleep

def connectToDatabase():
    # Connect to you cluster
    userName = "<InsertUserName"
    password = "<InsertPassword>"
    clusterName = "<InsertCluster>"
    # Connect to you cluster
    return pymongo.MongoClient("mongodb+srv://" + userName + ":" + password + "!tt8P@" + clusterName + ".upsgi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    

"""
Method for recieving data from a client and storing it in database
"""
def receiveDataConnection():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind((socket.gethostname(), 5432))
    tcp.listen(5)
    
    while True:
        clientsocket, adress = tcp.accept()
        
        # Connect to you cluster
        client = connectToDatabase()
    
        # Create a new database in your cluster
        db = client.weatherData
        
        # Create a new collection in you database
        dataCollection = db.dataCollection
        
        data = {}
        while True:
            msg = clientsocket.recv(160) #Recieves message from client
                
            data = json.loads(msg.decode('utf-8')) #Decodes message from client
            dataCollection.insert_one(data) #Insert into database
            
  
          
"""
Method for retrieving data from database and sending it to client
"""             
def retrieveDataConnection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connection_adress = (socket.gethostname(), 5431)
    sock.bind(connection_adress)
    
    while True:
        data, address = sock.recvfrom(4096)
            
        # Connect to you cluster
        client = connectToDatabase()
        
        # Find database
        db = client["weatherData"]
        
        # Find correct collection
        dataCollection = db["dataCollection"]
        data = dataCollection.find({},{ "_id": 0 })
        
        length = data.count()
        sock.sendto(str(length).encode("utf-8"), address)
        
        for i in data:
            toSend = json.dumps(i).encode("utf-8")
            sock.sendto(toSend, address)
 
       
receive = threading.Thread(target=receiveDataConnection)
retrieve = threading.Thread(target=retrieveDataConnection)

receive.start()
retrieve.start()