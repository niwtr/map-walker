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


datab=[]
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
    pass

def minimal_time(datab_link,source, destination):
    pass

def minimal_cost_restricted(datab_link, source,destination):
    pass

