"""
    Code to 
    	1. produce a list of AIA 171 flares based on GOES flare times 
    	2. Find the events closest in in time and space to the GOES flare
    	3. Produce a sub folder for each flare that meets the criteria
    	4. Make a human readable text file that contains the 	
    		a. Time of the flare peak in AIA
    		b. Coordinates of flare in AIA
    		c. Time difference, in seconds, between the peak in GOES and the peak in 
    			AIA.
    		 
    	 
"""

###########################################################################
#Import all of the modules necessary for main program and sub routines
import datetime
import time
import multiprocessing as mp
from sunpy.net import hek
import numpy
import csv
import os
###########################################################################
#Define system wide variables to run the main and sub-programs
# Paths used for main program and sub-programs.  
top_level_dir="/home/nschanch/Stat121/Nicole/"

#Time interval, +/-, around GOES peak time to search for AIA flares
delta_T=datetime.timedelta(minutes=5.)

#Spacial distance, in arcseconds, from the reported GOES location to search for 
# flares 
search_radius=5.

#Number of threads this code can use
n_threads=10

#AIA file name
AIA_file_name='AIA_171'
#AIA wavelength of interest
AIA_Wave='171'
#We are looking for flares
event_type='FL'
#Only choose Flare Detective triggers
source='Flare Detective - Trigger Module'

###########################################################################
#
#
#

###########################################################################
###########################################################################
#get_subdirs
#This program returns a list of all of the subdirectories in the given top
#	level directory.
#
def get_subdirs(top_dir):
	dir_list=[]
	print top_dir
	list=os.listdir(top_dir)
	print list
	for item in list:
		if os.path.isdir(top_dir+item) : dir_list.append(top_dir+item+'/')
		#print 'SPACE'
		#print(dir_list)
	
	return(dir_list)
###########################################################################
###########################################################################
#
def read_goes_file(directory):
	f = open(directory+'goes.csv', 'rt')
	rows = csv.reader(f, delimiter=',')
	
	counter=0
	
	for row in rows:
		if counter != 0: flare_info = row
		counter+=1
		
	
# goes_starttime, goes_peak_time, goes_x, goes_y goes_class 
	print flare_info
	return(flare_info[1],flare_info[3],flare_info[6],flare_info[7],flare_info[5])

###########################################################################
###########################################################################
#mk_AIA_171
#This program searches a directory for AIA_171 sub-directories.  If none are 
#  found, the code:
#	1. Creates an AIA 171 sub directory
#	2. Finds HEK flare events in 171 around the GOES event
#	3. Creates a human readable text file for each event that includes the 
#		following information.
#			a. Start time of flare
#			b. End time of flare
#			c. Peak time of flare
#			d. X location of flare
#			e. Y location of flare
#			f. Temporal distance between GOES flare and AIA flare
#			g. Spatial distance between GOES flare peak and AIA flare peak
def mk_AIA_171(directory):
	print('Here 3')
	print(directory)
		
	
#Get the peak time and postion of the GOES flare
	goes_list =read_goes_file(directory)
	goes_starttime=goes_list[0]
	goes_peak_time=goes_list[1]
	goes_x=goes_list[2]
	goes_y=goes_list[3]
	
#Define a search time based on the GOES peak time and the delta_T defined 
#	previously
	g_start=datetime.datetime.strptime(goes_starttime,"%Y/%m/%d %H:%M")
	start_time=(g_start-delta_T)
	
	end_time=(g_start+delta_T)
	
#Query the HEK for AIA 171 files
	client = hek.HEKClient()
	events= client.query(hek.attrs.Time(start_time.isoformat(),end_time.isoformat()),
		hek.attrs.EventType('FL'))
	
###########################################################################
#Eliminate all events except for Flare Detective events in the specified wavelength.
#There are better ways to do this than with two for loops.	
# 	counter=0
# 	for event in events:
# 		if event["obs_channelid"] != AIA_Wave :
# 			events.pop(counter)
# 		counter+=1
# 	
# 	counter=0						
# 	for event in events:			
# 		if event["frm_name"] != source :
# 			events.pop(counter)
# 		counter+=1

	counter=0
	good_events=[]
	for event in events:
		if event["obs_channelid"] == AIA_Wave and event["frm_name"] == source :
			good_events.append(events[counter])
		counter+=1
		
	events = good_events
		
###########################################################################
#Determine the spatial and temporal distance from the reported GOES flare and 
#	the flare detected by the Flare Detective.	
	distance=[]
	time_difference=[]		
	for event in events:
		dist=numpy.sqrt(((float(goes_x)-float(event["event_coord1"]))**2)+
			((float(goes_y)-float(event["event_coord2"]))**2))
		distance.append(dist)
		
		goes_peak_time_dt=datetime.datetime.strptime(goes_peak_time,
			"%Y/%m/%d %H:%M")
		event_peak_time_dt=datetime.datetime.strptime(event["event_peaktime"],
			"%Y-%m-%dT%H:%M:%S")
		t_diff=goes_peak_time_dt-event_peak_time_dt
		time_difference.append(t_diff.total_seconds())
		

###########################################################################		
#make a text file in the GOES Folder
#"event_starttime"
#"event_endtime"
#"event_peaktime"
#"event_coord1"
#"event_coord2"
	text_file=open(os.path.join(directory, AIA_file_name+'.csv'), 'w')	
# 	counter=0
# 	for event in events:
# 		text_file.write(event['event_starttime'])
# 		text_file.write(', ')
# 		text_file.write(event['event_endtime'])
# 		text_file.write(', ')
# 		text_file.write(event['event_peaktime'])
# 		text_file.write(', ')
# 		text_file.write(str(event['event_coord1']))
# 		text_file.write(', ')
# 		text_file.write(str(event['event_coord2']))
# 		text_file.write(', ')
# 		text_file.write(str(time_difference[counter]))
# 		text_file.write(', ')
# 		text_file.write(str(distance[counter]))
# 		text_file.write('\n')
# 		counter+=1

	if len(time_difference)>0:
		closest_time_loc = time_difference.index(min(time_difference))

		event = events[closest_time_loc]
	
		text_file.write(event['event_starttime'])
		text_file.write(', ')
		text_file.write(event['event_endtime'])
		text_file.write(', ')
		text_file.write(event['event_peaktime'])
		text_file.write(', ')
		text_file.write(str(event['event_coord1']))
		text_file.write(', ')
		text_file.write(str(event['event_coord2']))
		text_file.write(', ')
		text_file.write(str(time_difference[closest_time_loc]))
		text_file.write(', ')
		text_file.write(str(distance[closest_time_loc]))
		text_file.write('\n')
    	
		text_file.close()


	
	

###########################################################################
###########################################################################
#Main
#mk_171_list

######################################################################
#Search for sub-directories

#Create the list to hold the GOES directories' paths
GOES_dirs=get_subdirs(top_level_dir)
print('Here1')
print('Here2')

	 
######################################################################
#If there are any GOES directories then proceed.
#For each sub-directory, initiate a thread to search for AIA_171 entries
#Create the multi-processing pool
po=mp.Pool(n_threads)
for  directory in GOES_dirs:
	print('Here2a')
	mk_AIA_171(directory)
    
######################################################################

#End





