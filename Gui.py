import sys
import requests
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Web Server Fingerprinting Tool")
        self.setGeometry(200, 200, 500, 600)
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
        self.label.setText("Enter server name:")

        self.server = QLineEdit(self)
        self.server.setGeometry(50, 100, 400, 60)
        self.server.setFont(QFont('Helvetica Neue', 14))
        self.server.setStyleSheet("""
            border: 2px solid #CCCCCC;
            border-radius: 10px;
            padding: 10px;
        """)

        self.button = QPushButton(self)
        self.button.setGeometry(200, 180, 100, 40)
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
        self.resultLabel.setGeometry(50, 240, 400, 450)
        self.resultLabel.setFont(QFont('Helvetica Neue', 14))
        self.resultLabel.setStyleSheet("""
            color: #333333;
        """)
        self.resultLabel.setWordWrap(True)

    def getInfo(self):
        server = self.server.text()

        req = requests.get('http://www.' + server)
        result = ""

        result += "<strong>Banner Grab</strong><br>"
        result += str(req.headers).replace('\n', '<br>') + "<br><br>" 

        some_headers = ['Server', 'Date', 'Via', 'X-Powered-By', 'ETag']
        for header in some_headers:
            try:
                result += "<strong>" + header + "</strong> : " + req.headers[header] + "<br>"
            except:
                result += "<strong>" + header + "</strong> : Not found<br>"

        try:
            result += "<br><strong>Probable Server Type</strong><br>"
            data = list(req.headers)
            for i in range(len(data)):
                if(data[i]=='Date' or data[i]=='date'):
                    d=i
                if(data[i]=='Server' or data[i]=='server'):
                    s=i

            if(d>s):
                result += "Might be Apache<br><br>"
            else:
                result += "Might be IIS/Netscape<br><br>"
        except:
            result += "Could not find probable server type<br>"

        self.resultLabel.setText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
