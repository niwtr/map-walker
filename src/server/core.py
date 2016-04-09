#! /usr/bin/python
# -*- coding: utf-8 -*-

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
import threading
import time
import mailer
from datab import database_binding
from router import router_module
from transmitter import transmit_env
from transmitter import transmitter_packet
from log import log_file



'''
Environment of the core finite state machine.
##
cmail: mailbox of this module.
permitted_fn: only permitted functions are callable, aka, controllable by outside modules.
##

'''








class core_domain():
    
    router=[]
    
    database=[]
    
    transmitter=[]

    permitted_fn=[]             #permitted functions.
    
    def __init__(self):
        pass
        
        

    def initialize_env(self):       #initialize the environment.
        
        '''INIT CORE MAILBOX'''
        self.cmail=mailer.mailbox('core',50)
        '''INIT DATABASE'''
        self.database=database_binding()
        '''INIT ROUTER MODULE'''
        self.router=router_module(self.cmail, self.database)        
        '''INIT TRANSMITTER ENVIRONMENT'''
        self.transmitter=transmit_env(self.cmail)
        
        '''TRANSMITTER MAILBOX'''
        self.tr_mailbox=self.transmitter.tmail



    
    def start_transmitter(self): #procedure for controling transmitter module
        threading.Thread(target=self.transmitter.seq_start, args=()).start()
    
    '''interprete the request command into actual functions'''
    def command_interpreter(self,cmd):
        if cmd=='mtp':
            return self.router.minimal_time_path
        elif cmd=='mcp':
            return self.router.minimal_cost_path

    
    def run(self):
        while True:
            pkt=self.cmail.read()
            if isinstance(pkt, transmitter_packet):
                result=self.command_interpreter(pkt.req)(*pkt.args)
                self.cmail.send(self.tr_mailbox, pkt.pipe, str(result))

    
           

    def shut_down():            #write the log and shut down the state machine
        pass
    



cd=core_domain()
cd.initialize_env()
cd.start_transmitter()
cd.run()









