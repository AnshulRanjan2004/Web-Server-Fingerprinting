import sys
import socket
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Web Server Fingerprinting")
        self.setGeometry(200, 200, 750, 650)
        self.setStyleSheet("""
            background-color: #FFFFFF;
        """)
        self.UiComponents()

    def UiComponents(self):
        self.label = QLabel(self)
        self.label.setGeometry(50, 50, 400, 40)
        self.label.setFont(QFont('Helvetica Neue', 16))
        self.label.setStyleSheet("""
            color: #333333;
        """)
        self.label.setText("Enter the URL:")

        self.server = QLineEdit(self)
        self.server.setGeometry(50, 100, 600, 60)
        self.server.setFont(QFont('Helvetica Neue', 14))
        self.server.setStyleSheet("""
            border: 2px solid #CCCCCC;
            border-radius: 10px;
            padding: 10px;
        """)

        self.button = QPushButton(self)
        self.button.setGeometry(300, 180, 100, 50)
        self.button.setFont(QFont('Helvetica Neue', 14))
        self.button.setStyleSheet("""
            background-color: #0066CC;
            color: #FFFFFF;
            border: none;
            border-radius: 10px;
            padding: 10px;
        """)
        self.button.setText("Get Info")
        self.button.clicked.connect(self.getInfo)
        self.resultLabel = QLabel(self)
        self.resultLabel.setGeometry(50, 235, 675, 450)
        self.resultLabel.setFont(QFont('Helvetica Neue', 14))
        self.resultLabel.setStyleSheet("""
            color: #333333;
        """)
        self.resultLabel.setWordWrap(True)

    def getInfo(self):
        server = self.server.text()

        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Get the local machine name
        host = "172.20.10.5"
        port = 65432

        client_socket.connect((host, port))
        client_socket.send(server.encode())
        response = client_socket.recv(1024)
        client_socket.close()
        self.resultLabel.setText(response.decode())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
