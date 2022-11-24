# 과제 3: 태양계 모델을 개선하여 두 개의 행성을 추가하고, 각각의 행성에 두 개씩의 위성을 달아보자. (코드와 결과를 출력해 제출한다)
# 20210010 김민서
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

        self.planetAngle = 0 # 행성의 공전각도
        self.planetSelfAngle = 0 # 행성의 자전 각도
        self.planetRotateRadius = 100 # 행성의 공전반지름
        self.planetRadius = 5 # 행성의 반지름

        self.setelliteAngle = 0 # 위성의 공전각도
        self.setelliteSelfAngle = 0 # 위성의 자전 각도
        self.setelliteRotateRadius = 15 # 위성의 공전반지름
        self.setelliteRadius = 2 # 위성의 반지름

        self.planetRatio = [2, 0.5, 0.8, 1, 1.4] # 행성들간 공전, 자전, 크기 배율
    
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
        gluLookAt(130, 130, 130, 0,0,0, 0,1,0)

        ############### 태양 ############
        glPushMatrix()
        glRotate(self.planetSelfAngle * self.planetRatio[0], 0, 1, 0) # 태양 자전
        drawSphere(radius = self.planetRadius * self.planetRatio[0], func = self.meshLoader.draw_list) # 태양 그리기
        glPopMatrix()

        drawCircle(self.planetRotateRadius * self.planetRatio[1]) # 수성 궤도 그리기
        drawCircle(self.planetRotateRadius * self.planetRatio[2]) # 금성 궤도 그리기
        drawCircle(self.planetRotateRadius * self.planetRatio[3]) # 지구 궤도 그리기
        drawCircle(self.planetRotateRadius * self.planetRatio[4]) # 화성 궤도 그리기


        ########### 수성계 ##############
        glPushMatrix()

        glRotatef(self.planetAngle * self.planetRatio[1], 0, 1, 0)  # 수성 공전
        glTranslatef(self.planetRotateRadius * self.planetRatio[1], 0, 0) # Transform 이동(zero > 수성)

        drawCircle(self.setelliteRotateRadius * self.planetRatio[1]) # 위성1 궤도 그리기
        drawCircle(self.setelliteRotateRadius * self.planetRatio[2]) # 위성2 궤도 그리기

        #### 수성 ####
        glPushMatrix()
        glRotatef(self.planetSelfAngle * self.planetRatio[1], 0, 1, 0)  # 수성 자전
        drawSphere(radius = self.planetRadius * self.planetRatio[1], func = self.meshLoader.draw_list) # 수성 생성
        glPopMatrix()
        ### 수성끝 ###

        #### 위성1 ####
        glPushMatrix()
        glRotatef(self.planetSelfAngle * self.planetRatio[1], 0, 1, 0) # 위성1 자전
        glTranslatef(self.setelliteRotateRadius * self.planetRatio[1], 0, 0) # 위성1 위치이동
        drawSphere(radius = self.setelliteRadius * self.planetRatio[1], func = self.meshLoader.draw_list)
        glPopMatrix()
        ### 위성1끝 ###

        #### 위성2 ####
        glPushMatrix()
        glRotatef(self.planetSelfAngle * self.planetRatio[2], 0, 1, 0) # 위성2 자전
        glTranslatef(self.setelliteRotateRadius * self.planetRatio[2], 0, 0) # 위성2 위치이동
        drawSphere(radius = self.setelliteRadius * self.planetRatio[2], func = self.meshLoader.draw_list)
        glPopMatrix()
        ### 위성2끝 ###

        glPopMatrix()
        ############ 수성계 끝 #############

        ########### 금성계 ##############
        glPushMatrix()

        glRotatef(self.planetAngle * self.planetRatio[2], 0, 1, 0)  # 금성 공전
        glTranslatef(self.planetRotateRadius * self.planetRatio[2], 0, 0) # Transform 이동(zero > 금성)

        drawCircle(self.setelliteRotateRadius * self.planetRatio[1]) # 위성1 궤도 그리기
        drawCircle(self.setelliteRotateRadius * self.planetRatio[3]) # 위성2 궤도 그리기

        #### 금성 ####
        glPushMatrix()
        glRotatef(self.planetSelfAngle * self.planetRatio[2], 0, 1, 0)  # 금성 자전
        drawSphere(radius = self.planetRadius * self.planetRatio[2], func = self.meshLoader.draw_list) # 금성 생성
        glPopMatrix()
        ### 금성끝 ###

        #### 위성1 ####
        glPushMatrix()
        glRotatef(self.planetSelfAngle * self.planetRatio[1], 0, 1, 0) # 위성1 자전
        glTranslatef(self.setelliteRotateRadius * self.planetRatio[1], 0, 0) # 위성1 위치이동
        drawSphere(radius = self.setelliteRadius * self.planetRatio[1], func = self.meshLoader.draw_list)
        glPopMatrix()
        ### 위성1끝 ###

        #### 위성2 ####
        glPushMatrix()
        glRotatef(self.planetSelfAngle * self.planetRatio[3], 0, 1, 0) # 위성2 자전
        glTranslatef(self.setelliteRotateRadius * self.planetRatio[3], 0, 0) # 위성2 위치이동
        drawSphere(radius = self.setelliteRadius * self.planetRatio[3], func = self.meshLoader.draw_list)
        glPopMatrix()
        ### 위성2끝 ###

        glPopMatrix()
        ############ 금성계 끝 #############

        ########### 지구계 ##############
        glPushMatrix()

        glRotatef(self.planetAngle, 0, 1, 0)  # 지구 공전
        glTranslatef(self.planetRotateRadius, 0, 0) # Transform 이동(zero > 지구)

        drawCircle(self.setelliteRotateRadius) # 달 궤도 그리기

        #### 지구 ####
        glPushMatrix()
        glRotatef(self.planetSelfAngle, 0, 1, 0)  # 지구 자전
        drawSphere(radius = self.planetRadius, func = self.meshLoader.draw_list) # 지구 생성
        glPopMatrix()
        ### 지구끝 ###

        #### 달 ####
        glPushMatrix()
        glRotatef(self.planetSelfAngle, 0, 1, 0) # 달 자전
        glTranslatef(self.setelliteRotateRadius, 0, 0) # 달 위치이동
        drawSphere(radius = self.setelliteRadius, func = self.meshLoader.draw_list)
        glPopMatrix()
        ### 달끝 ###

        glPopMatrix()
        ############ 지구계 끝 #############

        ############## 화성계 ##############
        glPushMatrix()

        glRotatef(self.planetAngle * self.planetRatio[4], 0, 1, 0)  # 화성 공전
        glTranslatef(self.planetRotateRadius * self.planetRatio[4], 0, 0) # Transform 이동(zero > 화성)

        #### 화성 ####
        glPushMatrix()
        glRotatef(self.planetSelfAngle * self.planetRatio[4], 0, 1, 0) # 화성 자전
        drawSphere(radius = self.planetRadius * self.planetRatio[4], func = self.meshLoader.draw_list) # 화성 그리기
        glPopMatrix()
        ### 화성끝 ###

        glPopMatrix()
        ############# 화성계 끝 #############

        
        





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
        self.glWidget.planetAngle += 0.5
        self.glWidget.planetSelfAngle += 2
        self.glWidget.setelliteAngle += 1
        self.glWidget.update()

def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('메시 읽기')
    window.setFixedSize(1000, 700)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)
