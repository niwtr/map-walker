#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
Database module.
Get the database, convert it to the built-in data structure and hold a link
to it. The module should be initialized before any other modules except mailer
and log.
Design: Heranort
'''

import sqlite3, os


'''
Connect to the database.
'''
def connect_to_datab():
    path = os.getcwd()
    pparent_path = os.path.dirname(os.path.dirname(path))   #get the root dir
    # print(pparent_path)
    sql = sqlite3.connect(os.path.join(pparent_path, 'data', 'data.db'))
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
    data_distance = [[[] for i in range(10)] for i in range(10)]
    data_time = [[[] for i in range(10)] for i in range(10)]
    data_route = [[[] for i in range(10)] for i in range(10)]
    for element in raw_data:
        data_price[int(element[3])-1][int(element[5])-1].append(element[8])
        data_price[int(element[5])-1][int(element[3])-1].append(element[8])

        data_distance[int(element[3])-1][int(element[5])-1].append(element[7])
        data_distance[int(element[5])-1][int(element[3])-1].append(element[7])

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

        data_route[int(element[3])-1][int(element[5])-1].append(element[1])
        data_route[int(element[5])-1][int(element[3])-1].append(element[1])
    lis = {'price': data_price,'time': data_time, 'distance': data_distance, 'route': data_route}
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
    return data_all

'''
Check wether the history is modified. If so, emit warning.
'''
def check_health():
    pass

if(__name__ == '__main__'):
    sql = connect_to_datab()
    (raw_data_flight, raw_data_train, raw_data_bus) = datab_get_raw_data(sql)
    data_flight = datab_process_data(raw_data_flight)
    data_train = datab_process_data(raw_data_train)
    data_bus = datab_process_data(raw_data_bus)
    data_all = datab_mix_all(data_flight, data_train, data_bus)   #the final data
    data_name = datab_get_name(raw_data_train)  #station_name
    for element in data_all['train']['time']:
        print(element)
    print(data_name)