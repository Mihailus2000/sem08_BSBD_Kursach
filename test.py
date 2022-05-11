from PyQt5.QtWidgets import QWidget, QApplication, QStackedWidget, QPushButton, QTableWidget, QTableWidgetItem, \
    QStyledItemDelegate, QDialog, QMainWindow, QVBoxLayout, QLabel
# import PyQt5.QtGui
from PyQt5.uic import loadUi

from PyQt5 import QtCore, QtGui
import sys

# class Second(QMainWindow):
#     def __init__(self, parent=None):
#         super(Second, self).__init__(parent)
#         self.pushButton = QPushButton("click me")
#         self.pushButton = QPushButton("click me")
#         self.pushButton = QPushButton("click me")
#
#
# class First(QMainWindow):
#     def __init__(self, parent=None):
#         super(First, self).__init__(parent)
#         self.pushButton = QPushButton("click me")
#
#         self.setCentralWidget(self.pushButton)
#
#         self.pushButton.clicked.connect(self.on_pushButton_clicked)
#         self.dialogs = list()
#
#     def on_pushButton_clicked(self):
#         dialog = Second(self)
#         self.dialogs.append(dialog)
#         dialog.show()
#
#
# def main():
#     app = QApplication(sys.argv)
#     main = First()
#     main.show()
#     sys.exit(app.exec_())
#
#
# if __name__ == '__main__':
#     main()

class MyWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.label = QLabel("Привет, мир!")
        # self.label.setAlignment(AlignCenter)
        self.btnQuit = QPushButton("&Закрыть окно")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.btnQuit)
        self.setLayout(self.vbox)


class MyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.myWidget = MyWindow()
        self.button = QPushButton("&Изменить надпись")
        mainBox = QVBoxLayout()
        mainBox.addWidget(self.myWidget)
        mainBox.addWidget(self.button)
        self.setLayout(mainBox)
        self.button.clicked.connect(self.on_clicked)

    def on_clicked(self):
        self.myWidget.label.setText("Новая надпись")
        self.button.setDisabled(True)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MyDialog()
    window.setWindowTitle("Преимущество ООП-стиля")
    window.resize(300, 100)
    window.show()
    sys.exit(app.exec_())