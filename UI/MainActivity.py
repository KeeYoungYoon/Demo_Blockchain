import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox


class User :
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def getName(self):
        return self.name

    def getBalance(self):
        return self.balance

    def checkBalance(self, variation):
        return self.balance + variation >= 0

    def changeBalance(self, variation):
        if self.checkBalance(variation) :
            self.balance += variation
            return True
        return False

class Transaction :

    def __init__(self, receiver:User, sendor:User, amount):
        self.receiver = receiver
        self.sendor = sendor
        if sendor.checkBalance(-amount) and receiver.checkBalance(+amount) :
            sendor.changeBalance(-amount)
            receiver.changeBalance(amount)
            self.amount = amount

    def toString(self) -> str :
        ret = "Sendor : " + self.sendor.getName() + "\n"
        ret += "Receiver : " + self.receiver.getName() + "\n"
        ret += "Amount : " + self.amount + "\n"
        ret += "Sendor Balance : " + (self.amount + self.sendor.getBalance())
        ret += " -> " + self.sendor.getBalance() + "\n"
        ret += "Receiver Balance : " + self.receiver.getBalance()
        ret += " -> " + (self.receiver.getBalance() + self.amount) + "\n"
        return ret

class UserTab(QWidget) :
    def __init__(self, userlist):
        super().__init__()
        self.userlist = userlist
        self.initUI()

    def initUI(self):
        
        sendor_label = QLabel('Sendor : ', self)
        sendor_candidate = QComboBox(self)
        for user in self.userlist:
            sendor_candidate.addItem(user.name, user)
        sendor_box = QHBoxLayout()
        sendor_box.addWidget(sendor_label)
        sendor_box.addWidget(sendor_candidate)

        receiver_label = QLabel('Receiver : ', self)
        receiver_candidate = QComboBox(self)
        for user in self.userlist:
            receiver_candidate.addItem(user.name, user)
        receiver_box = QHBoxLayout()
        receiver_box.addWidget(receiver_label)
        receiver_box.addWidget(receiver_candidate)

        vbox = QVBoxLayout()
        vbox.addLayout(sendor_box)
        vbox.addLayout(receiver_box)
        self.setLayout(vbox)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def makeUserList(self):
        list = [User("Apple", 50000), User("Banana", 100000), User("Carrot", 80880)]
        return list


    def initUI(self):

        userlist = self.makeUserList()

        tabs = QTabWidget()
        tabs.addTab(UserTab(userlist), 'User')
        tabs.addTab(QWidget(), 'Miner')

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)

        self.setLayout(vbox)

        self.setWindowTitle('My First Application')
        self.move(300, 300)
        self.resize(400, 200)
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())