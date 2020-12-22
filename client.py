#!/usr/bin/python3           # This is client.py file

import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
#host = '192.168.0.9'  
host = '127.0.0.1'                       

port = 9999

# connection to hostname on the port.
s.connect((host, port))                               
s.sendall(b'<station id = "5"><carrierID>7</carrierID></station>')
#s.sendall(b'<carrierID>7</carrierID>')

# Receive no more than 1024 bytes
msg = s.recv(2024)                                     

s.close()
print (msg.decode('ascii'))