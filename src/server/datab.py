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
    sql = sqlite3.connect(pparent_path + '\data\data.db')
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
def datab_process_data(raw_data_flight, raw_data_train, raw_data_bus):
    data_price = [[-1 for i in range(10)] for i in range(10)]
    data_instance = [[-1 for i in range(10)] for i in range(10)]
    data_time = [[-1 for i in range(10)] for i in range(10)]
    for element in raw_data_bus:
        pass


'''
Preserve the processed data into somewhere.
'''
def datab_preserve_data():
    pass

'''
Check wether the history is modified. If so, emit warning.
'''
def check_health():
    pass

if(__name__ == '__main__'):
    sql = connect_to_datab()
    (raw_data_flight, raw_data_train, raw_data_bus) = datab_get_raw_data(sql)
    datab_process_data(raw_data_flight, raw_data_train, raw_data_bus)