from socket import *

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

s = socket(AF_INET, SOCK_STREAM)
s.bind(ADDR)


# s.connect(("example.com", 80))
# request = "GET / HTTP/1.0\r\nHost:example.com\r\n\r\n"
# s.send(request.encode())
# data = s.recv(10000)
# print(repr(data))
# s.close()