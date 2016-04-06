#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
Current version : 0.2
2016-3-26
by Heranort 
'''



import threading                                #for thread creation
import socket                                   #socket offical module
import time                                     #time official module

import os                                       #for fortune!
import mailer                                   #mailer module.

import platform                                 #judge the platform


#import log                                     #log module.


from mass_plists import M_A_S_S_PLIST           #property list for MASSES
from mass_plists import DISPATCH_PLIST

'''
################################################################################
                                   M_A_S_S
Modularized Abstract Socket Server (MASS) for TCP linking, and server environment
Authorized by Herathol Nortzor
First published: 2016-3-10

################################################################################
'''




'''
################################################################################
Modularized Abstract Socket Server class.
This is an abstraction of an instant-to-use socket server. Needs a property list
to configure and consumes a finite state machine, or cyclic procedure for inner 
running machine. When a MASS was instantialized, it creates an abstract server
but doesn't make any bind to the socket. And when the function start() was 
called, the MASS would bind to the socket instantly and start working with the 
state machine attached. The goal of this is to create an easy-to-use abstrac-
tion of socket server.
In fact, the REAL MASS would not exist. Each version of MASS is adapted to the
actual use, so does this one.


Happy hacking with the M_A_S_S!

################################################################################
'''


def sayhello():
    print ('timer stopped!')

class M_A_S_S():
    
    plist=[]
    
    sock=[]                                #the actual socket binding
        
    address='127.0.0.1'                    #ip address.
    
    com=9999                               #com for the socket
    
    machine=print                          #algorithm machine or procedure
    
    speed=0.5                              #the duration for the machine to idle
    
    sock_thread=threading.Thread()
    
    timer=0
    

    

    '''
    Initialize the M_A_S_S, needs a property list and a machine.
    The property list is designed for this actual scenery, it would look like this:
    
       {
            'name'    : 'SERVER',
            'welcome' : 'Enjoy working with MASS.',
            'address' : '127.0.0.1',
            'com'     : 9999,
            'speed'   : 0.5
            
        }
    
    
    It is in fact a dictionary of Python. 
    
    Machine: an algorithm machine, which governs the receive-send cycle and 
    inner-function algorithm. 
    '''
    def __init__(self,plist,machine):
        self.plist=plist
        self.server_name=plist['name']
        self.server_welcome_string=plist['welcome']
        self.address=plist['address']
        self.com=plist['com']
        self.speed=plist['speed']
        self.time_out=plist['time']

        self.machine=machine
    
    '''
    Procedure for managing the initialization and sweeping of algorithm machine. 
    It is the entry for the inner algorithm machine.
    
    addr: the address of the connection.
    '''

    def linque_fn (self, sock, addr):
        print(self.server_name+':'+'Accept new connection from %s:%s...' % addr)
        sock.send(b'established')                   #connection acknowledge.
        self.machine(self)
        print (self.server_name+':'+'connection from %s:%s closed.' % addr)
        
    '''
    Bind the MASS to actual ip & com. The server should make sure the com is not
    in use.
    When a MASS is ready, a message of 'waiting for connection' should appear on 
    the screen.
    ip_addr: ip address.
    com: com.
    '''
    def sock_tcp_establish(self, ip_addr, com):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.time_out)

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #handle the error that "address is used."
        s.bind((ip_addr,com))                               #bind socket to this.
        s.listen(5)  

        print (self.server_name+':'+'waiting for connection...')
        return s
    
    '''
    Send words to the client. 
    The words must be in type of string. 
    
    sock: the socket to send to.
    string: the words to be sent.
    '''
    def speak_to_client(self, string):
        estring=string.encode('utf-8')
        try:
            self.sock.send(estring)
        except BrokenPipeError as err:
            print(self.server_name+': '+"Encounter BROKENPIPE!")
            self.sock.close()
            self.sock_thread._delete()


    def unbound_server(self):
        self.sock.close()


        
        
    '''
    Start the server process!
    When this function is called, the MASS is about to be put into actual use.
    The inner function linque_fn would handle the inner algorithm.
    Leave the socket work till an assignment is over.
    '''
    def start(self):

        if not self.sock_thread.isAlive():
            
            s=self.sock_tcp_establish(self.address, self.com)
            try:
                sock,addr=s.accept()
                self.sock=sock
                self.sock_thread=threading.Thread(target=self.linque_fn,args=(sock, addr),name='Server'+str(self.com))
                self.sock_thread.start()     #blocked till connection establishs
                
            except socket.timeout:
                print(self.server_name+': '+"Connection timeout, unbound.")



'''
################################################################################
Runtime environment of the transmission. The playground for MASSES.

