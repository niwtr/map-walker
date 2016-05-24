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
from textprotocol import scprotocol
from transmitter import transmit_env
from transmitter import transmitter_packet
from log import log_file

import termios
import tty
import select
import sys
import os


'''
################################################################################
Environment of the core finite state machine.
##
cmail: mailbox of this module.
permitted_fn: only permitted functions are callable, aka, controllable by outside modules.
##
################################################################################
'''



def prinl(*c, end=''):log_file.info(*c)
def prinw(*c, end=''):log_file.warn(*c)

class core_domain():


    def __init__(self):
        pass



    def initialize_env(self):       #initialize the environment.
        self.core_machine_status='accept-all'
        '''INIT CORE MAILBOX'''
        self.cmail=mailer.mailbox('core',50)
        '''INIT DATABASE'''
        self.database=database_binding()
        '''INIT ROUTER MODULE'''
        self.router=router_module(self.cmail, self.database)        
        '''INIT TRANSMITTER ENVIRONMENT'''
        self.transmitter=transmit_env(self.cmail,self.command_interpreter)
#        self.scprotocol=scprotocol(self.router, self.database)
        '''TRANSMITTER MAILBOX'''
        self.tr_mailbox=self.transmitter.tmail


    def start_transmitter(self): #procedure for controling transmitter module
        threading.Thread(target=self.transmitter.seq_start, args=()).start()

    '''interprete the request command into actual functions'''
    def command_interpreter(self,cmd):
        def nil (*arg):
            return "ERROR COMMAND:"+str(arg)
        if cmd=='mtp':
            return self.router.minimal_time_path
        elif cmd=='mcp':
            return self.router.minimal_cost_path
        elif cmd=='rmcp':
            return self.router.restricted_minimal_cost_path
        elif cmd=='echo':
            return lambda x:x
#        elif cmd=="query":
#            return self.scprotocol.query
#        elif cmd=="query_all": #in this part, we must 
#            return self.scprotocol.query_all
        else :
            return nil
        
        '''
        elif cmd=='rmcp':
            return self.router.restricted_minimal_cost_path
        elif cmd=='trace':
            return self.tracer.trace
        '''
        
    def transmit_back(self):
        
        pkt=self.cmail.pread() #cowsay: original pread.
        
        if isinstance(pkt, transmitter_packet):
            try:
                self.cmail.send(self.tr_mailbox, pkt.pipe, str(pkt.eval_func()))
            except:
                self.cmail.send(self.tr_mailbox, pkt.pipe, "ERROR ARG")
                prinw("MASS "+str(pkt.MASS_NAME)+ " sent error argument.")
                
                
                
          
            
    def core_machine(self):

        while True:
      
            time.sleep(0.1) #cowsay:original 0.1             #i have to slow down the core machine.

            if self.core_machine_status=='accept-all':
                if self.cmail.check('tag')=='transmitter':
                    self.transmit_back()
            elif self.core_machine_status=='refuse-all':
                while not self.cmail.clearp():
                    self.cmail.preserve()
                    
                    
    def run(self):
        threading.Thread(target=self.core_machine, args=()).start()



    def shut_down(self):            #write the log and shut down the state machine
        
        pass



'''
################################################################################
Provides terminal interface for users.
This is non-necessary for server administrator. 
The monitor procedure is seperated from the core to keep the core clean and #.
################################################################################
'''

class shelled_core(core_domain):
    
    def __init__(self):
        self.tty_rows, self.tty_columns = os.popen('stty size', 'r').read().split()            
        self.tty_rows=int(self.tty_rows)
        self.tty_columns=int(self.tty_columns)	        

        
    
    def init_core(self):
        self.initialize_env()
        self.start_transmitter()
        self.run()
        return self
    
    
    def prinl(self,c):
        for i in range(0, self.tty_columns):
            print(c,end='')    
        
    
    def mailbox_monitor_interface(self, mail_box):
        self.prinl('-')
        print('Mailbox '+str(mail_box))
        self.prinl('-')
        count=1
        for mail in mail_box.history:
            print(str(count)+': '+'Mail from ',mail('tag'),'with content ',mail('describe'))
            
        self.prinl('*')
        print('Press o to return to main interface.')

    def main_interface(self):
        self.prinl('-')
        print('Main interface.')
        self.prinl('-') 
        print('Press m for server monitor')
        print('Press k to kill a server')
        print('Press q or <esc> to quit')
        print('Press t to check transmitter mailbox history')
        print('Press c to check core mailbox history')

    def server_monitor_interface(self):
        servs=self.transmitter.get_server_status()
        ids=servs['idling']
        wds=servs['working']
        print('Current idling servers:')
        if ids==[]:
            print('None')
        else:
            for i in ids :
                print(i)
        print('')
        print('Current working servers:')
        if wds==[]:
            print('None')
        else: 
            for i in wds:
                print(i)
        print('')
        print('Dispatcher: ',end='')
        if self.transmitter.dispatcher_MASS.sock_thread.isAlive():
            print('BUSY')
        else: 
            print('IDLE')

    def monitor(self):

        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())        

        status='main'

        while True:
            sys.stdout.flush()
            time.sleep(0.1)
            os.system("clear")

            if status=='main': 
                self.main_interface()
                
            elif status=='server monitor':
                self.prinl('-')
                print('Server monitor.')
                self.prinl('-')
                self.server_monitor_interface()
                self.prinl('-')
                print('Pass o to return to main interface.')
                self.prinl('-')
                 
                
            elif status=='kill':
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                com=int(input("Type the com of the server: "))
                sucp=self.transmitter.shutdown_MASS(com)
                if not sucp:
                    print('Could not find server %s' % str(com))
                else: 
                    print('Server %s shutted down.' % str(com))
                status='main'            
                tty.setcbreak(sys.stdin.fileno())  
                
            elif status=='cmail':
                self.mailbox_monitor_interface(self.cmail)

            elif status=='tmail':
                self.mailbox_monitor_interface(self.transmitter.tmail)
                
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                c = sys.stdin.read(1)
                if c == '\x1b' or c=='q': 
                    #restore old tty setting
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                    self.shut_down()        #currently no work.
                    os._exit(0)             #shutdown completely.                    
                    print('bye.')
                    break

                elif c=='k': status='kill'

                elif c=='m': status='server monitor'
                
                elif c=='o': status='main'
                
                elif c=='t': status='tmail'
                
                elif c=='c': status='cmail'


        #restore old tty setting
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        
        os._exit(0)             #shutdown completely.

    



if __name__=='__main__':
    mode=0
    if mode==0:
        shelled_core().init_core().monitor()
    else:
        #for clean testing.
        a=core_domain()
        a.initialize_env()
        a.start_transmitter()
        a.run()
