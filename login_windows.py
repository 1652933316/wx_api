import os
import sys
import json
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from get_mac import *

# 简单模拟用户数据库 (实际项目请使用真实数据库)
users = json.loads(requests.get("http://42.194.243.47:81/read_txt").text)


class RegisterWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 启用高 DPI 缩放支持
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

        self.setWindowTitle("注册")
        self.setFixedSize(300, 200)

        # 控件
        self.lbl_username = QLabel("用户名:")
        self.txt_username = QLineEdit()
        self.lbl_password = QLabel("密码:")
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.lbl_confirm = QLabel("确认密码:")
        self.txt_confirm = QLineEdit()
        self.txt_confirm.setEchoMode(QLineEdit.Password)
        self.btn_register = QPushButton("注册")
        self.btn_cancel = QPushButton("取消")

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.lbl_username)
        layout.addWidget(self.txt_username)
        layout.addWidget(self.lbl_password)
        layout.addWidget(self.txt_password)
        layout.addWidget(self.lbl_confirm)
        layout.addWidget(self.txt_confirm)

        # 按钮布局
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_register)
        btn_layout.addWidget(self.btn_cancel)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # 信号连接
        self.btn_register.clicked.connect(self.register)
        self.btn_cancel.clicked.connect(self.close)

    def register(self):
        username = self.txt_username.text().strip()
        password = self.txt_password.text().strip()
        confirm = self.txt_confirm.text().strip()

        # 输入验证
        if not username or not password:
            QMessageBox.warning(self, "错误", "用户名和密码不能为空")
            return

        if password != confirm:
            QMessageBox.warning(self, "错误", "两次密码输入不一致")
            return

        if username in users:
            QMessageBox.warning(self, "错误", "用户名已存在")
            return

        # 注册成功
        users[username] = {"password": password}
        QMessageBox.information(self, "成功", "注册成功！")
        self.close()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("登录")
        self.setFixedSize(300, 150)

        # 控件
        self.lbl_username = QLabel("用户名:")
        self.txt_username = QLineEdit()
        self.lbl_password = QLabel("密码:")
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.btn_login = QPushButton("登录")
        self.btn_register = QPushButton("注册账号")

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.lbl_username)
        layout.addWidget(self.txt_username)
        layout.addWidget(self.lbl_password)
        layout.addWidget(self.txt_password)

        # 按钮布局
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_login)
        btn_layout.addWidget(self.btn_register)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # 信号连接
        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.show_register)

    def login(self):
        username = self.txt_username.text().strip()
        password = self.txt_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "错误", "请输入用户名和密码")
            return

        if username not in users:
            QMessageBox.warning(self, "错误", "用户名不存在")
            return

        if users[username]['password'] != password:
            QMessageBox.warning(self, "错误", "密码错误")
            return

        mac_place = get_physical_mac()
        if not users[username].get("mac_place"):
            users[username]['mac_place'] = str(mac_place)
        else:
            if users[username].get("mac_place") != mac_place:
                QMessageBox.warning(self, "错误", "登录设备错误！")
                return
        try:
            # 发送 POST 请求并上传 JSON 数据
            response = requests.post(
                "http://42.194.243.47:81/write_txt",
                json=json.dumps(users),  # 自动设置 Content-Type 为 application/json
                timeout=10  # 设置超时时间为 10 秒
            )

            # 检查响应状态
            if response.status_code == 200:
                print("上传成功:", response.text)
            else:
                print(f"上传失败: HTTP {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            QMessageBox.warning(self, "错误", "登录设备错误！")
            raise
        except Exception as e:
            print(f"发生错误: {e}")
            QMessageBox.warning(self, "错误", "登录设备错误！")
            raise

        QMessageBox.information(self, "成功", f"欢迎回来，{username}！")
        # 这里可以跳转到主界面
        self.close()
        from main import Main,Child
        self.main = Main()
        self.child = Child()
        self.main.toolButton.clicked.connect(lambda: self.child.Open(self.main))
        self.main.Open()

    def show_register(self):
        register_window = RegisterWindow(self)
        register_window.exec_()


if __name__ == "__main__":
    # 启用高 DPI 支持
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())