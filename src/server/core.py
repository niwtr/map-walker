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

import termios
import tty
import select
import sys
import os


'''
Environment of the core finite state machine.
##
cmail: mailbox of this module.
permitted_fn: only permitted functions are callable, aka, controllable by outside modules.
##

'''




class core_domain():


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

    def core_machine(self):
        while True:
            pkt=self.cmail.pread()
            if isinstance(pkt, transmitter_packet):
                result=self.command_interpreter(pkt.req)(*pkt.args)
                self.cmail.send(self.tr_mailbox, pkt.pipe, str(result))        

    def run(self):
        threading.Thread(target=self.core_machine, args=()).start()


    def mail_interface(self, mail_box):
        prinl('-')
        print('Mailbox '+str(mail_box))
        prinl('-')
        
        for mail in mail_box.history:
            print('Mail from ',mail('tag'),'with content ',mail('describe'))
            
        prinl('*')
        print('Press o to return to main interface.')

    def main_interface(self):
        prinl('-')
        print('Main interface.')
        prinl('-') 
        print('Press m for server monitor')
        print('Press k to kill a server')
        print('Press q or <esc> to quit')
        print('Press t to check transmitter mailbox history')
        print('Press c to check core mailbox history')


        
    command_usage_string='''
    shutdown <com> := Shutdown the server of com <com>

    '''

    


    def monitor(self):

        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())        

        status='main'

        while True:
            sys.stdout.flush()
            time.sleep(0.5)
            os.system("clear")

            if status=='main': 
                self.main_interface()
                
            elif status=='server monitor':
                prinl('-')
                print('Server monitor.')
                prinl('-')
                self.transmitter.server_monitor()
                prinl('-')
                print('Pass o to return to main interface.')
                prinl('-')
                 
                
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
                self.mail_interface(self.cmail)

            elif status=='tmail':
                self.mail_interface(self.transmitter.tmail)
                
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                c = sys.stdin.read(1)
                if c == '\x1b' or c=='q': 
                    print('bye.')
                    break#break #currently cannot quit neatly.

                elif c=='k': status='kill'

                elif c=='m': status='server monitor'
                
                elif c=='o': status='main'
                
                elif c=='t': status='tmail'
                
                elif c=='c': status='cmail'






        #restore old tty setting
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        exit()



    def shut_down():            #write the log and shut down the state machine
        pass





    
tty_rows, tty_columns = os.popen('stty size', 'r').read().split()            
tty_rows=int(tty_rows)
tty_columns=int(tty_columns)	

def prinl(c):
    for i in range(0, tty_columns):
        print(c,end='')    

cd=core_domain()
cd.initialize_env()
cd.start_transmitter()
cd.run()
#able to work without monitor.
cd.monitor()





