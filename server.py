import socket
import pickle
from boltons import socketutils
from PIL import ImageGrab
import os

server = ""
port = 12354

def takeScreenShot(buff):
    image = ImageGrab.grab()
    dump = pickle.dump(image)
    buff.sendall(len(dump) + b'\n')
    buff.sendall(dump)


# create socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((server, port))

    # start socket and wait to connect
    print("Starting Server!")
    s.listen()
    conn, addr = s.accept()
    print("Connected by: ", addr)


    buff = socketutils.BufferedSocket(conn, None)

    while True:
        flag = buff.recv_until(b':F:').decode()
        print(f'Receive: {flag}')
        
        if flag == 'screenshot':
            takeScreenShot(buff)

        