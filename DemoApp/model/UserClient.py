import socket
from threading import Thread

class UserClient :

    def __init__(self, interface):
        self.interface = interface
        self.username = ""
        self.HOST = 'localhost'
        self.PORT = 9009
        self.sock: socket.socket
        self.receiver: Thread
        self.is_connected: bool = False

    def rcvMsg(self, sock):
        save = []
        index = 0

        while True :
            try:
                data = sock.recv(1024)
                if not data:
                    break
                print(data.decode())
                decode_data = data.decode('utf-8')
                if not 'role:' in decode_data and not 'is join' in decode_data and not 'is quit' in decode_data:
                    save.append(decode_data)

                self.interface.send_log(decode_data+"\n")

                if 'is join' in decode_data :
                    splited_data:str = decode_data.split()
                    received_user = splited_data[0][1:-1]
                    if received_user != self.username :
                        self.interface.receive_other_user(received_user)

                elif 'has joined' in decode_data :
                    splited_data: str = decode_data.split()
                    received_user = splited_data[0][1:-1]
                    if received_user != self.username:
                        self.interface.receive_other_user(received_user)

                elif 'is quit' in decode_data :
                    splited_data: str = decode_data.split()
                    received_user = splited_data[0][1:-1]
                    if received_user != self.username:
                        self.interface.remove_other_user(received_user)

                else:
                    pass

            except:
                pass

    def connect(self, username : str):
        if self.is_connected is True :
            return

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))
        self.receiver = Thread(target=self.rcvMsg, args=(self.sock,))
        self.receiver.daemon = True
        self.receiver.start()

        self.username = username
        self.sock.send(("user " + username).encode())
        self.is_connected = True

    def disconnect(self):
        if self.is_connected is False:
            return

        self.sock.close()
        self.is_connected = False

    def submit(self, msg : str):
        self.sock.send(msg.encode())

