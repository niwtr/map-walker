from datab import database_binding

from router import router_module



class scprotocol():
    
    
    data_fl=database_binding.data_flight
    data_bus=database_binding.data_bus
    data_tr=database_binding.data_train
    
    def __init__(self, router, db):
        self.data_all=db.data_all
        self.router_binding=router
    
    def dist(self, v1, v2, mode, mean):
        meandict={0:'flight', 1:'train', 2:'bus'}
        return self.data_all[meandict[mean]][mode][v1][v2][0]
    def tdist(self, v1, v2, mean):
        return self.dist(v1, v2, 'time', mean)
    def cdist(self, v1, v2, mean):
        return self.dist(v1, v2, 'price', mean)
    def ddist(self, v1, v2, mean):
        return self.dist(v1, v2, 'distance', mean)    
    
    def interpreter(cmd):
        pass
    
    '''
    mcp & mtp return a triple, with the first place being the path, the second
    being the time and the third being the cost.
    '''
    
    def mtp(self, id_src, id_dest):
        raw=self.router_binding.minimal_time_path(id_src, id_dest)
        path_matrix=raw[0]
        mintime=raw[1]

        cost_total=0
        for index in range(0, len(path_matrix)-1):
            first=path_matrix[index]
            second=path_matrix[index+1]
            mean=first[1] #get the mean of transportation.
            cost_total=cost_total+self.cdist(first[0], second[0], mean)
        return (path_matrix, mintime, cost_total)
            
    def mcp(self, id_src, id_dest):
        raw=self.router_binding.minimal_cost_path(id_src, id_dest)
        path_matrix=raw[0]
        mincost=raw[1]

        time_total=0
        for index in range(0, len(path_matrix)-1):
            first=path_matrix[index]
            second=path_matrix[index+1]
            mean=first[1] #get the mean of transportation.
            time_total=time_total+self.tdist(first[0], second[0], mean)
        return (path_matrix, time_total, mincost)        
    
    
    def query(self, from_node, to_node, mean_of_transportation):
        return (self.tdist(from_node, to_node, mean_of_transportation), 
                self.cdist(from_node, to_node, mean_of_transportation),
                self.ddist(from_node, to_node, mean_of_transportation)
                )
    
    #(time, cost, distance)

    def query_all(self, *path_list):
        res=[]
        for index in range(len(path_list)-1):
            current=path_list[index]
            nextn=path_list[index+1]
            mean=current[1]
            query_res=self.query(current[0], nextn[0], mean)
            
            res.append([current[0], nextn[0], mean, 
                        query_res[0], query_res[1], query_res[2]])                        ])
        return res
            