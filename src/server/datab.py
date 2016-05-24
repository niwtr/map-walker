#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
Database module.
Get the database, convert it to the built-in data structure and hold a link
to it. The module should be initialized before any other modules except mailer
and log.
Design: Heranort, L.Laddie
'''

import sqlite3, os, re
from log import log_file
import router

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
    mode = [router.vehicle.flight, router.vehicle.train, router.vehicle.bus]
    for i in range(3):
        for element in raw_data[i]:
            #convert time format to integer
            temp_int = 0
            temp_string = element[6]
            if(temp_string.find('h') != -1):
                temp_int += int(temp_string.split('h')[0]) * 60
                temp_string = temp_string.split('h')[1]
            if(temp_string.find('m') != -1):
                temp_int += int(temp_string.split('m')[0])

            fm = re.compile(r'\d{1,2}:\d\d')
            if(element[9]):
                ans = fm.findall(element[9])
            else:
                ans = []
            for j in ans:
                new_path = router.router_path(element[2], element[4], element[1], mode[i], temp_int, element[7], element[8], j)
            data_path[int(element[3])-1][int(element[5])-1].append(new_path)
            data_path[int(element[5])-1][int(element[3])-1].append(new_path)
    return data_path

'''
Check wether the history is modified. If so, emit warning.
'''
def check_health():
    pass

class database_binding():
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
        print(element.mode)