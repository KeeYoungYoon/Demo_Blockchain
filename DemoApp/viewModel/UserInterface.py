from threading import Lock

from viewModel.Transaction import Transaction

from model.UserClient import UserClient


class UserInterface:

    def __init__(self, tab):
        self.tab = tab
        self.client = UserClient(self)
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

    # Client에서 사용
    def receive_other_user(self, other_user: str):
        self.tab.receive_other_user(other_user)

    # Client에서 사용
    def remove_other_user(self, other_user: str):
        self.tab.remove_other_user(other_user)

    # UserTab에서 사용
    def submit(self, to:str, data:str):
        transaction = Transaction(self.user, to, data)
        self.client.submit(transaction.msg())
        self.send_log("-----send Transection to Server-----\n" +
                        transaction.toString() +
                     "------------------------------------\n")

