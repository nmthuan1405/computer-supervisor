import socket
from _thread import start_new_thread
import os
from io import BytesIO
from time import time

HOST = '0.0.0.0'
PORT = 5455
ThreadCount = 0

ServerSock = socket.socket()

try:
    ServerSock.bind((HOST,PORT))
except socket.error as e:
    print(str(e))

print('socket is listening')

ServerSock.listen(5)

def clientThread(connection,addr):
    full = b''
    while True:
        data = connection.recv(2048)
        if not data:
            break
        else:
            full += data
    connection.close()
    with open('images/{}{}.png'.format(addr,time()),'w+b') as f:
        f.write(full)
        print('Image Saved')

while True:
    Client,addr = ServerSock.accept()
    print('connected to {} : {}'.format(addr[0],addr[1]))
    start_new_thread(clientThread,(Client,addr))
    ThreadCount += 1
    print('Thread #{}'.format(ThreadCount))
ServerSock.close()
