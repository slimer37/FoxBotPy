from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QTextEdit, QPushButton, QGroupBox, QHBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase
import sys


def createTextBoxWithClearButton(title: str, sizeFactor: int):
    group = QGroupBox(title)
    
    group.setStyleSheet('font-family: "Rowdies"; font-weight: 300')
        
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
    
    textbox.setStyleSheet("""
QTextEdit {
    background-color: #2b065c;
    color: #E1F7F5;
    border: none;
    outline: none;
}
""")
    
    clearButton.setStyleSheet("""
QPushButton
{
    color: #1E0342;
    font-weight: 300;
    border: none;
    background-color: #E1F7F5;
}

QPushButton:pressed
{
    background-color: #c3d9d7;
}
""")

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
        
        self.setStyleSheet('background-color: #1E0342; color: #f4ff7f')
        
        vlayout = QVBoxLayout()
        self.setLayout(vlayout)
        
        label = QLabel("FoxBot Control Panel")
        label.setStyleSheet('font-family: "Rowdies"; font-weight: 700;')
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

import os

if getattr(sys, 'frozen', False):
    path = os.path.join(sys._MEIPASS, "Rowdies")
else:
    path = "Rowdies"

for weight in ["Regular", "Light", "Bold"]:
    fontfile = f"Rowdies-{weight}.ttf"
    QFontDatabase.addApplicationFont(os.path.join(path, fontfile))
    print(f"Loaded {fontfile}")

def getwindow():
    window = Window()
    return window

def rungui(window: Window):
    window.show()
    return app.exec()
