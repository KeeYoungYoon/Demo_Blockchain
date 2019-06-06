from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout

import sys
from view.UserTab import UserTab
from view.MinerTab import MinerTab
from view.ServerTab import ServerTab


class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        tabs = QTabWidget()
        tabs.addTab(UserTab(), 'User')
        tabs.addTab(MinerTab(), 'Miner')
        tabs.addTab(ServerTab(), 'Server')

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