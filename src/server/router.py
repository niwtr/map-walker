'''
ROUTER module
Calculates the shortest path(with specific stategies) and flow the path data 
to clients, via the transmitter module.

Three strategies are required:
 1. minimal cost
 2. minimal timep
 3. minimsl cost in a limited time.

The path calculated already must be stored somewhere to suppor the tracer module.

RUN OTTA TIME, SEE YOU TOMMORROW.
'''

import mailer
import log
import datab
import copy


cmail=[]



'''
Initialize the router module, including initializing the mailer, ensuring conne-
ction to the data base, checking the health of connection between core, and est-
ablishing user history.
'''

def init_router():
    pass


'''
Write the current route to history.
The history maybe used twice for reference of path recommendation.
'''

def emit_to_history(route):
    pass

'''
Mail the path to core module.
'''
def mailing_path_to_core(route):
    pass

'''
This algorithm can use mode to select different minimal ways.
For example: minimal_path(data_all, 0, [1, 5, 9], 'price')
'''
def minimal_path(datab_link, source, destination, mode):
    dat_flight = datab_link['flight'][mode]
    dat_train = datab_link['train'][mode]
    dat_bus = datab_link['bus'][mode]
    minimal = [[[-1 for i in range(2)] for i in range(10)] for i in range(10)]
    inf = 100000   #set a infite value

    #caluclate the minimal price matrix
    for i in range(10):
        for j in range(10):
            a = inf
            b = inf
            c = inf
            if(dat_flight[i][j]):
                a = min(dat_flight[i][j])
            if(dat_train[i][j]):
                b = min(dat_train[i][j])
            if(dat_bus[i][j]):
                c = min(dat_bus[i][j])

            if(a <= b and a <= c):   #the flight has lower price
                minimal[i][j][0] = a
                minimal[i][j][1] = 0
            elif(b <= a and b <= c):  #the train has lower price
                minimal[i][j][0] = b
                minimal[i][j][1] = 1
            else:                     #the bus has lower price
                minimal[i][j][0] = c
                minimal[i][j][1] = 2
            if(minimal[i][j][0] == inf):  #regular the value
                minimal[i][j] = [-1, -1]

    #dijkstra algorithm
    dis = [-1 for i in range(10)]
    path = [[-1] for i in range(10)]
    final = [False for i in range(10)]

    for i in range(10):
        dis[i] = minimal[source][i][0]
        path[i] = [[source, minimal[source][i][1]]]
    dis[source] = 0
    final[source] = True
    k = -1     #the last arrive city id
    for i in range(9):
        k = -1
        min_temp = inf     #find the minimal dis[j]
        for j in range(10):
            if(final[j] == False and dis[j] < min_temp):
                k = j
                min_temp = dis[j]
        final[k] = True      #add a city
        if(k in destination):   #when a demand city added
            destination.remove(k)
            if(not destination):    #find all the demand city
                break
            for i in range(10):     #from the last demand city to find others
                if(i != k):
                    dis[i] = minimal[k][i][0] + dis[k]
                    path[i] = copy.deepcopy(path[k])
                    path[i].append([k, minimal[k][i][1]])
        for w in range(10):   #from the select city to update others
            if(final[w] == False and minimal[k][w][0] != -1 and (min_temp + minimal[k][w][0] < dis[w])):
                dis[w] = min_temp + minimal[k][w][0]
                path[w] = copy.deepcopy(path[k])
                path[w].append([k, minimal[k][w][1]])
    path[k].append([k, -1])  #add the last arrive city
    return (path[k], dis[k])

def minimal_cost_restricted(datab_link, source,destination):
    pass

if(__name__ == '__main__'):
    sql = datab.connect_to_datab()
    (raw_data_flight, raw_data_train, raw_data_bus) = datab.datab_get_raw_data(sql)
    data_flight = datab.datab_process_data(raw_data_flight)
    data_train = datab.datab_process_data(raw_data_train)
    data_bus = datab.datab_process_data(raw_data_bus)
    data_all = datab.datab_mix_all(data_flight, data_train, data_bus)   #the final data
    data_name = datab.datab_get_name(raw_data_flight)

    (path_cost, min_cost) = minimal_path(data_all, 0, [9, 2, 1, 6], 'price')
    (path_time, min_time) = minimal_path(data_all, 0, [1, 2, 6, 9], 'time')

    def print_path(data_path, data_name):
        for element in data_path:
            print(data_name[element[0]], end=' ')
            if(element[1] == 0):
                print('-飞机->', end=' ')
            elif(element[1] == 1):
                print('-火车->', end=' ')
            elif(element[1] == 2):
                print('-汽车->', end=' ')

    print_path(path_cost, data_name)
    print(min_cost)
    print_path(path_time, data_name)
    print(min_time)
