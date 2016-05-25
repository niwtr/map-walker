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
    cordict={1:(364, 444), 
             2:(447, 278),
             3:(555, 405), 
             4:(612, 161), 
             5:(719, 160), 
             6:(713, 262),
             7:(862, 181),
             8:(774, 558),
             9:(428, 788),
             10:(100, 834)}
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
        if(first_time):
            minita=(last_start_time.minute+last_travel_time.minute)//60 
            if(last_start_time.hour+last_travel_time.hour+minita>24): #overnight
                hop[7].day+=1
        last_start_time=hop[7]
        last_travel_time=hop[4]
        first_time=False

def dtoi(datime):
    return datime.minute+datime.hour*60+datime.day*3600

def trace(cur_time, pathl):  #curtime should be int.
    curtime=cur_time
    
    for [source, destination, num,
         mode,travel_time, distance, 
         price, start_time] in pathl:
        if(curtime<dtoi(start_time)): #we are waiting in the bus station. the start_time is morphed into integer.
            return calc_cur_cord(source, destination, 0)
        if(curtime<dtoi(start_time)+travel_time):
            tperc=(curtime-dtoi(start_time))/travel_time
            return calc_cur_cord(source, destination, tperc)
        else : #curtime>start_time+travel_time. this implies we are on next hop.
            curtime=curtime+travel_time
    
database=database_binding()
rt=router_module(0, database)
trace(1,translata(rt.minimal_time_path(1, [2,3,4])))





