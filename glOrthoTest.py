from ast import keyword
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt
import math

def drawAxes():
    glBegin(GL_LINES)
    glColor3f(1,0,0)
    glVertex3f(0,0,0)
    glVertex3f(1,0,0)
    glColor3f(0,1,0)
    glVertex3f(0,0,0)
    glVertex3f(0,1,0)
    glColor3f(0,0,1)
    glVertex3f(0,0,0)
    glVertex3f(0,0,1)
    glEnd()

def drawHelix():
    glBegin(GL_LINE_STRIP)
    for i in range(1000):
        angle = i / 100
        x, y = math.cos(angle), math.sin(angle)
        glVertex3f(x, y, angle/10)
    glEnd()

def drawBox(l, r, b, t, n, f): #glOrtho가 만드는 공간을 가시화
    glColor(1, 1, 1)
    # 앞면
    glBegin(GL_LINE_LOOP)
    glVertex3f(l, t, n); glVertex3f(l, b, n)
    glVertex3f(r, b, n); glVertex3f(r, t, n)
    glEnd()
    #뒷면
    glBegin(GL_LINE_LOOP)
    glVertex3f(l, t, f); glVertex3f(l, b, f)
    glVertex3f(r, b, f); glVertex3f(r, t, f)
    glEnd()

    glBegin(GL_LINES)
    glVertex3f(l, t, n); glVertex3f(l, t, f)
    glVertex3f(l, b, n); glVertex3f(l, b, f)
    glVertex3f(r, t, n); glVertex3f(r, t, f)
    glVertex3f(r, b, n); glVertex3f(r, b, f)
    glEnd()
    
class MyGLWidget(QOpenGLWidget):
    def __init__(self, parent=None, observation = False):
        super().__init__(parent)
        self.observation = observation

        self.left = self.bottom = self.near = -2
        self.right = self.top = self.far = 2

    def initializeGL(self):
        pass

    def resizeGL(self, w, h):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if self.observation:
            glOrtho(-4, 4, -4, 4, -10, 100)
        else:
            glOrtho(self.left, self.right, self.bottom, self.top, self.near, self.far)


    def paintGL(self):
        self.projection_update()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        if self.observation == True:
            gluLookAt(
                1, 0.7, 0.5, # 카메라의 위치
                0, 0, 0, # 쳐다보는 목표의 위치
                0, 1, 0  # 카메라의 상향벡터
            )

        drawAxes()
        drawHelix()
        drawBox(self.left, self.right, self.bottom, self.top, self.near, self.far)
        
    def projection_update(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if not self.observation:
            glOrtho(self.left, self.right, self.bottom, self.top, self.near, self.far)

class MyWindow(QMainWindow):
    def __init__(self, title=''):
        QMainWindow.__init__(self) # QMainWindow 슈퍼 클래스의 초기화
        self.setWindowTitle(title)

        # GUI 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        gui_layout = QHBoxLayout()

        central_widget.setLayout(gui_layout)

        self.glWidget1 = MyGLWidget()
        self.glWidget2 = MyGLWidget(observation = True)

        gui_layout.addWidget(self.glWidget1)
        gui_layout.addWidget(self.glWidget2)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key.Key_A:
            self.glWidget1.left -= 0.1
            self.glWidget2.left -= 0.1
            self.glWidget1.right -= 0.1
            self.glWidget2.right -= 0.1
        elif key == Qt.Key.Key_D:
            self.glWidget1.left += 0.1
            self.glWidget2.left += 0.1
            self.glWidget1.right += 0.1
            self.glWidget2.right += 0.1
        elif key == Qt.Key.Key_W:
            self.glWidget1.top += 0.1
            self.glWidget2.top += 0.1
            self.glWidget1.bottom += 0.1
            self.glWidget2.bottom += 0.1
        elif key == Qt.Key.Key_S:
            self.glWidget1.top -= 0.1
            self.glWidget2.top -= 0.1
            self.glWidget1.bottom -= 0.1
            self.glWidget2.bottom -= 0.1


        self.glWidget1.update()
        self.glWidget2.update()
    
def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('glOrtho 연습')
    window.setFixedSize(1200, 600)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main(sys.argv)