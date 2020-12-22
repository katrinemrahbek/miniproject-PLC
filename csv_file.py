import csv
  
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

        
    