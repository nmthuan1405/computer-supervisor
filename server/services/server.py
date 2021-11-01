from services.Socket import Socket
import socket
import threading
import queue

ADDRESS = ""
PORT    = 1234

class Server(threading.Thread):
    def __init__(self):
        super().__init__(name="server")

        self.ui_queue = None
        self.socket_queue = queue.Queue()
        self.socket = None
        self.clients = []

        self.add_client_thread = None

    def add_ui_queue(self, ui_queue):
        self.ui_queue = ui_queue
    
    def ui_cmd(self, cmd, ext = None):
        self.ui_queue.put((cmd, ext))

    def start_socket(self):
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(1)
        self.socket.bind((ADDRESS, PORT))
        self.socket.listen()

        self.add_client_thread = add_client(self.socket, self.clients)
        self.add_client_thread.start()

    def stop_socket(self):
        for client in self.clients:
            if client.is_alive():
                client.stop()

        self.socket.close()
        self.add_client_thread.join()

    def task_start(self):
        try:
            self.start_socket()
        except:
            self.ui_cmd("err", "cannot start")
            self.ui_cmd("start")
        else:
            self.ui_cmd("stop")

    def task_stop(self):
        try:
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
                self.task_start()
            elif cmd == "stop":    
                self.task_stop()


class add_client(threading.Thread):
    def __init__(self, socket, clients):
        super().__init__(name="add_client")
        self.socket = socket
        self.clients = clients

    def run(self):
        while True:
            try:
                conn, addr = self.socket.accept()
                client = Client(conn, addr)
                self.clients.append(client)
                client.start()

            except socket.timeout:
                # DEBUG("add_client timeout")
                pass
            
            except:
                DEBUG("end add_client thread")
                break

class Client(Socket, threading.Thread):
    def __init__(self, socket, addr, DELIM=b'\x00'):
        Socket.__init__(self, socket=socket, DELIM=DELIM)
        threading.Thread.__init__(self, name=addr)
        DEBUG("new client", addr)

    def stop(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except:
            DEBUG("ERR when stop", self.name)
        finally:
            DEBUG("remove client", self.name)
    
    def run(self):
        while True:
            flag = self.recv_str()
            DEBUG("received flag", flag)

            if flag == 'close':
                self.stop()
                break


def DEBUG(*args,**kwargs):
    print("Server:", *args,**kwargs)