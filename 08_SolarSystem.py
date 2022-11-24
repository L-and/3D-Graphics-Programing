from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import *

import math
import numpy as np

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

def drawCircle (r) :
    glColor3f( 1.0, 1.0, 1.0 )
    glBegin(GL_LINE_LOOP)
    for i in range ( 50 ) :
        glVertex3f(r*math.cos( 6.28*float(i) / 50.0 ) , 
                   0 , 
                   r*math.sin( 6.28*float(i) / 50.0 ) )
    glEnd()

def drawSphere(radius = 1, func=None):
    glPushMatrix()
    glScalef(radius, radius, radius)
    drawAxes()
    if func is not None:
        func()
    glPopMatrix()

class MeshLoader:
    def __init__(self):
        self.nV = 0 # 정점의 개수
        self.nF = 0 # 면의 개수
        self.vertexBuffer = None # 정점 버퍼
        self.idxBuffer = None # 면을 구성하는 정점 인덱스 버퍼
        self.list = None

    def loadData(self, filename):
        with open(filename, 'rt') as inputfile:
            self.nV = int(next(inputfile))
            self.vertexBuffer = np.zeros(shape = (self.nV*3, ), dtype=float)
            for i in range(self.nV):
                verts = next(inputfile).split()
                self.vertexBuffer[i*3:i*3+3] = verts[0:3]
            
            coordMin = self.vertexBuffer.min()
            coordMax = self.vertexBuffer.max()
            scale = max([coordMin, coordMax], key=abs)
            self.vertexBuffer /= scale

            self.nF = int(next(inputfile))
            self.idxBuffer = np.zeros(shape=(self.nF*3, ), dtype=int)
            for i in range(self.nF):
                idx = next(inputfile).split()
                self.idxBuffer[i*3: i*3+3] = idx[1:4]


    def draw(self):

        glBegin(GL_TRIANGLES)
        for i in range(self.nF):
            verts = self.idxBuffer[i*3: i*3+3]
            glColor3fv(  ( self.vertexBuffer[verts[0]*3 : verts[0]*3 +3] + np.array([1])) / 1.5 )
            glVertex3fv( self.vertexBuffer[verts[0]*3 : verts[0]*3 +3] )
            glColor3fv(  ( self.vertexBuffer[verts[1]*3 : verts[1]*3 +3] + np.array([1])) / 1.5 )
            glVertex3fv( self.vertexBuffer[verts[1]*3 : verts[1]*3 +3] )
            glColor3fv(  ( self.vertexBuffer[verts[2]*3 : verts[2]*3 +3] + np.array([1])) / 1.5 )
            glVertex3fv( self.vertexBuffer[verts[2]*3 : verts[2]*3 +3] )
        glEnd()

        glColor3f(0,0,1)
        for i in range(self.nF):
            verts = self.idxBuffer[i*3: i*3+3]
            glBegin(GL_LINE_LOOP)
            glVertex3fv( self.vertexBuffer[verts[0]*3 : verts[0]*3 +3] )
            glVertex3fv( self.vertexBuffer[verts[1]*3 : verts[1]*3 +3] )
            glVertex3fv( self.vertexBuffer[verts[2]*3 : verts[2]*3 +3] )
            glEnd()

    def make_displayList(self):
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        self.draw()
        glEndList()

    def draw_list(self):
        glCallList(self.list)



class MyGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0

        self.earthAngle = 0 # 지구의 공전각도
        self.earthSelfAngle = 0 # 지구의 자전 각도
        self.earthRotateRadius = 30 # 지구의 공전반지름
        self.earthRadius = 2 # 지구의 반지름

        self.moonAngle = 0 # 달의 공전각도
        self.moonSelfAngle = 0 # 달의 자전 각도
        self.moonRotateRadius = 3 # 달의 공전반지름
        self.moonRadius = 0.5 # 달의 반지름
    
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)

        self.meshLoader = MeshLoader() # 메시 로더 생성
        self.meshLoader.loadData('./sphere.txt')
        self.meshLoader.make_displayList()
        
        glEnable(GL_DEPTH_TEST) ########################


    def resizeGL(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.01, 5000)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) ###############
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(50, 50, 50, 0,0,0, 0,1,0)

        drawSphere(radius = 10, func = self.meshLoader.draw_list) # 태양

        drawCircle(self.earthRotateRadius) # 지구 궤도
        drawCircle(self.earthRotateRadius * 1.5) # 달 궤도

        # 지구
        glPushMatrix()
        
        glRotatef(self.earthAngle, 0, 1, 0)
        glTranslatef(self.earthRotateRadius, 0, 0)

        glPushMatrix()
        glRotatef(self.earthSelfAngle, 0, 1, 0)
        drawSphere(radius = self.earthRadius, func = self.meshLoader.draw_list)
        glPopMatrix()

        drawCircle(self.moonRotateRadius) # 달 궤도
        # 달
        glRotatef(self.earthSelfAngle, 0, 1, 0)
        glTranslatef(self.moonRotateRadius, 0, 0)

        drawSphere(radius = self.moonRadius, func = self.meshLoader.draw_list)
        glPopMatrix()

        
        # 화성
        glRotatef(self.earthAngle * 0.8, 0, 1, 0)
        glTranslatef(self.earthRotateRadius * 1.5, 0, 0)

        glPushMatrix()
        glRotatef(self.earthSelfAngle * 0.8, 0, 1, 0)
        drawSphere(radius = self.earthRadius, func = self.meshLoader.draw_list)
        glPopMatrix()



class MyWindow(QMainWindow):
    def __init__(self, title=''):
        QMainWindow.__init__(self)
        self.setWindowTitle(title)
        self.glWidget = MyGLWidget()
        self.setCentralWidget(self.glWidget)

        self.timer = QTimer(self)
        self.timer.setInterval(5)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()

    def timeout(self):
        self.glWidget.earthAngle += 1
        self.glWidget.earthSelfAngle += 5
        self.glWidget.moonAngle += 0.5
        self.glWidget.update()

def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('메시 읽기')
    window.setFixedSize(1000, 700)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)
