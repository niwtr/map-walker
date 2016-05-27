#! /usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time
import threading
#get the com.

ip_address='119.29.232.198'#socket.gethostbyname(socket.gethostname())#'10.201.12.244'
ds=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ds.connect((ip_address,9999))
print(ds.recv(1024).decode('utf-8'))
addr=int(ds.recv(1024).decode('utf-8'))
ds.close()
#establish

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Addr:' +str(addr))
s.connect((ip_address,addr))

print(s.recv(1024).decode('utf-8'))
def listen(s,a):

    time.sleep(0.01)
    dd=s.recv(1024).decode('utf-8')
    if(dd=='closed'):
        s.close()
        return
    else:
        print(str(addr)+" "+time.asctime()+" get response to "+str(a)+": ", end="")
        print(dd)        
            
def speak_to_server(s):
  
    
    a=2
    #threading.Thread(target=listen,args=(s))
    while(1):
        
        if a>4:
            a=2
        else: pass
        time.sleep(0.01)

        dd=[]
        STR=str("echo::"+str(["hello, world"])).encode('utf-8')
  
        
        if (1):##str
            s.sendall(STR)
            listen(s,a)
                
        else:
            print('No inputs. Type again.')    

        a=a+1



speak_to_server(s)


