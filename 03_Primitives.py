from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtWidgets import QOpenGLWidget, QComboBox
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout,QHBoxLayout, QWidget
from PyQt5.QtWidgets import QGroupBox, QPushButton
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QPen
import sys
import numpy as np

# 정점데이터
POINTS = [[0,0], [10,10], [100, 50]]

PRIMITIVES = [
    'GL_POINTS', 'GL_LINES', 'GL_LINE_STRIP', 'GL_LINE_LOOP',
    'GL_TRIANGLES', 'GL_TRIANGLE_STRIP', 'GL_TRIANGLE_FAN',
    'GL_QUADS', 'GL_QUAD_STRIP', 'GL_POLYGON'
    ]

PRIMITIVE_VALUES = [
    GL_POINTS, GL_LINES, GL_LINE_STRIP, GL_LINE_LOOP,
    GL_TRIANGLES, GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN,
    GL_QUADS, GL_QUAD_STRIP, GL_POLYGON
    ]

selected = 0

class MyGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(MyGLWidget, self).__init__(parent)

    def initializeGL(self) -> None:
        glClearColor(0.8, 0.8, 0.6, 1.0)
        glPointSize(4)
        glLineWidth(2)

    def resizeGL(self, width, hieght):
        # 카메라의 투영특성 설정
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 240, 380, 0, -1, 1)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # 프리미티브를 이용한 객체 그리기
        glBegin(PRIMITIVE_VALUES[selected])
        nPoints = len(POINTS)
        for i in range(nPoints):
            glVertex2fv(POINTS[i])
        glEnd()

        # 그려진 프레임버퍼를 화면으로 송출
        glFlush()

class MyWindow(QMainWindow):
    def __init__(self, title=''):
        QMainWindow.__init__(self)
        self.setWindowTitle(title)

        # GUI 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        gui_layout = QHBoxLayout() # 수평나열 레이아웃 

        # 정점입력을 받기위한 위젯
        central_widget.setLayout(gui_layout)

        self.glWidget = MyGLWidget()
        gui_layout.addWidget(self.glWidget)

        self.controlGroup = QGroupBox('정점 입력')
        gui_layout.addWidget(self.controlGroup)

        control_layout = QVBoxLayout()
        self.controlGroup.setLayout(control_layout)

        ## 정점을 초기화하는 버튼을 추가. 버튼을 누르면 정점이 사라진다.
        ## 이 버튼을 누르면 resetPoints라는 이 메소드가 호출된다.
        reset_button = QPushButton('정점 초기화', self)
        reset_button.clicked.connect(self.resetPoints)

        ### 프리미티브 선택 기능 추가
        primitive_selection = QComboBox()
        for i in range(len(PRIMITIVES)):
            primitive_selection.addItem(PRIMITIVES[i])

        # ComboBox에 기능연결
        primitive_selection.currentIndexChanged.connect(self.selectPrimitive)

        reset_button = QPushButton('reset vertices', self)
        reset_button.clicked.connect(self.resetPoints)

        control_layout.addWidget(primitive_selection)
        control_layout.addWidget(reset_button)

        ## 정점을 입력받기 위한 위짓을 만들고, pointInput이라는 멤버로 관리하자.
        self.pointInput = Drawer(parent=self)
        gui_layout.addWidget(self.pointInput)

    ### Primitive 선택 
    def selectPrimitive(self, text):
        global selected
        selected = int(text)
        self.glWidget.update()    

    # 초기화버튼 클릭 시 실행되는 메서드
    def resetPoints(self, btn):
        global POINTS
        POINTS = []
        self.pointInput.update()


### 정점 입력을 위해 QPainter를 사용
class Drawer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent = parent

        self.painter = QPainter()

    # QPainter를 이용해 입력된 정점을 출력하는 메서드
    def paintEvent(self, event):
        global POINTS

        self.painter.begin(self)
        self.painter.setPen(QPen(Qt.red, 6))

        for i in range(len(POINTS)):
            self.painter.drawPoint(POINTS[i][0], POINTS[i][1])

        self.painter.setPen(QPen(Qt.blue, 2))
        for i in range(len(POINTS) - 1):
            self.painter.drawLine(POINTS[i][0], POINTS[i][1], POINTS[i+1][0], POINTS[i+1][1])
        
        self.painter.end()

    # 마우스 이벤트발생 시 좌표를읽어 POINTS에 추가하는 메서드
    def mousePressEvent(self, event):
        POINTS.append([event.x(), event.y()])
        print(event.x(), event.y())
        self.parent.glWidget.update()
        self.update()

def main(argv=[]):
    app = QApplication(argv)
    window = MyWindow('데이터 입력')
    window.setFixedSize(800, 400)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)
