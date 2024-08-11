from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QTextEdit, QPushButton, QGroupBox
from PyQt6.QtCore import Qt
import sys


def createTextBoxWithClearButton(title: str, placeholderText: str = ''):
    group = QGroupBox(title)
    box = QVBoxLayout()

    textbox = QTextEdit()
    textbox.setReadOnly(True)
    textbox.setPlainText(placeholderText)
    textbox.setAlignment(Qt.AlignmentFlag.AlignLeft)

    box.addWidget(textbox)

    clearButton = QPushButton(text="Clear")

    clearButton.clicked.connect(lambda: textbox.clear())

    box.addWidget(clearButton)

    group.setLayout(box)

    return group, textbox

class CaptureOutput:
    def __init__(self, textDest):
        self.textDest = textDest
        
    def write(self, message: str):
        # use callback and print to normal stdout
        self.textDest(message)
        sys.__stdout__.write(message)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(750, 400)
        self.setWindowTitle('FoxBot by slimer37')

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setDirection(QVBoxLayout.Direction.LeftToRight)

        chatGroup, self.chatbox = createTextBoxWithClearButton("Chat")
        layout.addWidget(chatGroup)

        sysGroup, self.sysbox = createTextBoxWithClearButton("System")
        layout.addWidget(sysGroup)
        
        sys.stdout = CaptureOutput(self.sysbox.insertPlainText)
        sys.stderr = sys.stdout

app = QApplication(sys.argv)
    
def getwindow():
    window = Window()
    return window

def rungui(window: Window):
    window.show()
    return app.exec()
