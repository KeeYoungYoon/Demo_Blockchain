from threading import Lock

from model.MinerClient import MinerClient


class MinerInterface:

    def __init__(self, tab):
        self.tab = tab
        self.client = MinerClient(self)
        self.lock = Lock()

    def send_log(self, msg : str):
        self.lock.acquire()
        self.tab.log_signal.emit(msg)
        self.lock.release()

    #UserTab에서 사용
    def connect(self, user : str):
        self.user = user
        self.client.connect(self.user)

    #UserTab에서 사용
    def disconnect(self):
        self.client.disconnect()
        self.send_log("[%s] is quit\n" % self.user)

