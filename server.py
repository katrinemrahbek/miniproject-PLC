#!/usr/bin/python3         
import socket  
import csv    
import xml.sax


# csv file name 
filename = "procssing_times_table.csv"
rows = [] 
array2D = []

# reading csv file 
with open(filename, 'r') as csvfile: 
   
   csvreader = csv.reader(csvfile) 
   
   for row in csvreader: 
      rows.append(row) 
   for row in rows:
      array2D.append(row[0].split(";")) 

def cvshandling(station, carrier):
   return array2D[carrier][station]

def filehandler(data):
   f = open("carrierfile.xml", "w")
   f.write(data)
   f.close

class carrierHandler(xml.sax.ContentHandler):
   def __init__(self):
      self.CurrentData = ""
      self.carrierID = ""
      
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      if tag =="carrierID":
         print("---carrier---")
      if tag =="station":
         print("___station___")
         stationID = attributes["id"]
         print("station ID = ", stationID)

   def endElement(self, tag):
      if self.CurrentData == "carrierID":
         print("ID = ", self.carrierID)
      self.CurrentData = ""

   def characters(self, content):
      if self.CurrentData == "carrierID":
         self.carrierID =content
   

parser =xml.sax.make_parser()
Handler = carrierHandler()
parser.setContentHandler(Handler)



# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = '127.0.0.1'                         

port = 9999                                           

# bind to the port
serversocket.bind((host, port))  
print("server ready")                                

      

while True:
   # server listen
   serversocket.listen()     
                           
   # establish a connection
   clientsocket, addr = serversocket.accept()      

   print("Got a connection from %s" % str(addr))
   msg = clientsocket.recv(2024)
   data = msg.decode('utf-8')

   filehandler(data)
   
   parser.parse("carrierfile.xml")
   processing_time=cvshandling(5, int(Handler.carrierID))
   print("\nprocessing_time: ", processing_time)
   
   clientsocket.send(processing_time.encode())
   clientsocket.close()

