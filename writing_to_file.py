#!/usr/bin/python3   


f = open("myfile.xml", "w")
f.write("<helleooo world!>")
f.close

f = open("myfile.xml", "r")
print(f.read())