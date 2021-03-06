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
#from textprotocol import scprotocol
from transmitter import transmit_env
from transmitter import transmitter_packet
from log import log_file
from tracer import tracer_module

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
        '''INIT TRACER MODULE'''
        self.tracer=tracer_module()
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
        elif cmd=="trace":
            return self.tracer.trace
        elif cmd=="start-time":
            return self.tracer.calc_start_time
        elif cmd=="end-time":
            return self.tracer.calc_end_time
        elif cmd=='echo':
            return lambda x:x
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
        self.status='main'
        self.__event=False
        
    
    def init_core(self):
        self.initialize_env()
        self.start_transmitter()
        self.run()
        threading.Thread(target=self.input_listener).start()
        
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
            #print(str(count)+': '+'Mail from ',mail('tag'),'with content ',mail('describe'))
            print(str(count)+': ',mail('describe'))
            count+=1
            
        self.prinl('*')
        print('Press o to return to main interface.')

    def main_interface(self):
        self.prinl('-')
        print('''
        Map-Walker, the ULTIMATE solution to online path guiding
        Current Version: 0.5
        Developers:
                     Tianrui Niu,
                     Han Liu, 
                     Mo Ying
        Make fun.
        ''')    
        self.prinl('-') 
        print('Press l to check license.')
        print('Press m for server monitor')
        print('Press k to kill a server')
        print('Press t to check transmitter mailbox history')
        print('Press c to check core mailbox history')
        print('Press q or <esc> to quit')
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


    def input_listener(self):
        while 1:
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                c = sys.stdin.read(1)
                
                if c == '\x1b' or c=='q': 
                    print("Moriturus te saluto.")
                    time.sleep(1)
                    self.status='exit'
                    break
    
                elif c=='k': self.status='kill'
    
                elif c=='m': self.status='server monitor'
                
                elif c=='o': self.status='main'
                
                elif c=='t': self.status='tmail'
                
                elif c=='c': self.status='cmail'    
                
                elif c=='l': self.status='license'
                
                elif c==' ': pass
                self.__event=True
        
    def monitor(self):

        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())        

        while True:


            if self.status=='main': 
                self.main_interface()
                
            elif self.status=='server monitor':
                self.prinl('-')
                print('Map-Walker Server Monitor.')
                self.prinl('-')
                self.server_monitor_interface()
                self.prinl('-')
                print('Pass o to return to main interface.')
                self.prinl('-')
                 
            elif self.status=='exit':   

                break
                
            elif self.status=='kill':
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                com=int(input("Type the com of the server: "))
                sucp=self.transmitter.shutdown_MASS(com)
                if not sucp:
                    print('Could not find server %s' % str(com))
                else: 
                    print('Server %s shutted down.' % str(com))
                self.status='main'            
                tty.setcbreak(sys.stdin.fileno())  
                
            elif self.status=='cmail':
                self.mailbox_monitor_interface(self.cmail)

            elif self.status=='tmail':
                self.mailbox_monitor_interface(self.transmitter.tmail)
            elif self.status=='license':
                self.prinl('-')
                print('''
                The MIT License (MIT)

Copyright (c) 2016 niwtr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
                ''')
                self.prinl('-')
                
                
            sys.stdout.flush()
            while(not self.__event and self.status!='exit'):
                time.sleep(0.01)
            self.__event=False
            os.system("clear")            

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
