import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

class MyWindow(QMainWindow):
    def __init__(self, title=''):
        QMainWindow.__init__(self)
        self.setWindowTitle(title)

def main(argv=[]):
    app = QApplication(argv)
    window = MyWindow('20210010 김민서')
    window.setFixedSize(600, 600)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main(sys.argv)
