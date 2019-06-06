import socket
from threading import Thread

import model.Block as Block
import model.KeyGenerator as KeyGenerator
import model.ProofOfWork as ProofOfWork
import datetime
import time

from viewModel import UserInterface
from viewModel import MinerInterface

HOST = 'localhost'
PORT = 9009
username = ""

def rcvMsg(sock):
    save = []
    index = 0
    global username

    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode())
            decode_data = data.decode('utf-8')
            if not 'role:' in decode_data and not 'is join' in decode_data and not 'is quit' in decode_data:
                save.append(decode_data)

            if username == "miner1" and len(save) == 10:
                f = open('chat.txt', 'a+t')
                f.writelines(str(save))
                f.write('\n')
                f.close()
                pow = ProofOfWork.pow()
                index = Block.brick(pow, index)
                index = index+1
                for i in range (10):
                    save.pop()

        except:
            pass


def runChat():
    global username
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        t = Thread(target=rcvMsg, args=(sock,))
        t.daemon = True
        t.start()

        username = input()
        sock.send(username.encode())

        while True:
            msg = input()
            if msg == "exit" :
                break
            msg = msg + " " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            sock.send(msg.encode())



