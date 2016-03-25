import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('127.0.0.1', 9990))
# 接收欢迎消息:
print(s.recv(1024).decode('utf-8'))

def speak_to_server(s):
    
    while(1):
        str=input().encode('utf-8')
        s.send(str)
        dd=s.recv(1024).decode('utf-8')
        if(dd=='closed'):
            s.close()
            break
        else:
            print(dd)


speak_to_server(s)


