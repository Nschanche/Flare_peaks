"""
    Code to produce a list of GOES times from a CSV file and from those times 
    	create a file directory based on the event #. The program then makes a CSV
    	file with a single entry for an individual event.
"""


import csv
import os
###########################################################################
top_dir="/home/nschanch/Stat121/Nicole/"
file_name="/home/nschanch/Stat121/Nicole/goes_events.csv"
###########################################################################
###########################################################################

f = open(file_name, 'rt')
rows = csv.reader(f, delimiter=',')
counter=0

events=[]
for row in rows:	
#	print row
	if counter == 0: titles=row
	else:
		events.append(row)
	counter+=1
	
for event in events:
	working_dir=top_dir+'GOES_'+event[0]
	os.mkdir(working_dir, 0777)
	file = open(working_dir+'/goes.csv', 'wt')
	goes_file= csv.writer(file)
	goes_file.writerow(titles)
	goes_file.writerow(event)
	
	
	






