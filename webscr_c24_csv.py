import csv

teksts = ("Žēburs", "čž")

with open("out.csv", 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    for row in teksts:
        srow = []
        for e in row:           
            srow.append(e.encode('utf-8'))      
        writer.writerows(srow)
