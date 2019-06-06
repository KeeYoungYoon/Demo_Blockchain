import socketserver
import threading

import os

import txManager
import Block
import KeyGenerator
import ProofOfWork
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

    def handle(self):
        print('[%s] is connected' % self.client_address[0])
        save = []
        try:
            username = self.registerUsername()
            msg = self.request.recv(1024)

            while msg:
                data = msg.decode('utf-8')
                print(data)
                save.append(data)
                if len(save)%10 == 0:

                    for name in self.userman.users:
                        if "miner" in name:
                            conn, addr = self.userman.users[name]
                            for i in range(0, 10):
                                tx = save[i]
                                print(tx)
                                conn.send(tx.encode())
                                time.sleep(0.01)
                            print('Block Received')#새로 추가된 부분 시작
                            fr = open('block.txt', 'r')
                            print('Successfully Opened Block')
                            last_dict = fr.readlines()[-1].rstrip()
                            hash, signature, public_key = Block.brick_hash(last_dict)
                            print('Validation Process: ',KeyGenerator.validation(last_dict.encode('utf-8'), signature,KeyGenerator.readKey()))
                            print('Send Block to Participants')
                            self.userman.sendMessageToAll('Validated Block Sent')#여
                            #validation
                                #for j in range(100):
                                #    continue
                                #save.pop(0)
                               # print(tx)
                                #conn.send(tx.encode())
                            break

                msg = self.request.recv(1024)
#                print(msg.decode())
#                if self.userman.messageHandler(username, msg.decode()) == -1:
#                    self.request.close()
#                    break
#                msg = self.request.recv(1024)
#                data = msg.decode('utf-8')
#                if data == "bc":
#                    if os.path.isfile("key.pem") ==False:
#                        KeyGenerator.create_key()
#                    print("block!")
#                    f = open('chat.txt', 'a+t')
#                    f.writelines(str(save))
#                    f.write('\n')
#                    pow =  ProofOfWork.pow()
#                    if pow == True:
#                        Block.brick()
#                        break
#                else:
#                    print(data)
#                    save.append(data)
#                data = msg.decode('utf-8')
#                self.sendMessageToAll(data)
#                msg = self.request.recv(1024)

        except Exception as e:
            print('in error')
            print(e)

        print('[%s] Termination' % self.client_address[0])
        self.userman.removeUser(username)

    def registerUsername(self):
        while True:
            self.request.send('role:'.encode())
            username = self.request.recv(1024)
            username = username.decode().strip()
            if self.userman.addUser(username, self.request, self.client_address):
                return username


class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def runServer():
    try:
        server = ChatingServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()


runServer()
