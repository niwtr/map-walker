#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
Database module.
Get the database, convert it to the built-in data structure and hold a link
to it. The module should be initialized before any other modules except mailer
and log.
Design: Heranort, L.Laddie
'''

import sqlite3, os
from log import log_file

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
Process the raw data.
'''
def datab_process_data(raw_data):
    data_price = [[[] for i in range(10)] for i in range(10)]
    data_time = [[[] for i in range(10)] for i in range(10)]
    for element in raw_data:
        data_price[int(element[3])-1][int(element[5])-1].append(element[8])
        data_price[int(element[5])-1][int(element[3])-1].append(element[8])

        #convert time format to integer
        temp_int = 0
        temp_string = element[6]
        if(temp_string.find('h') != -1):
            temp_int += int(temp_string.split('h')[0]) * 60
            temp_string = temp_string.split('h')[1]
        if(temp_string.find('m') != -1):
            temp_int += int(temp_string.split('m')[0])

        data_time[int(element[3])-1][int(element[5])-1].append(temp_int)
        data_time[int(element[5])-1][int(element[3])-1].append(temp_int)
    lis = {'price': data_price,'time': data_time}
    return lis

'''
Get the name of station id
'''
def datab_get_name(raw_data):
    data_name = [-1 for i in range(10)]
    for element in raw_data:
        data_name[int(element[3]) - 1] = element[2]
        data_name[int(element[5]) - 1] = element[4]
    return data_name

'''
Mix all the different transportation to one data list
'''
def datab_mix_all(data_flight, data_train, data_bus):
    data_all = {'flight': data_flight, 'train': data_train, 'bus': data_bus}
    log_file.info('database successfully processed')
    return data_all

'''
Check wether the history is modified. If so, emit warning.
'''
def check_health():
    pass

class database_binding():
    sql=[]
    raw_data_flight=raw_data_train=raw_data_bus=[]
    data_flight=[]
    data_train=[]
    data_bus=[]
    data_all=[]
    data_name=[]
    def __init__(self):
        self.sql = connect_to_datab()
        (self.raw_data_flight, self.raw_data_train, self.raw_data_bus) = datab_get_raw_data(self.sql)
        self.data_flight = datab_process_data(self.raw_data_flight)
        self.data_train = datab_process_data(self.raw_data_train)
        self.data_bus = datab_process_data(self.raw_data_bus)
        self.data_all = datab_mix_all(self.data_flight, self.data_train, self.data_bus)   #the final data
        self.data_name = datab_get_name(self.raw_data_train)  #station_name    
        


if(__name__ == '__main__'):
    pass
    '''
    sql = connect_to_datab()
    (raw_data_flight, raw_data_train, raw_data_bus) = datab_get_raw_data(sql)
    data_flight = datab_process_data(raw_data_flight)
    data_train = datab_process_data(raw_data_train)
    data_bus = datab_process_data(raw_data_bus)
    data_all = datab_mix_all(data_flight, data_train, data_bus)   #the final data
    data_name = datab_get_name(raw_data_train)  #station_name
    '''
 