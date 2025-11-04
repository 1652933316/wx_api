from PyQt5.QtWidgets import QMainWindow, QWidget
from main_windows import Ui_wechat_ai
from child_windows import Ui_set


class Main(Ui_wechat_ai):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)

    def Open(self):
        self.show()

class Child(QMainWindow,Ui_set):
    def __init__(self):
        super(Child, self).__init__()
        self.setupUi(self)
        # self.pushButton.clicked.connect(self.close)
    def Open(self, main):
        self.main = main
        self.show()
