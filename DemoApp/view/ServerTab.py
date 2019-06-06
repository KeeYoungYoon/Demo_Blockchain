from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLineEdit, QTextEdit, QLabel, QHBoxLayout, QPushButton, QFrame, QScrollArea, \
    QVBoxLayout, QComboBox

from viewModel.ServerInterface import ServerInterface

class ServerTab(QWidget):

    log_signal = pyqtSignal(str)

    def __init__(self):

        super().__init__()
        self.interface = ServerInterface(self)

        self.scroll_text = QTextEdit(self)
        self.scroll_text.setReadOnly(True)

        self.log: str = ""
        self.log_signal.connect(self.receive_log)

        self.initUI()

    @pyqtSlot(str)
    def receive_log(self, new_log:str):
        self.log += new_log
        self.scroll_text.setText(self.log)

    def run(self):
        self.interface.run()

    def stop(self):
        self.interface.stop()

    def initUI(self):

        connect_button = QPushButton("Run")
        connect_button.clicked.connect(self.run)
        disconnect_button = QPushButton("Stop")
        disconnect_button.clicked.connect(self.stop)
        from_box = QHBoxLayout()
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
