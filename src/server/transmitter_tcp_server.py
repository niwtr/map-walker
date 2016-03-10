'''
Modularized Abstract Socket Server (MASS) for TCP linking 
Authorized by Herathol Nortzor
First published: 2016-3-10
'''


import threading
import socket
import time



##inner algorithm function.
##rewrite this function and pass that to sock_tcp_connection in actual usage!
def func (x):
    return x

#function for managing the link between S and C
def linque_fn (sock,addr,fn):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'established') #connection acknowledge.
    while True:
        data=sock.recv(1024) #maximum content of message
        time.sleep(1)  #essential time sleep
        if data.decode('utf-8')=='over': #exit when receive command 'over'
            break
        sock.send(('%s' % fn(data).decode('utf-8')).encode('utf-8'))  #sending the compution result to client.
    sock.close()
    print ('connection from %s:%s closed.' % addr)

def sock_tcp_establish(ip_addr, com):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #bind socket to this.
    s.bind((ip_addr,com))
    #upto five clients.
    s.listen(5)  
    #welcome sentences...
    print ('waiting for connection...')
    return s

def sock_tcp_connection_loop (s,fn):
    while True:
        sock,addr=s.accept()
        t=threading.Thread(target=linque_fn,args=(sock,addr,fn))
        t.start()
    


#usage
sock_tcp_connection_loop(sock_tcp_establish('127.0.0.1',9999), func)