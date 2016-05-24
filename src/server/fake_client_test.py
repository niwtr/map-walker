#! /usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time
#get the com.

ip_address=socket.gethostbyname(socket.gethostname())#'10.201.12.244'
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

def speak_to_server(s):
    
    
    a=2
    while(1):
        
        if a>4:
            a=2
        else: pass
        time.sleep(0.01)
       # print('SPEAK: ',end=''),
        dd=[]
        #str=input().encode('utf-8')
        STR=str("query::"+str([1,a,2,0])).encode('utf-8')
        if (1):##str
            s.sendall(STR)
            
            dd=s.recv(1024).decode('utf-8')
            if(dd=='closed'):
                s.close()
                break
            else:
                print(str(addr)+time.asctime()+" get response to "+str(a)+": ", end="")
                print(dd)
                
                
        else:
            print('No inputs. Type again.')    

        a=a+1



speak_to_server(s)


