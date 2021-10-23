from services.Socket import Socket
import threading

class Client(Socket, threading.Thread):
    def __init__(self, DELIM=b'\x00'):
        Socket.__init__(self, socket= None, DELIM=DELIM)
        threading.Thread.__init__(self, name="client")
