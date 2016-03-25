import threading
import socket
import time

#mail
import mailer

#log module
#import log

#from router import router_bindings


'''
################################################################################
Modularized Abstract Socket Server (MASS) for TCP linking, and server environment
Authorized by Herathol Nortzor
First published: 2016-3-10
################################################################################
'''




'''
################################################################################
Modularized Abstract Socket Server class.

'''



class M_A_S_S():
    
    server_name='SERVER'
    
    server_welcome_string='Enjoy working with MASS.'
    
    sock=[]
        
    address='127.0.0.1'
    
    com=9999
    
    machine=print
    
    def __init__(self,plist,machine):
        self.server_name=plist['name']
        self.server_welcome_string=plist['welcome']
        self.address=plist['address']
        self.com=plist['com']
        self.machine=machine
        pass

    
        
     #function for managing the link between S and C
    def linque_fn (self, sock, addr ,machine):
        print(self.server_name+':'+'Accept new connection from %s:%s...' % addr)
        sock.send(b'established') #connection acknowledge.
        machine(sock)            
        print (self.server_name+':'+'connection from %s:%s closed.' % addr)
    
    def sock_tcp_establish(self, ip_addr, com):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #bind socket to this.
        s.bind((ip_addr,com))
        #upto five clients.
        s.listen(5)  
        #welcome sentences...
        print (self.server_name+':'+'waiting for connection...')
        return s
    
 
        
    def speak_to_client(self, sock, string):
        estring=string.encode('utf-8')
        sock.send(estring)
        
        
     ##no method for closing a thread?   
    def start(self):
        s=self.sock_tcp_establish(self.address, self.com)
        sock,addr=s.accept()
        self.sock=sock
        t=threading.Thread(target=self.linque_fn,args=(sock,addr,self.machine))
        t.start()   





'''
################################################################################
'''


'''
Runtime environment of the transmission.
##
##
%%
env: A list of environment variables.
core_mail_binding: pipe for communicating with core module.
sock: a socket.
%%


'''


class transmit_env(M_A_S_S):    
    
    env=[]  #preserved for config.
    
    cmail=[]

    core_mail_binding=[]
    
    s1=s2=[]
    
    #speed=[]
    default_MASS_plist={
        
        'name'    : 'SERVER',
        'welcome' : 'Enjoy working with MASS.',
        'address' : '127.0.0.1',
        'com'     : 9999,
        
    }
    default2_MASS_plist={
    
        'name'    : 'SERVER',
        'welcome' : 'Enjoy working with MASS.',
        'address' : '127.0.0.1',
        'com'     : 9990,
    
    }        

    def the_env(self):
        return self
    
    '''
    connect the core pipe into this module and initialize the environment itself.
    ##
    mail: mailer of the core.
    ##
    '''
    def __init__(self,core_mail):
        
        self.core_mail_binding=core_mail
        self.cmail=mailer.mailbox('transmitter',50)
        
        self.s1=M_A_S_S(self.default_MASS_plist,self.machine)
        self.s2=M_A_S_S(self.default2_MASS_plist,self.machine)        
    
    '''
    used in the tcp_server as message handler.
    interprete the command received by TCP/IP transmission.
    translate the command into list of messages
    the messages would then sent to the **core** module
    which would then handle that.
    
    ##
    cmd: commands received as string.
    ##
    
    '''
    
    def cmd_interpreter(self,cmd,sock):
        
        if cmd=='sayhello':
            self.cmail.send(self.cmail,self.speak_to_client,sock,'hello?')
        else:
            self.cmail.send(self.cmail, self.speak_to_client,sock,'erl')  ##error: unrecognized command
    

    def machine(self,sock):
        print (sock)
        while True:
            data=sock.recv(1024) #maximum content of message
            time.sleep(0.5)  #essential time sleep
            ddata=data.decode('utf-8')
            
            if(ddata=='exit'):
                self.speak_to_client(sock, 'closed')
                sock.close()
                return 0
            else: 
                self.cmd_interpreter(ddata, sock)
                
            self.cmail.display_mails()
            self.cmail.read_all()




    
a=transmit_env([])

a.s1.start()
a.s2.start()


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
    
    def handle_transmission_error(error_code, env):
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
    
  