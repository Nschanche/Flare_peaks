import csv
###########################################################################
###########################################################################
#
def read_goes_file(directory):
	f = open('goes.csv', 'rt')
	rows = csv.reader(f, delimiter=',')
	
	counter=0
	
	for row in rows:
		if counter != 0: flare_info = row
		counter+=1
# goes_starttime, goes_peak_time, goes_x, goes_y goes_class 
			
	return(flare_info[1],flare_info[3],flare_info[6],flare_info[7],flare_info[5])