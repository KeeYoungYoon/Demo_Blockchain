from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLineEdit, QTextEdit, QLabel, QHBoxLayout, QPushButton, QFrame, QScrollArea, \
    QVBoxLayout, QComboBox

from viewModel.MinerInterface import MinerInterface

class MinerTab(QWidget):

    log_signal = pyqtSignal(str)

    def __init__(self):

        super().__init__()
        self.interface = MinerInterface(self)

        self.from_line = QLineEdit(self)

        self.scroll_text = QTextEdit(self)
        self.scroll_text.setReadOnly(True)

        self.log: str = ""
        self.log_signal.connect(self.receive_log)

        self.initUI()

    @pyqtSlot(str)
    def receive_log(self, new_log:str):
        self.log += new_log
        self.scroll_text.setText(self.log)

    def connect(self):
        self.interface.connect(self.from_line.text())

    def disconnect(self):
        self.interface.disconnect()

    def initUI(self):

        from_label = QLabel('Miner : ', self)
        connect_button = QPushButton("Connect")
        connect_button.clicked.connect(self.connect)
        disconnect_button = QPushButton("Disconnect")
        disconnect_button.clicked.connect(self.disconnect)
        from_box = QHBoxLayout()
        from_box.addWidget(from_label)
        from_box.addStretch(1)
        from_box.addWidget(self.from_line)
        from_box.addWidget(connect_button)
        from_box.addWidget(disconnect_button)

        split_line1 = QFrame()
        split_line1.setFrameShape(QFrame.HLine)

        log_label = QLabel('Log')
        log_box = QHBoxLayout()
        log_box.addWidget(log_label)

        scroll = QScrollArea()
        scroll.setWidget(self.scroll_text)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(200)

        vbox = QVBoxLayout()
        vbox.addLayout(from_box)
        vbox.addWidget(split_line1)
        vbox.addLayout(log_box)
        vbox.addWidget(scroll)

        self.setLayout(vbox)
