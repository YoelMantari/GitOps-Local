import socket
from collections import deque
import sys

# Una cola dummy (un proceso Python que escuche en un puerto local).

ip = sys.argv[1]
puerto = int(sys.argv[2])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((ip, puerto))
s.listen()
cola = deque()
while True:
    conn, addr = s.accept()
    print(f"Conexion establecida")
    while True:
        data = conn.recv(1024).decode().strip()
        if data == 'GET' :
            conn.sendall(f"Mensajes en la cola: {cola}\n".encode())
        else:
            cola.append(data.strip())
            conn.sendall(f"Se agrego: '{data}' a la cola\n".encode())
