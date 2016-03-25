import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('127.0.0.1', 9997))
# 接收欢迎消息:
print(s.recv(1024).decode('utf-8'))

def speak_to_server(s):
    while(1):
        str=input().encode('utf-8')
        s.send(str)
        print(s.recv(1024).decode('utf-8'))


speak_to_server(s)

s.close()
