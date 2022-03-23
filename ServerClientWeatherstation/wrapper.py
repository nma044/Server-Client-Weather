# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 21:22:52 2021

@author: Nathaniel
"""

#client 

from time import sleep
from station import StationSimulator
import socket 
import json

if __name__ == "__main__":
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection_adress = (socket.gethostname(), 5432) 
    sock.connect(connection_adress)
        
    
    bergen_station = StationSimulator(simulation_interval=1)
    bergen_station.turn_on()
    
    
    for _ in range(72):
        sleep(1)
        
        message = {"location" : bergen_station.location,
                   "month" : bergen_station.month,
                   "temp" : bergen_station.temperature,
                   "rain" : bergen_station.rain
                   }
        
        print(message)
        toSend = json.dumps(message).encode("utf-8") #Enkoder dict til bytes
        sock.sendall(toSend) #Sender til server
    
        
    bergen_station.shut_down()


