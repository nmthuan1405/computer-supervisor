from services.Socket import Socket
import socket
import threading
import queue

PORT = 1234

class Client(Socket, threading.Thread):
    def __init__(self, DELIM=b'\x00'):
        Socket.__init__(self, socket= None, DELIM=DELIM)
        threading.Thread.__init__(self, name="client")

        self.ui_queue = None
        self.socket_queue = queue.Queue()

    def add_ui_queue(self, ui_queue):
        self.ui_queue = ui_queue
    
    def ui_cmd(self, cmd, ext = None):
        self.ui_queue.put((cmd, ext))

    def start_socket(self, SERVER):
        self.socket = socket.socket()
        self.socket.connect((SERVER, PORT))

    def stop_socket(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except:
            pass

    def task_start(self, ip):
        try:
            self.start_socket(ip)
        except:
            self.ui_cmd("err", "cannot start")
            self.ui_cmd("start")
        else:
            self.ui_cmd("stop")

    def task_stop(self):
        try:
            self.send_str("close")
            self.stop_socket()
        except:
            DEBUG("ERR when stop socket")
        finally:
            self.ui_cmd("start")

    def run(self):
        while True:
            task = self.socket_queue.get()
            DEBUG("task", task)

            cmd, ext = task
            if cmd == "exit":
                break
            elif cmd == "start":
                self.task_start(ext)
            elif cmd == "stop":    
                self.task_stop()


def DEBUG(*args,**kwargs):
    print("Client:", *args,**kwargs)