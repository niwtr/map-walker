#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
Database module.
Get the database, convert it to the built-in data structure and hold a link
to it. The module should be initialized before any other modules except mailer
and log.
Design: L.Laddie
'''

import sqlite3, os, re, datetime
from log import log_file
from enum import Enum

'''
Define the different vehicles
'''
class vehicle(Enum):
    flight = 0
    train = 1
    bus = 2

'''
It is a class of one path which contains the source, destination, distance,
starting time and so on.
'''
class router_path:
    def __init__(self, source, destination, num, mode,travel_time, distance, price, start_time):
        self.source = source
        self.destination = destination
        self.num = num
        self.mode = mode
        self.travel_time = travel_time
        self.distance = distance
        self.price = price
        self.start_time = datetime.datetime.strptime(start_time, '%H:%M')

'''
Connect to the database.
'''
def connect_to_datab():
    path = os.getcwd()
    pparent_path = os.path.dirname(os.path.dirname(path))   #get the root dir
    data_path = os.path.join(pparent_path, 'data', 'data.db')
    sql = sqlite3.connect(data_path)
    log_file.info('database connected from %s', data_path)   #write to the log file
    return sql

'''
Get raw data of the database.
'''
def datab_get_raw_data(sql):
    cur = sql.cursor()
    cur.execute('select * from flight')  #fetch the raw data of flight
    raw_data_flight = cur.fetchall()
    cur.execute('select * from train')  #fetch the raw data of train
    raw_data_train = cur.fetchall()
    cur.execute('select * from highway') #fetch the raw data of highway
    raw_data_bus = cur.fetchall()
    return (raw_data_flight, raw_data_train, raw_data_bus)

'''
Process the raw data to one list
'''
def datab_process_data(raw_data_flight, raw_data_train, raw_data_bus):
    data_path = [[[] for i in range(10)] for i in range(10)]
    raw_data = [raw_data_flight, raw_data_train, raw_data_bus]
    mode = [vehicle.flight, vehicle.train, vehicle.bus]
    for i in range(3):
        for element in raw_data[i]:
            #convert time format
            temp_string = element[6]
            hour = '0'
            minute = '0'
            if(temp_string.find('h') != -1):
                hour = temp_string.split('h')[0]
                temp_string = temp_string.split('h')[1]
            if(temp_string.find('m') != -1):
                minute = temp_string.split('m')[0]
            travel_time = int(hour) * 60 + int(minute)

            #convert the start time format
            fm = re.compile(r'\d{1,2}:\d\d')
            if(element[9]):
                ans = fm.findall(element[9])
            else:
                ans = []
            for j in ans:
                new_path_l = router_path(element[3], element[5], element[1], mode[i], travel_time, element[7], element[8], j)
                new_path_r = router_path(element[5], element[3], element[1], mode[i], travel_time, element[7], element[8], j)
                data_path[int(element[3])-1][int(element[5])-1].append(new_path_l)
                data_path[int(element[5])-1][int(element[3])-1].append(new_path_r)
    return data_path

'''
Check wether the history is modified. If so, emit warning.
'''
def check_health():
    pass

class database_binding:
    sql = []
    raw_data_flight = raw_data_train = raw_data_bus = []
    data_path = []

    def __init__(self):
        self.sql = connect_to_datab()
        (self.raw_data_flight, self.raw_data_train, self.raw_data_bus) = datab_get_raw_data(self.sql)
        self.data_path = datab_process_data(self.raw_data_flight, self.raw_data_train, self.raw_data_bus)

if(__name__ == '__main__'):
    sql = connect_to_datab()
    (raw_data_flight, raw_data_train, raw_data_bus) = datab_get_raw_data(sql)
    data_path = datab_process_data(raw_data_flight, raw_data_train, raw_data_bus)
    for element in data_path[0][1]:
        print(element.num)
