import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.bind(("127.0.0.1", 1234))
s.listen()
conn, addr = s.accept()