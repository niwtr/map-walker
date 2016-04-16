#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
Current version : 0.3
2016-3-26
by Heranort 
'''




import threading                                #for thread creation
import socket                                   #socket offical module
import time                                     #time official module

import os                                       #for fortune!

from mailer import mail
from mailer import mailbox
import platform                                 #judge the platform
import sys

from mass_plists import M_A_S_S_PLIST           #property list for MASSES
from mass_plists import DISPATCH_PLIST
from log import log_file                        #log object
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



def print(*c, end=''):log_file.info(*c)
def prinw(*c, end=''):log_file.warn(*c)

class M_A_S_S():
    

    plist=[]

    sock=[]                                #the actual socket binding

    address=[]                             #ip address bingding. generated below.
    
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

        self.address=socket.gethostbyname(socket.gethostname())
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
            prinw(self.server_name+': '+"Encounter BROKENPIPE!")
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
                prinw(self.server_name+': '+"Connection timeout, unbound.")



'''
################################################################################
Class definition of the packet transmitted between core module and transmitter.
We have to define such packet because we have to mark which MASS server is 
sending msgs and which MASS server should the reply mail be sent to .
Thus this class wraps:
1. the MASS binding for current server.
2. the request command, namely, the req.
3. the argument list, yeah it indeed is a tuple.

The request command can be interpreted by the interpreter in core module, and the
argument tuple can be applied to the function interpreted.
################################################################################
'''
class transmitter_packet():
    def __init__(self,MASS, func,args):
        self.MASS=MASS
        self.func=func
        self.args=args
        self.pipe=MASS.speak_to_client

    def eval_func(self):
        return self.func(*self.args)




'''
################################################################################
Runtime environment of the transmission. The playground for MASSES.

env: A list of environment variables.
cmail: The core mailbox.
core_mail_binding: Pipe for communicating with core module.
MASSES: A list of MASSES.
################################################################################
'''


class transmit_env():    

    current_idling_com = []
    

    '''
    Connect the core pipe into this module and initialize the environment itself.
    Create the MASSES.
    tmail: the mailbox owned by transmitter itself.
    cmail: mailbox of the core module. 
    env: left empty currently.
    '''

    def __init__(self,core_mail, interpreter):

        self.tmail=mailbox('transmitter',50)        
        self.cmail=core_mail
        self.interpreter=interpreter
        self.env=[]
        self.dispatcher_MASS=[]
        self.init_dispatcher_MASS()
        self.MASSES=[]
    
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
    
    In fact this is a message parser. it parses the message fetched from the 
    client and parse its structure. 
    
    For example the command
        mtp::[1,[2,3,4]]
    can be parsed into <request_command>:=mtp,
                       <argument_list>  :=[1,[2,3,4]]
    '''

        
    def cmd_evaluator(self,cmd,MASS):
        cmd=cmd.split('::')        #seperate the command by double-colons
        command=cmd[0]             #the first element should be command. 
        args=tuple(eval(cmd[1]))   #the argument list, tupled
        pkt=transmitter_packet(MASS,self.interpreter(command),args)   #pack up the message.
        return pkt
    
    def shutdown_MASS(self, com):
        isFound=False
        for mass in self.MASSES:
            if mass.com==com:
                if mass.sock_thread.isAlive():
                    mass.unbound_server()
                    self.init_dispatcher_MASS()                                        
                isFound=True
        return isFound

    '''
    Algorithm machine. Controls how the MASS works.
    Consumes the env and the MASS. 
    The MASS can be distributive but the mailer is unique to the env, so the
    machine must have connection to the environment itself.

    MASS: the current working MASS
    '''

    def machine(self,MASS):
        
        '''
        Wait for the core module to reply.
        Check for each mails in the mail list
        Return only on condition the mail toward current MASS was found.
        Remind that a transmitter environment can contain lots of MASSES
        and searching for the reply to a certain MASS is required
        because each MASS contains its own machine.
        The uniqueness is asured by the MASS itself. That for each MASS, 
        the function 'MASS.speak_to_client' is unique.
        That is the signiture for any of the MASS servers.
        For example: 
        
            class foo():
               def bar(self):
                  pass

            a=foo()
            b=foo()
            a.bar==b.bar     =>  False

        '''
        
        def wait_for_event():
            is_event_comming=False
            while not is_event_comming:
                for mails in self.tmail.maillist:
                    (fn, args)=mails('describe')
                    if fn==MASS.speak_to_client:
                        is_event_comming=True            

        while True:
            '''
            Wait for the command from clients.
            Will block thread.
            '''
	    
            try: 
                data=MASS.sock.recv(1024)         
		
            except OSError:
                break                       #Broken pipe, server shutted down 

		
            time.sleep(MASS.speed)          #this sleep time is essential.

            ddata=data.decode('utf-8')

            if not ddata:
                prinw(str(MASS.server_name)+': Encounter Brokenpipe.')
                break
                
            if(ddata=='exit'):              #this command'd not be sent to interpreter.
                MASS.speak_to_client('closed')
                MASS.unbound_server()       #close the sock.
                self.init_dispatcher_MASS()
                return 0
            else:                           #push the command into the interpreter.
                pkt=self.cmd_evaluator(ddata, MASS)
                self.tmail.send(self.cmail, lambda x:x, pkt)  
                                            #send the function prompt to the core.
                wait_for_event()            #wait for the respond of the core.
                


            self.tmail.pread_all()           #execute all the mails.



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


    def get_server_status(self):
        idling=[]
        working=[]
        for mass in self.MASSES:
            if mass.sock_thread.isAlive():
                working.append(mass.server_name)
            else:
                idling.append(mass.server_name)
                
        return {
                  'idling'  : idling,
                  'working' : working
                }
                
 
        
            

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


    





    