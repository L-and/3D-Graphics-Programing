from OpenGL.GL import *
from OpenGL.GLU import *

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
import sys

#### MyWindow 클래스의 시작 ############################
class MyGLWindow(QOpenGLWidget) : # QOpenGLWidget 상속

    def __init__(self):  
        super().__init__()  # 슈퍼클래스 QMainWindow 생성자 실행

        self.setWindowTitle('나의 첫 OpenGL 앱')

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        
        glBegin(GL_TRIANGLES)
        glColor3f(1, 1, 0)
        glVertex3f(-1, 0, 0)
        glVertex3f( 1, 0, 0)
        glVertex3f( 0, 1, 0)
        glColor3f(0, 1, 1)
        glVertex3f(-1, 0.5, 0)
        glVertex3f( 1, 0.5, 0)
        glVertex3f( 0,-0.5, 0)
        glEnd()

#### MyGLWindow 클래스의 끝 ############################

def main(argv = sys.argv) :
    ## 윈도우 생성하기
    app = QApplication(argv)
    window = MyGLWindow()
    window.show()

    app.exec()


if __name__ == '__main__' :
    main(sys.argv)



