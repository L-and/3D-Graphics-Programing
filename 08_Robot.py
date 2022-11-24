from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import *

import math
import numpy as np

def drawPlane():
    n, w = 100, 500
    # n: 체스판 한면의 정점수, w: 체스판 한면의 길이
   
    d = w / (n-1) # 인접한 두 정점 사이의 간격

    #  체스판 그리기
    glColor3f(0.3,0.5,0)
    glBegin(GL_QUADS)
    for i in range(n):
        for j in range(n):
            if (i+j)%2 == 0:
                startX = -w/2 + i*d
                startZ = -w/2 + j*d
                glVertex3f(startX, 0, startZ)
                glVertex3f(startX, 0, startZ+d)
                glVertex3f(startX+d, 0, startZ+d)
                glVertex3f(startX+d, 0, startZ)
    glEnd()

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

def drawCube():
    v0 = [-0.5, 0.5, 0.5]
    v1 = [ 0.5, 0.5, 0.5]
    v2 = [ 0.5, 0.5,-0.5]
    v3 = [-0.5, 0.5,-0.5]
    v4 = [-0.5,-0.5, 0.5]
    v5 = [ 0.5,-0.5, 0.5]
    v6 = [ 0.5,-0.5,-0.5]
    v7 = [-0.5,-0.5,-0.5]
    glBegin(GL_LINES)
    glVertex3fv(v0); glVertex3fv(v1)
    glVertex3fv(v1); glVertex3fv(v2)
    glVertex3fv(v2); glVertex3fv(v3)
    glVertex3fv(v3); glVertex3fv(v0)
    glVertex3fv(v4); glVertex3fv(v5)
    glVertex3fv(v5); glVertex3fv(v6)
    glVertex3fv(v6); glVertex3fv(v7)
    glVertex3fv(v7); glVertex3fv(v4)
    glVertex3fv(v0); glVertex3fv(v4)
    glVertex3fv(v1); glVertex3fv(v5)
    glVertex3fv(v2); glVertex3fv(v6)
    glVertex3fv(v3); glVertex3fv(v7)    
    glEnd()
    drawAxes()


class MyGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.base_position = [0.0,0.0]

        # 몸통의 스케일
        self.bodyScaleX = 2
        self.bodyScaleY = 1
        self.bodyScaleZ = 2

        # 팔1의 스케일
        self.arm1ScaleX = 0.5
        self.arm1ScaleY = 4
        self.arm1ScaleZ = 0.5

        # 팔1: y축기준 회전, x축기준 회전
        self.arm1YRot = 30 # 팔1의 회전
        self.arm1XRot = 10 # 팔1의 굽힘

        # 팔2의 스케일
        self.arm2ScaleX = 0.5
        self.arm2ScaleY = 3
        self.arm2ScaleZ = 0.5

        # 팔2: x축 기준 회전
        self.arm2XRot = 45 # 팔2의 굽힘

        # 손1의 회전
        self.handAngle = 0
   
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.planeList = glGenLists(1)
        glNewList(self.planeList, GL_COMPILE)
        # 그리기 코드
        drawPlane()
        glEndList()

        glEnable(GL_DEPTH_TEST)


    def resizeGL(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.01, 100)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0,7,10, 0,0,0, 0,1,0)

        glCallList(self.planeList)
        drawAxes()

        ###  Base: 전후 좌우로 이동 가능

        # 제어를 통해 옮겨간 위치
        glTranslatef(self.base_position[0], 0, self.base_position[1])
       
        glTranslatef(0, 0.5, 0) # 몸통을 평면으로 들어올리는 변환
        glPushMatrix()
        glScalef(self.bodyScaleX, self.bodyScaleY, self.bodyScaleZ)   # 몸통의 크기 변경
        drawAxes()    
        glColor3f(1,1,1)        
        drawCube()
        glPopMatrix()


        glPushMatrix() # 몸통의 위치
        ### 팔1 그리기
        # 팔1 피벗 설정
        glTranslatef(0, self.bodyScaleY / 2, 0) # 몸통의 반만큼 올림(중심이 관절의 위치)
        
        ## 회전 적용
        glRotatef(self.arm1XRot, 1, 0, 0)
        glRotatef(self.arm1YRot, 0, 1, 0)
        
        glTranslatef(0, self.arm1ScaleY / 2, 0) # 팔의 길이의 절반만큼 올려 피벗과 관절의 위치를 맞춰줌

        # 팔1 크기 설정
        glPushMatrix()
        glScalef(self.arm1ScaleX, self.arm1ScaleY, self.arm1ScaleZ)
        drawCube()
        glPopMatrix()
        
        ### 팔2 그리기
        # 부모인 팔 1의 반만큼 위로 이동
        glTranslatef(0, self.arm1ScaleY / 2, 0)
        glRotatef(self.arm2XRot, 1, 0, 0)        

        # 팔 2의 피벗을 관절로 설정
        glTranslatef(0, self.arm2ScaleY / 2, 0)

        # 팔2 크기 설정
        glPushMatrix()
        glScalef(self.arm2ScaleX, self.arm2ScaleY, self.arm2ScaleZ)
        drawCube()
        glPopMatrix()

        ####### 손 그리기
        # 손 1
        glPushMatrix() # 손 1 변환 전에 기록
        #### 손 1의 변환
        glTranslatef(0, 1.5, 0)
        glRotatef(self.handAngle, 1, 0, 0)
        glTranslatef(0, 0.5, 0)
        glPushMatrix()
        glScalef(1, 1, 0.1)
        drawAxes()
        glColor3f(1, 1, 0)
        drawCube()
        glPopMatrix() # 손 크기 변경 전으로 회귀
        glPopMatrix() # 손1 변환 전으로 회귀

        ####### 손2 그리기
        # 손 2  
        glPushMatrix() # 손 1 변환 전에 기록
        #### 손 2의 변환
        glTranslatef(0, 1.5, 0)
        glRotatef(-self.handAngle, 1, 0, 0)
        glTranslatef(0, 0.5, 0)
        glPushMatrix()  
        glScalef(1, 1, 0.1)
        drawAxes()
        glColor3f(1, 1, 0)
        drawCube()
        glPopMatrix() # 손 크기 변경 전으로 회귀
        glPopMatrix() # 손2 변환 전으로 회귀


        glPopMatrix() # 몸통위치로 회귀
    ########### 날개 그리기

        glPushMatrix()

        glTranslatef(1, 0, 0)
        glRotatef(30, 0, 0, 1)
        glTranslatef(1.5, 0, 0)
        glPushMatrix()
        glScalef(3, 0.1, 2)
        glColor3f(1, 1, 1)
        drawCube()
        glPopMatrix()

        glPopMatrix()

        glPushMatrix()

        glTranslatef(-1, 0, 0)
        glRotatef(-30, 0, 0, 1);      
        glTranslatef(-1.5, 0, 0)
        glPushMatrix()  
        glScalef(3, 0.1, 2)
        glColor3f(1, 1, 1)
        drawCube()
        glPopMatrix()

        glPopMatrix()


class MyWindow(QMainWindow):
    def __init__(self, title=''):
        QMainWindow.__init__(self)
        self.setWindowTitle(title)
        self.glWidget = MyGLWidget()
        self.setCentralWidget(self.glWidget)

    def keyPressEvent(self, e):
       
        step = 0.1
        angle_step = 1

        if e.key() == Qt.Key.Key_W:
            self.glWidget.base_position[1] -= step
        elif e.key() == Qt.Key.Key_S:
            self.glWidget.base_position[1] += step
        elif e.key() == Qt.Key.Key_A:
            self.glWidget.base_position[0] -= step
        elif e.key() == Qt.Key.Key_D:
            self.glWidget.base_position[0] += step
        elif e.key() == Qt.Key.Key_Q:
            self.glWidget.arm1YRot -= angle_step
        elif e.key() == Qt.Key.Key_E:
            self.glWidget.arm1YRot += angle_step
        elif e.key() == Qt.Key.Key_1:
            self.glWidget.arm1XRot -= angle_step
        elif e.key() == Qt.Key.Key_2:
            self.glWidget.arm1XRot += angle_step
        elif e.key() == Qt.Key.Key_3:
            self.glWidget.arm2XRot -= angle_step
        elif e.key() == Qt.Key.Key_4:
            self.glWidget.arm2XRot += angle_step
        elif e.key() == Qt.Key.Key_5:
            self.glWidget.handAngle -= angle_step
        elif e.key() == Qt.Key.Key_6:
            self.glWidget.handAngle += angle_step
       
        self.glWidget.update()

def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('변환의 이해')
    window.setFixedSize(1200, 600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)