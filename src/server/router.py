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
import copy, datetime
from datab import database_binding
from log import log_file
from datab import vehicle
def translata(raw_pathl):  
    day_weight=3600
    hour_weight=60
    minute_weight=1
    moddict={vehicle.bus : 2,
             vehicle.flight:0, 
             vehicle.train:1}
    acc=[]
    dtoi=lambda datime:datime.minute+datime.hour*hour_weight+datime.day*day_weight
    for obj in raw_pathl:
        acc.append([obj.source, obj.destination,
                    obj.num,moddict[obj.mode], obj.travel_time,
                    obj.distance, obj.price, dtoi(obj.start_time)])

    return acc

'''
Write the current route to history.
The history maybe used twice for reference of path recommendation.
'''

def emit_to_history(route):
    pass


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
        source -= 1
        for i in range(len(destination)):
            destination[i] -= 1
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
                        dis[i] = min_path[k][i].price + dis[k]
                        path[i] = copy.deepcopy(path[k])
                        path[i].append(min_path[k][i])
            for w in range(10):   #from the select city to update others
                if(final[w] == False and min_path[k][w] and (min_temp + min_path[k][w].price < dis[w])):
                    dis[w] = min_temp + min_path[k][w].price
                    path[w] = copy.deepcopy(path[k])
                    path[w].append(min_path[k][w])
        return translata(path[k])

    def minimal_time_path(self, source, destination):
        source -= 1
        for i in range(len(destination)):
            destination[i] -= 1
        min_path = [[] for i in range(10)]
        inf = 1000000

        #transfer the time to datatime format
        def transfer(date_time):
            temp_time = date_time % (24 * 60)
            hour = temp_time / 60
            minute = temp_time % 60
            temp_time = str(int(hour)) + ':' + str(int(minute))
            return datetime.datetime.strptime(temp_time, '%H:%M')

        #dynamic find the next minimal path
        def dyn_find_next(i, j, last_time):
            min_temp = inf
            temp_path = []
            for element in self.data_path[i][j]:
                payload = 0
                if(element.start_time > last_time[i]):
                    temp_time = element.start_time - last_time[i]
                    payload = temp_time.seconds / 60
                else:
                    temp_time = last_time[k] - element.start_time
                    payload = 24 * 60 - (temp_time.seconds / 60)
                if(min_temp > element.travel_time + payload):
                    min_temp = element.travel_time + payload
                    temp_path = element
            return (min_temp, temp_path)

        #Prepare the data before dijkstra
        for j in range(10):
            min_temp = inf
            for k in self.data_path[source][j]:
                if(min_temp > k.travel_time):
                    min_temp = k.travel_time
                    min_path[j] = k

        #dijkstra algorithm
        final = [False for i in range(10)]  #whether finding the minimal path to city i
        path = [[] for i in range(10)]      #the path from source to city i
        dis = [inf for i in range(10)]      #the time offset when arrive city i
        last_time = [[] for i in range(10)]     #the clock when arrive the city i

        #initialize the variables
        for i in range(10):
            if(min_path[i]):
                dis[i] = min_path[i].travel_time
                path[i] = [min_path[i]]
                last_time[i] = transfer(min_path[i].travel_time)

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
                for q in range(10):     #from the last demand city to find others
                    if(q != k):
                        (min_temp, temp_path) = dyn_find_next(k, q, last_time)
                        dis[q] = min_temp + dis[k]
                        path[q] = copy.deepcopy(path[k])
                        path[q].append(temp_path)
                        last_time[q] = transfer(dis[q])

            for w in range(10):   #from the select city to update others
                (min_temp, temp_path) = dyn_find_next(k, w, last_time)
                if(final[w] == False and temp_path and (dis[k] + min_temp < dis[w])):
                    dis[w] = dis[k] + min_temp
                    path[w] = copy.deepcopy(path[k])
                    path[w].append(temp_path)
                    last_time[w] = transfer(dis[w])
        return translata(path[k])

    def restricted_minimal_cost_path(self, source, destination, restrict):
        restrict_data_path = [[[] for i in range(10)] for i in range(10)]
        for i in range(10):
            for j in range(10):
                for element in self.data_path[i][j]:
                    if(element.travel_time <= restrict):
                        restrict_data_path[i][j].append(element)

        inf = 10000000
        path = [[] for i in range(10)]
        dp = [[0 for i in range(10)] for i in range(restrict+1)]
        for i in range(restrict + 1):
            if(i > 0):
                for j in range(10):
                    for ele_path in path[j]:
                        for ele_data in restrict_data_path[source][j]:
                            pass

        # for i in range(9, -1, -1):
        #     for j in range(restrict + 1):
        #         if(data_flight_time[source][i] and data_flight_time[source][i][0] <= j):
        #             dp[j][i] = data_flight_price[source][i][0]
        #
        # for i in range(10):
        #     for l in range(restrict + 1):
        #         if(data_flight_time[source][i] and l >= data_flight_time[source][i][0]):
        #             dp[l][i] = min(dp[l][i], dp[l - data_flight_time[source][i][0]][i] + data_flight_price[source][i][0])
        #
        # for i in range(10):
        #     for j in range(restrict+1):
        #         print(dp[j][i], end=' ')
        #     print('')

if(__name__ == '__main__'):
    database = database_binding()
    router_path = router_module(0 ,database)
    path = router_path.minimal_time_path(1, [2, 3, 4, 5, 6])
    for element in path:
        print(element.source, element.destination, element.mode, element.price, element.travel_time, element.start_time)
    # restrict_path = router_path.restricted_minimal_cost_path(0, [1, 2], 300)