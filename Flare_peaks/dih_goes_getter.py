import sunpy
import sunpy.instr.goes
import numpy as np
import sunpy.time.timerange

def dih_goes_getter(begintime,endtime):
    test1 = sunpy.time.is_time(begintime)
    test2 = sunpy.time.is_time(endtime)
    if test1 and test2:
        print "good times brah!"
        time_range = sunpy.time.timerange.TimeRange(begintime,endtime)
    else:
        print "Those are bad times sir!"
    eventlist = sunpy.instr.goes.get_goes_event_list(time_range)
    return eventlist