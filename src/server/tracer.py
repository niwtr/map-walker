#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
Tracer module.

Making travel simulation.
'''


import mailer
import log
import datetime
from router import router_module
from datab import database_binding

def get_coordinate(cityid):
    cordict={0:(364, 444), 
             1:(447, 278),
             2:(555, 405), 
             3:(612, 161), 
             4:(719, 160), 
             5:(713, 262),
             6:(862, 181),
             7:(774, 558),
             8:(428, 788),
             9:(100, 834)}
    return cordict[cityid]



'''
Get the path we need.
'''
def get_path(path):
    pass

#translates the original path list of objects into path list of lists.
def translata(raw_pathl):
    acc=[]
    for obj in raw_pathl:
        acc.append([obj.source, obj.destination,
                    obj.num,obj.mode, obj.travel_time,
                    obj.distance, obj.price, obj.start_time])
    return acc
    

'''
Traveling simulation.
'''
def calc_cur_cord(source, dest, timepercent):
    sx=get_coordinate(source)[0]
    sy=get_coordinate(source)[1]
    dx=get_coordinate(dest)[0]
    dy=get_coordinate(dest)[1]
    return [
        sx+(dx-sx)*timepercent,
        sy+(dy-sy)*timepercent
    ]

''' [source, destination, num,
         mode,travel_time, distance, 
         price, start_time]'''

    
def datetime_modifier(pathl):
    last_start_time=datetime.datetime
    last_travel_time=datetime.datetime
    first_time=True   #in the first time we should not modify the date, see it as a principle
    for hop in pathl:
        if(not first_time):
            if(hop[7].hour<last_start_time.hour): #overnight
                date=hop[7]
                hour=date.hour
                day=date.day+1
                minute=date.minute
                year=date.year
                month=date.month
                hop[7]=datetime.datetime(year, month, day,hour,minute)
        last_start_time=hop[7]
        last_travel_time=hop[4]
        first_time=False

def total_time(pathl):
    pathl=translata(pathl)
    dest=pathl[-1][1]
    acc=0
    xtime=0
    last_start_time=0
    first_run=True
    for [source, destination, num,
         mode,travel_time, distance, 
         price, start_time] in pathl:    
        start_time=dtoi(start_time)
        
        if(first_run):
            xtime=start_time
            first_start_time=start_time
            acc+=travel_time
            first_run=False
        else:
            if(destination!=dest):
                acc+=start_time-last_start_time
            acc+=travel_time
            last_start_time=start_time
    return acc+xtime
        

def dtoi(datime):
#    print("day: ",datime.day, "hour: ",datime.hour, "minute: ",datime.minute )
    return datime.minute+datime.hour*60+datime.day*3600

def trace(cur_time, pathl):  #curtime should be int.
   
    curtime=cur_time
    datetime_modifier(pathl)
    for [source, destination, num,
         mode,travel_time, distance, 
         price, start_time] in pathl:
        
        start_time=dtoi(start_time)
        '''
        print("cur_time: " ,end='')
        print(curtime)
        print("start time: ", end='')
        print (start_time)
        print("travel time: ", end='')
        print(travel_time)
        print("")
        '''
        print(start_time)
        if(curtime<start_time): #we are waiting in the bus station. the start_time is morphed into integer.
            return calc_cur_cord(source, destination, 0)
        if(curtime<=start_time+travel_time):
            tperc=(curtime-start_time)/travel_time
            return calc_cur_cord(source, destination, tperc)
        
        else : #curtime>start_time+travel_time. this implies we are on next hop.
            curtime=curtime+travel_time
    
    
database=database_binding()
rt=router_module(0, database)

for obj in rt.minimal_time_path(1, [2,3,4]):
    print(obj.source, obj.destination, obj.mode, dtoi(obj.start_time))

#for i in range (4320, 8000, 10):
#    print(trace(i,translata(rt.minimal_time_path(1, [2,3,4]))))

print(total_time(rt.minimal_time_path(1, [2,3,4])))



