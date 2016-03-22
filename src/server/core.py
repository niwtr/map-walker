'''
Core module of server.
The reason why I seperarted fucntions into this module is to set a conversational
message passing model, to make promise of the clear partition of each module.
To lower the complexity, efforts must be made to design and decrease the interfaces
that ensure the conversation of modules. 
Offering mechanism for arranging and commumication with any other modules. 
Establishing environment before running other modules. 
It'd be worthy of time gaining full acknowledges of this module, both in function 
and implementation, before your start of programming. 


Design: Heranort
'''
import mailer






'''
Environment of the core finite state machine.
##
cmail: mailbox of this module.
permitted_fn: only permitted functions are callable, aka, controllable by outside modules.
##



'''
class core_domain():
    
    cmail=[]                    #mailer of core environment.

    permitted_fn=[]             #permitted functions.
    
    def __init__():
        pass

    def initialize_env():       #initialize the environment.
        pass
    
    def proc_idle():            #idle procedure
        pass
    
    def proc_ctl_router():      #procedure for controling router module
        pass
    
    def proc_ctl_tracer():      #procedure for controling tracer module
        pass
    
    def proc_ctl_transmitter(): #procedure for controling transmitter module
        pass
    
    def proc_ctl_datab():       #procedure for controling database module.
        pass
    
    def run():                  #run state mathine
        pass
    
    def shut_down():            #write the log and shut down the state machine
        pass
    
















