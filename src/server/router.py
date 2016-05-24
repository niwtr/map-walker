'''
ROUTER module
Calculates the shortest path(with specific stategies) and flow the path data 
to clients, via the transmitter module.

Three strategies are required:
 1. minimal cost
 2. minimal time
 3. minimal cost in a limited time.

The path calculated already must be stored somewhere to support the tracer module.

Design: Heranort, L.Laddie
'''

import mailer
import log
import time
import copy
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
        self.start_time = time.strptime(start_time, '%H:%M')


'''
Write the current route to history.
The history maybe used twice for reference of path recommendation.
'''

def emit_to_history(route):
    pass


'''
################################################################################
This algorithm can use mode to select different minimal ways.
For example: minimal_path(data_all, 0, [1, 5, 9], 'price')
################################################################################
'''
def minimal_path(datab_link, source, destination, mode):
    dat_flight = datab_link['flight']
    dat_train = datab_link['train']
    dat_bus = datab_link['bus']
    minimal = [[[-1 for i in range(2)] for i in range(10)] for i in range(10)]
    #cmt: the 0th level denotes the val, the 1th level denotes the mean of transportation.
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
        path[i] = [[source, minimal[source][i][1]]]    ##
    dis[source] = 0
    final[source] = True
    k = -1     #the last arrive city id
    for i in range(9):
        k = -1
        min_temp = inf     #find the minimal dis[j]
        for j in range(10):    #relax.
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


def minimal_cost_restricted(datab_link, source, destination, restrict):
    def dist(v1, v2, mode, mean):
        meandict={0:'flight', 1:'train', 2:'bus'}
        return datab_link[meandict[mean]][mode][v1][v2][0]

    def tdist(v1, v2, mean):
        return dist(v1, v2, 'time', mean)

    def cdist(v1, v2, mean):
        return dist(v1, v2, 'price', mean)

def minimal_path_restricted(datab_link, source,destination, limit, mode):
    data_flight_time = datab_link['flight']['time']
    data_flight_price = datab_link['flight']['price']
    city_num = len(data_flight_time)
    dp = [[-1 for i in range(10)] for i in range(limit+1)]
    for i in range(9, -1, -1):
        for j in range(limit + 1):
            if(data_flight_time[source][i] and data_flight_time[source][i][0] <= j):
                dp[j][i] = data_flight_price[source][i][0]

    for i in range(10):
        for l in range(limit + 1):
            if(data_flight_time[source][i] and l >= data_flight_time[source][i][0]):
                dp[l][i] = min(dp[l][i], dp[l - data_flight_time[source][i][0]][i] + data_flight_price[source][i][0])

    for i in range(10):
        for j in range(limit+1):
            print(dp[j][i], end=' ')
        print('')

'''
################################################################################
Work as interface toward the core module.
Exporting route_calculating functions used by core.
Does not contian a mailbox.
################################################################################
'''
class router_module():  
    data_all=[]
    '''
    Initialize the router module, including initializing the mailer, ensuring conne-
    ction to the data base, checking the health of connection between core, and est-
    ablishing user history.
    '''
    def __init__(self, core_mail_binding, database_binding):
        self.data_all = database_binding.data_all

    def minimal_cost_path(self,id_src, id_dest):
            return minimal_path(self.data_all, id_src,id_dest, 'price')

    def minimal_time_path(self, id_src, id_dest):
        return minimal_path(self.data_all, id_src, id_dest, 'time')

    def restricted_minimal_cost_path(self, id_src, id_dest, restrict):
        return minimal_cost_restricted(self.data_all, id_src, id_dest, restrict)

if(__name__ == '__main__'):
    pass
    # database = database_binding()
    # minimal_path_restricted(database.data_all, 1, 5, 120, 'price')
    # path = Path(0, 1, 'CA002/003', 1200, 500, 600, '8:00')
    # print(path.start_time > time.strptime('7:00', '%H:%M'))