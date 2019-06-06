import socketserver
from threading import Thread
import threading

import os

import model.Block as Block
import model.KeyGenerator as KeyGenerator
import model.ProofOfWork as ProofOfWork
import time

HOST = 'localhost' #Ip Blockchain server로 진행할 IP
PORT = 9009
lock = threading.Lock()

class UserManager:

    def __init__(self):
        self.users = {}

    def addUser(self, username, conn, addr):
        if username in self.users:
            conn.send('already registered \n'.encode())
            return None

        lock.acquire()
        self.users[username] = (conn, addr)
        lock.release()

        self.sendMessageToAll('[%s] is join.' % username)
        print('+++ Number of Participation [%d]' % len(self.users))

        return username

    def removeUser(self, username):
        if username not in self.users:
            return

        lock.acquire()
        del self.users[username]
        lock.release()

        self.sendMessageToAll('[%s] is quit.' % username)
        print('--- Number of Participation [%d]' % len(self.users))


    def sendMessageToAll(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())


class MyTcpHandler(socketserver.BaseRequestHandler):
    userman = UserManager()
    minerman = UserManager()

    def handle(self):
        server_interface.send_log('[%s] is connected\n' % self.client_address[0])
        global save
        save = []
        try:
            username = self.registerUsername()

            for user in self.userman.users :
                if user is not username :
                    self.request.send(("[%s] has joined." % user).encode())

            msg = self.request.recv(1024)

            while msg:
                data = msg.decode('utf-8')
                print(data)

                data_list = data.split(" ")

                if data_list[0] == username and data_list[1] in self.userman.users:
                    conn, addr = self.userman.users[data_list[1]]
                    #conn.send(data.encode())
                    save.append(data)
                    if len(save)%10 == 0:
                        for name in self.minerman.users:
                            conn, addr = self.minerman.users[name]
                            for i in range(0, 10):
                                tx = save[i]
                                print(tx)
                                conn.send(tx.encode())
                                time.sleep(0.01)
                            for i in range(10):
                                save.pop(0)
                            time.sleep(3)
                            server_interface.send_log('Block Received\n')
                            fr = open('block.txt', 'r')
                            server_interface.send_log('Successfully Opened Block\n')
                            last_dict = fr.readlines()[-1].rstrip()
                            hash, signature, public_key = Block.brick_hash(last_dict)
                            server_interface.send_log('Validation Process: ')
                            server_interface.send_log(str(KeyGenerator.validation(last_dict.encode('utf-8'), signature, KeyGenerator.readKey())) + " ")
                            server_interface.send_log('Send Block to Participants\n')
                            self.userman.sendMessageToAll('Validated Block Sent\n')
                            break
                    else:
                        conn.send(data.encode())
                else:
                    conn, addr = self.userman.users[username]
                    conn.send("Invalid transaction".encode())
                msg = self.request.recv(1024)

        except Exception as e:
            server_interface.send_log('in error\n')
            server_interface.send_log(str(e) + "\n")

        server_interface.send_log('[%s] Termination\n' % self.client_address[0])
        self.userman.removeUser(username)

    def registerUsername(self):
        while True:
            username = self.request.recv(1024)
            username = username.decode().split()
            role = username[0].strip()
            username = username[1].strip()

            if role == "user" :
                if self.userman.addUser(username, self.request, self.client_address):
                    return username

            elif role == "miner":
                if self.minerman.addUser(username, self.request, self.client_address):
                    return username


class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class Server :
    def __init__(self, interface):
        global server_interface
        server_interface = interface

    def run(self):
        self.server = ChatingServer((HOST, PORT), MyTcpHandler)
        self.th = Thread(target=self.server.serve_forever)
        self.th.daemon = True
        self.th.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
