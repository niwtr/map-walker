
#TCP_IP
import transmitter_tcp_server
#log module
import log






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
def cmd_interpreter(cmd):
    pass



'''
Runtime environment of the transmission.
##
##
%%
env: A list of environment variables.
cpipe: pipe for communicating with core module.
%%


'''
class transmit_environment():
    
    
    env=[]
    cpipe=[]

    
    '''
    init the environment and get ready for the connection.
    ##
    config: configure options.
    ##
    '''
    def init_environment(config):
        pass
    
    '''
    connect the core pipe into this module and initialize the environment itself.
    ##
    mail: mailer of the core.
    ##
    '''
    def __init__(self, mail):
        pass
    
    
    

    
    
    '''
    establish connection and get into transmission loop.
    '''    
    def transmission_loop():
        pass
    
    


'''class for writing logs.'''

class transmit_logger(transmit_environment):
    
    
    
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
    
    
