from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLineEdit, QTextEdit, QLabel, QHBoxLayout, QPushButton, QFrame, QScrollArea, \
    QVBoxLayout, QComboBox

from viewModel.UserInterface import UserInterface

class UserTab(QWidget):

    log_signal = pyqtSignal(str)

    def __init__(self):

        super().__init__()
        self.interface = UserInterface(self)

        self.from_line = QLineEdit(self)
        self.to_combo = QComboBox(self)
        self.data_line = QLineEdit(self)
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

    def submit(self):
        self.interface.submit(self.to_combo.currentText(), self.data_line.text())

    def receive_other_user(self, other_user: str):
        self.to_combo.addItem(other_user)
        # UserTab에서 다른 User 목록 갱신

    # Client에서 사용
    def remove_other_user(self, other_user: str):
        index = self.to_combo.findText(other_user)
        self.to_combo.removeItem(index)

    def initUI(self):

        from_label = QLabel('From : ', self)
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

        to_label = QLabel('To    : ', self)
        to_box = QHBoxLayout()
        to_box.addWidget(to_label)
        to_box.addStretch(1)
        to_box.addWidget(self.to_combo)

        data_label = QLabel('Data : ', self)
        data_box = QHBoxLayout()
        data_box.addWidget(data_label)
        data_box.addStretch(1)
        data_box.addWidget(self.data_line)

        submit_button = QPushButton(self)
        submit_button.setText("Submit")
        submit_button.clicked.connect(self.submit)
        submit_box = QHBoxLayout()
        submit_box.addWidget(submit_button)

        split_line2 = QFrame()
        split_line2.setFrameShape(QFrame.HLine)

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
        vbox.addLayout(to_box)
        vbox.addLayout(data_box)
        vbox.addLayout(submit_box)
        vbox.addWidget(split_line2)
        vbox.addLayout(log_box)
        vbox.addWidget(scroll)

        self.setLayout(vbox)
