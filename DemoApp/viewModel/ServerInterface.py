from threading import Lock

from model.Server import Server


class ServerInterface:

    def __init__(self, tab):
        self.tab = tab
        self.server = Server(self)
        self.lock = Lock()

    def send_log(self, msg : str):
        self.lock.acquire()
        self.tab.log_signal.emit(msg)
        self.lock.release()

    #UserTab에서 사용
    def run(self):
        self.server.run()

    #UserTab에서 사용
    def stop(self):
        self.server.stop()

