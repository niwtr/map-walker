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
import copy
from datab import database_binding
from log import log_file


'''
Write the current route to history.
The history maybe used twice for reference of path recommendation.
'''

def emit_to_history(route):
    pass

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
class router_module:
    data_all=[]
    '''
    Initialize the router module, including initializing the mailer, ensuring conne-
    ction to the data base, checking the health of connection between core, and est-
    ablishing user history.
    '''
    def __init__(self, core_mail_binding, database_binding):
        self.data_path = database_binding.data_path

    '''
    ################################################################################
    This algorithm can use mode to select different minimal ways.
    For example: minimal_cost_path(data_all, 0, [1, 5, 9])
    ################################################################################
    '''
    def minimal_cost_path(self, source, destination):
        min_path = [[[] for i in range(10)] for i in range(10)]
        inf = 1000000

        #Prepare the data before dijkstra
        for i in range(10):
            for j in range(10):
                min_temp = inf
                for k in self.data_path[i][j]:
                    if(min_temp > k.price):
                        min_temp = k.price
                        min_path[i][j] = k

        #dijkstra algorithm
        final = [False for i in range(10)]
        path = [[] for i in range(10)]
        dis = [inf for i in range(10)]

        for i in range(10):
            if(min_path[source][i]):
                dis[i] = min_path[source][i].price
                path[i] = [min_path[source][i]]

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
                        dis[i] = min_path[k][i].price + dis[k]
                        path[i] = copy.deepcopy(path[k])
                        path[i].append(min_path[k][i])
            for w in range(10):   #from the select city to update others
                if(final[w] == False and min_path[k][w] and (min_temp + min_path[k][w].price < dis[w])):
                    dis[w] = min_temp + min_path[k][w].price
                    path[w] = copy.deepcopy(path[k])
                    path[w].append(min_path[k][w])
        return path[k]

    def minimal_time_path(self, id_src, id_dest):
        pass

    def restricted_minimal_cost_path(self, id_src, id_dest, restrict):
        return minimal_cost_restricted(self.data_path, id_src, id_dest, restrict)

if(__name__ == '__main__'):
    database = database_binding()
    router_path = router_module(0 ,database)
    path = router_path.minimal_cost_path(0, [8, 2])
    for element in path:
        print(element.source, element.destination, element.mode, element.price)