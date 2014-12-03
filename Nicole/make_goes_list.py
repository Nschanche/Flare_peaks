"""
    Code to produce a list of GOES times and from those times create a file directory.
"""


import csv
import os
###########################################################################
top_dir="/Users/hwinter/programs/git_folder/Nicole/"
file_name="/Users/hwinter/programs/git_folder/Nicole/goes_events.csv"
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
	
	
	






