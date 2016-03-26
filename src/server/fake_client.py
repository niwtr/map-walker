import socket
#get the com.
ds=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ds.connect(('127.0.0.1',9999))
print(ds.recv(1024).decode('utf-8'))
addr=int(ds.recv(1024).decode('utf-8'))
ds.close()
#establish

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1',addr))

print(s.recv(1024).decode('utf-8'))

def speak_to_server(s):
    
    
    
    while(1):
        print('SPEAK: ',end=''),
        str=input().encode('utf-8')
        s.send(str)
        dd=s.recv(1024).decode('utf-8')
        if(dd=='closed'):
            s.close()
            break
        else:
            print(dd)


speak_to_server(s)


