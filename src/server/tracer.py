#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
################################################################################
Tracer module.

Making travel simulation.
################################################################################
'''


import mailer
import log
import datetime
import copy
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

day_weight=1440
hour_weight=60
minute_weight=1


#translates the original path list of objects into path list of lists.
'''
Translate the raw path list (contain objects as element.) to the path list matrix.
This mechanism is used for word transmission.
'''
def translata(raw_pathl):    
    acc=[]
    dtoi=lambda datime:datime.minute+datime.hour*hour_weight+datime.day*day_weight
    
    for obj in raw_pathl:
        acc.append([obj.source, obj.destination,
                    obj.num,obj.mode, obj.travel_time,
                    obj.distance, obj.price, dtoi(obj.start_time)])

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
        round(sx+(dx-sx)*timepercent, 2),
        round(sy+(dy-sy)*timepercent, 2)
    ]

''' [source, destination, num,
         mode,travel_time, distance, 
         price, start_time]'''

def _add_day(datime, day):   #old implementation.
    date=datime
    hour=date.hour
    day=date.day+day
    minute=date.minute
    year=date.year
    month=date.month
    datime=datetime.datetime(year, month, day,hour,minute)    
    return datime

def add_day(datime, day):
    datime+=day*day_weight
    return datime
    
def datetime_modifier(pathl):
    last_start_time=[]#datetime.datetime
    last_travel_time=[]#datetime.datetime
    day_plus=0 #day increasement.
    first_time=True   #in the first time we should not modify the date, see it as a principle
    for hop in pathl:
        if(not first_time):
            #if(hop[7].hour<last_start_time.hour): #overnight #old implementation
            if((hop[7]%day_weight)<=(last_start_time%day_weight)):   #overnight.
                day_plus+=1
        hop[7]=add_day(hop[7], day_plus)
        last_start_time=hop[7]
        last_travel_time=hop[4]
        first_time=False




class tracer_module():
    
    def calc_end_time(self, *pathl): #calculate the total time for a path list.
    #    pathl=translata(pathl)
        pathu=copy.deepcopy(pathl)
        datetime_modifier(pathu)
        dest=pathu[-1][1]
        acc=0
        for [source, destination, num,
             mode,travel_time, distance, 
             price, start_time] in pathu:    
            #start_time=dtoi(start_time)     #old implementation.
            if(destination==dest):
                acc+=start_time+travel_time
        return acc
    
    def calc_start_time(self, *pathl):
        #pathl=translata(pathl)
        return pathl[0][7]
    

    
    def trace(self, cur_time, pathl):  #curtime should be int.
        pathu=copy.deepcopy(pathl)
        curtime=cur_time
        datetime_modifier(pathu)
    
        for [source, destination, num,
             mode,travel_time, distance, 
             price, start_time] in pathu:
            
            #start_time=dtoi(start_time)   #old implementation.
            '''
            #test:
            print("cur_time: " ,end='')
            print(curtime)
            print("start time: ", end='')
            print (start_time)
            print("travel time: ", end='')
            print(travel_time)
            print("")
            '''
            if(curtime<start_time): #we are waiting in the bus station. the start_time is morphed into integer.
                return calc_cur_cord(source, destination, 0)
            if(curtime<=start_time+travel_time):
                tperc=(curtime-start_time)/travel_time
                return calc_cur_cord(source, destination, tperc)
            
            else : #curtime>start_time+travel_time. this implies we are on next hop.
                
                pass
    def __init__(self):
        pass


__enigma=False
if __enigma:
    tr=tracer_module()
    database=database_binding()
    rt=router_module(0, database)
#test suite.
    path=rt.minimal_time_path(1,[2,3,4])   #bind path.
    pathl=translata(path)  #translate the path into human readable
    for i in range (tr.calc_start_time(pathl),tr.calc_end_time(pathl), 10):
        #trace starts from calc_start_time(path), ends at calc_end_time(path)
        print(tr.trace(i,pathl))
    
    print(tr.calc_start_time(pathl))
    
    print(tr.calc_end_time(pathl))
