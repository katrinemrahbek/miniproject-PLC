#!/usr/bin/python3         
import socket  
import csv    
import xml.sax


# csv filename and initialize arrays
filename = "procssing_times_table.csv"
rows = [] 
array2D = []

# reading csv file 
with open(filename, 'r') as csvfile: 
   
   csvreader = csv.reader(csvfile) 
   # Seperating the different elements in the csv file
   for row in csvreader: 
      rows.append(row) 
   for row in rows:
      array2D.append(row[0].split(";")) 

# Finding the process time by the station ID and the carrier ID
def cvshandling(station, carrier):
   return array2D[carrier][station]

# Writes the xml string in a file
def filehandler(data):
   f = open("carrierfile.xml", "w")
   f.write(data)
   f.close

# Parses the xml string
class carrierHandler(xml.sax.ContentHandler):
   def __init__(self):
      self.CurrentData = ""
      self.carrierID = ""
      
   def startElement(self, tag, attributes): # is called at the start of a element
      self.CurrentData = tag
      if tag =="carrierID":
         print("---carrier---")
      if tag =="station":
         print("___station___")
         stationID = attributes["id"]
         print("station ID = ", stationID)

   def endElement(self, tag):   # is called at the end of a element
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
#host = '127.0.0.1'   

# the host and port name
host = '172.20.66.112'                      
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
   
   # recieve a message
   msg = clientsocket.recv(2024)
   data = msg.decode('utf-8')

   # put it into a file
   filehandler(data)
   
   # parsing the XML file 
   parser.parse("carrierfile.xml")

   # getting the processing time for the carrier at this station
   processing_time=cvshandling(5, int(Handler.carrierID))
   print("\nprocessing_time: ", processing_time)
   
   # sends processing time 
   clientsocket.send(processing_time.encode())
   
   #close socket
   clientsocket.close()