env: A list of environment variables.
cmail: The host mailbox.
core_mail_binding: Pipe for communicating with core module.
MASSES: A list of MASSES.
################################################################################
'''


class transmit_env():    
    
    env=[]                  #preserved for config.
    
    cmail=[]

    core_mail_binding=[]
    
    MASSES=[]
    
    dispatcher_MASS=[]

    current_idling_com = []
    
    
    '''
    Connect the core pipe into this module and initialize the environment itself.
    Create the MASSES.
    
    core_mail: mailbox of the core module. 
    '''
    
    def __init__(self,core_mail):
        
        self.core_mail_binding=core_mail
        self.cmail=mailer.mailbox('transmitter',50)
        self.init_dispatcher_MASS()
        for pl in M_A_S_S_PLIST:
            self.MASSES.append(M_A_S_S(pl,self.machine))
        
    def init_dispatcher_MASS(self):
        self.dispatcher_MASS=M_A_S_S(DISPATCH_PLIST,self.com_dispatcher_machine)
        
    
    '''
    used in the tcp_server as message handler.
    interprete the command received by TCP/IP transmission.
    translate the command into list of messages
    the messages would then sent to the **core** module
    which would then handle that.
    
    cmd: commands received as string.
    MASS: the MASS on current work.
    
    '''
    
    def cmd_interpreter(self,cmd,MASS):
        sock=MASS.sock

        if cmd=='sayhello':
            self.cmail.send(self.cmail,MASS.speak_to_client,'hello')
        elif cmd=='name':
            self.cmail.send(self.cmail,MASS.speak_to_client,\
                            MASS.server_name)
        elif cmd=='welcome me':
            self.cmail.send(self.cmail,MASS.speak_to_client,\
                            MASS.server_welcome_string)
        elif cmd=='fortune':
            self.cmail.send(self.cmail,MASS.speak_to_client,\
                            os.popen('fortune').read())
        else:
            self.cmail.send(self.cmail, MASS.speak_to_client,\
                            'ERROR LANG: '+cmd)  ##error: unrecognized command
            
    
    '''
    Algorithm machine. Controls how the MASS works.
    Consumes the env and the MASS. 
    The MASS can be distributive but the mailer is unique to the env, so the
    machine must have connection to the environment itself.
        
    MASS: the current working MASS
    '''

    def machine(self,MASS):
        sock=MASS.sock
        #print (sock)
        while True:
            '''
            Wait for the command from clients.
            Will block thread.
            '''
            data=MASS.sock.recv(1024)         
               
               
                
            time.sleep(MASS.speed)          #this sleep time is essential.
            ddata=data.decode('utf-8')
            
            if(ddata=='exit'):       #this command'd not be sent to interpreter.
                MASS.speak_to_client('closed')
                MASS.unbound_server()        #close the sock.
                self.init_dispatcher_MASS()
                
                return 0
            else:                    #push the command into the interpreter.
                self.cmd_interpreter(ddata, MASS)
                
            self.cmail.display_mails()
            self.cmail.read_all()    #execute all the mails.
            


    '''
    In need of automatic com matching, this machine must be introduced. 
    Could be seen as the daemon of the actual algorithm machine.
    This machine would flash out before any actual machine appears, returning
    the address of whom the server idles. And our client would bind themselves 
    to the idling server, then the connection can be established.
    
    The machine won't care for what the client prompts, it just returns the name
    of idling server and close.
    This should take a short time.
    '''
    def com_dispatcher_machine(self, MASS):
        sock=MASS.sock
        print(MASS.server_name+': '+'COM_DISPATCHER_MACHINE IS RUNNING.')
        time.sleep(MASS.speed)
        cic=str(self.current_idling_com)
        print('DISPATCHER: DISPATCHING TO COM: '+cic)
        MASS.speak_to_client(cic)
        return 
    
    
    def monitor_terminal(self):
        print('')
        print('Current working servers:')
        isfound=False
        for mass in self.MASSES:
            if mass.sock_thread.isAlive():
                print (mass.server_name)
                isfound=True
        if isfound==False:
            print('None.')
        print('')        
        print ('Current idling servers:')
        for mass in self.MASSES:
            if (not mass.sock_thread.isAlive()):
                print(mass.server_name)
        print('')
        
    
    
        
    '''
    Start the servers sequentially. 
    '''    
    def seq_start(self):
        def __seq_start():
            for mass in self.MASSES:
                if (not mass.sock_thread.isAlive()):
                    self.current_idling_com=mass.com
                    self.init_dispatcher_MASS()
                    self.dispatcher_MASS.start()
                    mass.start()
        while 1:
            __seq_start()
            time.sleep(2)
        __seq_start()


'''.....................testing and usage.......................................'''
    
a=transmit_env([])

'''  
Preserved for core module
'''
def __core():
    while True:
        if(platform.system() == 'Linux'):
            os.system("clear")          #clear terminal output
        elif(platform.system() == 'Windows'):
            os.system("cls")            #clear terminal output
        a.monitor_terminal()
        time.sleep(5)
        
        
threading.Thread(target=a.seq_start, args=()).start()
__core()




'''class for writing logs.'''

class transmit_logger():
    
    
    
    '''
    When a transmission error occured, this function would be called.
    Alter the environment variables sent to this function.
    Send error codes and messages to log file.
    ##
    error_code: error code.
    env: A list of environment variables. 
    ##
    '''
    
    def handle_transmission_error(env):
        pass


    '''
    design: Heranort
    Send transmission log to the log module.
    ##
    message: log message to be sent
    bad_p: predication of wether the message is normal or bad. 
           Will be delivered to differenet log files.
    lcode: log code to send.
    ##
    '''
    def send_transmit_log(message,bad_p,lcode):
        pass
    
  
