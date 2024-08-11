from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QTextEdit, QPushButton, QGroupBox, QHBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt
import sys


def createTextBoxWithClearButton(title: str, sizeFactor: int):
    group = QGroupBox(title)
        
    sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
    sizePolicy.setHorizontalStretch(sizeFactor)
    
    group.setSizePolicy(sizePolicy)
    
    box = QVBoxLayout()

    textbox = QTextEdit()
    textbox.setReadOnly(True)
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
        self.resize(800, 400)
        self.setWindowTitle('FoxBot by slimer37')
        
        vlayout = QVBoxLayout()
        self.setLayout(vlayout)
        
        label = QLabel("FoxBot Control Panel")
        vlayout.addWidget(label)
        
        vlayout.addWidget(label)

        layout = QHBoxLayout()

        chatGroup, self.chatbox = createTextBoxWithClearButton("Chat", 3)
        layout.addWidget(chatGroup)

        sysGroup, self.sysbox = createTextBoxWithClearButton("System", 2)
        layout.addWidget(sysGroup)
        
        vlayout.addLayout(layout)
        
        sys.stdout = CaptureOutput(self.sysbox.insertPlainText)

app = QApplication(sys.argv)
    
def getwindow():
    window = Window()
    return window

def rungui(window: Window):
    window.show()
    return app.exec()
