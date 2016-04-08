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
Algolrithms.
'''
def minimal_cost(datab_link, source, destination):
    dat_flight = datab_link['flight']['price']
    dat_train = datab_link['train']['price']
    dat_bus = datab_link['bus']['price']
    min_price = [[[-1 for i in range(2)] for i in range(10)] for i in range(10)]
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
                min_price[i][j][0] = a
                min_price[i][j][1] = 0
            elif(b <= a and b <= c):  #the train has lower price
                min_price[i][j][0] = b
                min_price[i][j][1] = 1
            else:                     #the bus has lower price
                min_price[i][j][0] = c
                min_price[i][j][1] = 2
            if(min_price[i][j][0] == inf):  #regular the value
                min_price[i][j] = [-1, -1]

    #dijkstra algorithm
    dis = [-1 for i in range(10)]
    path = [[-1] for i in range(10)]
    final = [False for i in range(10)]

    for i in range(10):
        dis[i] = min_price[source][i][0]
        path[i] = [[source, min_price[source][i][1]]]
    dis[source] = 0
    final[source] = True
    for i in range(9):
        k = -1
        min_temp = inf
        for j in range(10):
            if(final[j] == False and dis[j] < min_temp):
                k = j
                min_temp = dis[j]
        final[k] = True
        if(k == destination):
            break
        for w in range(10):
            if(final[w] == False and min_price[k][w][0] != -1 and (min_temp + min_price[k][w][0] < dis[w])):
                dis[w] = min_temp + min_price[k][w][0]
                path[w] = copy.deepcopy(path[k])
                path[w].append([k, min_price[k][w][1]])
    path[destination].append([destination, -1])
    return (path[destination], dis[destination])

def minimal_time(datab_link,source, destination):
    dat_flight = datab_link['flight']['time']
    dat_train = datab_link['train']['time']
    dat_bus = datab_link['bus']['time']
    min_time = [[[-1 for i in range(2)] for i in range(10)] for i in range(10)]
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
                min_time[i][j][0] = a
                min_time[i][j][1] = 0
            elif(b <= a and b <= c):  #the train has lower price
                min_time[i][j][0] = b
                min_time[i][j][1] = 1
            else:                     #the bus has lower price
                min_time[i][j][0] = c
                min_time[i][j][1] = 2
            if(min_time[i][j][0] == inf):  #regular the value
                min_time[i][j] = [-1, -1]

    #dijkstra algorithm
    dis = [-1 for i in range(10)]
    path = [[-1] for i in range(10)]
    final = [False for i in range(10)]

    for i in range(10):
        dis[i] = min_time[source][i][0]
        path[i] = [[source, min_time[source][i][1]]]
    dis[source] = 0
    final[source] = True
    for i in range(9):
        k = -1
        min_temp = inf
        for j in range(10):
            if(final[j] == False and dis[j] < min_temp):
                k = j
                min_temp = dis[j]
        final[k] = True
        if(k == destination):
            break
        for w in range(10):
            if(final[w] == False and min_time[k][w][0] != -1 and (min_temp + min_time[k][w][0] < dis[w])):
                dis[w] = min_temp + min_time[k][w][0]
                path[w] = copy.deepcopy(path[k])
                path[w].append([k, min_time[k][w][1]])
    path[destination].append([destination, -1])
    return (path[destination], dis[destination])

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

    source = 0
    desti = 4

    (path_cost, min_cost) = minimal_cost(data_all, source, desti)
    (path_time, min_time) = minimal_time(data_all, source, desti)

    def print_path(data_path, data_name):
        for element in data_path:
            print(data_name[element[0]], end=' ')
            if(element[1] == 0):
                print('飞机', end=' ')
            elif(element[1] == 1):
                print('火车', end=' ')
            elif(element[1] == 2):
                print('汽车', end=' ')

    print_path(path_cost, data_name)
    print(min_cost)
    print_path(path_time, data_name)
    print(min_time)