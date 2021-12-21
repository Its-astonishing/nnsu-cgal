#from PyQt5.QtCore import *
#from PyQt5.QtWidgets import *
#from PyQGLViewer import *
#from OpenGL.GL import *
#
#class Viewer(QGLViewer):
#
#    def __init__(self,parent = None):
#        QGLViewer.__init__(self,parent)
#        
#    def draw(self):
#        glBegin(GL_TRIANGLES)
#        glColor3f(1.0, 0.0 , 0.0)
#        glVertex3f(-0.7, 0.0, 0.0)
#        glColor3f(0.0, 1.0 , 0.0)
#        glVertex3f(0.7, 0.0, 0.0)
#        glColor3f(0.0, 0.0 , 1.0)
#        glVertex3f(0.0, 1.0, 0.0)
#        glEnd()
#        
#    def keyPressEvent(self,e):
#        modifiers = e.modifiers()
#        if (e.key()==Qt.Key_W):
#            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
#        if (e.key()==Qt.Key_F):
#            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
#        self.updateGL()
#  
#def main():
#    qapp = QApplication([])
#    viewer = Viewer()
#    viewer.show()
#    qapp.exec_()
#
#if __name__ == '__main__':
#    main()

#viewer3d_triangle.py
import time
import random
import math
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQGLViewer import *
from OpenGL.GL import *

class Points:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Viewer(QGLViewer):

    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
        self.is_scene_shown_ = True
        self.figures_num = 0
        self.cube_points_list = []

        self.is_cube_initialized = False
        
        self.ball_points_list = []
        self.is_ball_initialized = False
        
        self.sphere_points_list = []
        self.is_sphere_initialized = False
        
        
       
    def draw_cube_grid(self):
        glBegin(GL_POINTS)
        grid_range = 4
        grid_step = grid_range / 10
        points_value = []
        
        cached_value_i = 0.0
        
        for i in range(grid_range):
            points_value.append(cached_value_i)
            cached_value_i = cached_value_i + grid_step
            
        for x in range(grid_range):
            x_value = points_value[x]
            for y in range(grid_range):
                y_value = points_value[y]

                for z in range(grid_range):
                    z_value = points_value[z]
                    glVertex3f(x_value, y_value, z_value)
                    #current_point = Points(x_value, y_value, z_value)
                    #cube_points.append(current_point)
        glEnd()
        
    def init_points_random_cube(self):
        points_count = 1000
        for i in range(points_count):
            x = random.uniform(0.0, 1.0)
            y = random.uniform(0.0, 1.0)
            z = random.uniform(0.0, 1.0)
            self.cube_points_list.append(Points(x, y, z))
        
    def draw_random_cube(self):
        if (not self.is_cube_initialized):
            self.init_points_random_cube()
            self.is_cube_initialized = True
        glBegin(GL_POINTS)
        for point in self.cube_points_list:
            glVertex3f(point.x, point.y, point.z)
        glEnd()
        
    def init_points_random_ball(self):
        points_count = 1000
        for i in range(points_count):
            r = random.uniform(0.0, 1.0)
            phi = random.uniform(0.0, 360)
            tetta = random.uniform(0.0, 180)
            x = r * math.sin(tetta) * math.cos(phi)
            y = r * math.sin(tetta) * math.sin(phi)
            z = r * math.cos(tetta)
            self.ball_points_list.append(Points(x, y, z))
            
        
    def draw_random_ball(self):
        if (not self.is_ball_initialized):
            self.init_points_random_ball()
            self.is_ball_initialized = True
        glBegin(GL_POINTS)
        for point in self.ball_points_list:
            glVertex3f(point.x, point.y, point.z)
        glEnd()
        
    def init_points_random_sphere(self):
        points_count = 1000
        for i in range(points_count):
            delta = random.uniform(-0.1, 0.1)
            r = 1.0 + delta
            phi = random.uniform(0.0, 360)
            tetta = random.uniform(0.0, 180)
            x = r * math.sin(tetta) * math.cos(phi)
            y = r * math.sin(tetta) * math.sin(phi)
            z = r * math.cos(tetta)
            self.ball_points_list.append(Points(x, y, z))
            
        
    def draw_random_sphere(self):
        if (not self.is_sphere_initialized):
            self.init_points_random_sphere()
            self.is_sphere_initialized = True
        glBegin(GL_POINTS)
        for point in self.ball_points_list:
            glVertex3f(point.x, point.y, point.z)
        glEnd()
            
    
    def draw(self):
        glPointSize(4)
        if (self.is_scene_shown_):
            if (self.figures_num == 0):
                glBegin(GL_TRIANGLES)
                glColor3f(1.0, 0.0 , 0.0)
                glVertex3f(-0.7, 0.0, 0.0)
                glColor3f(0.0, 1.0 , 0.0)
                glVertex3f(0.7, 0.0, 0.0)
                glColor3f(0.0, 0.0 , 1.0)
                glVertex3f(0.0, 1.0, 0.0)
                glEnd()
            elif(self.figures_num == 1):
                self.draw_cube_grid()
            elif(self.figures_num == 2):
                self.draw_random_cube()
            elif(self.figures_num == 3):
                self.draw_random_ball()
            elif(self.figures_num == 4):
                self.draw_random_sphere()    
                
                                
                
		
    def keyPressEvent(self,e):
        modifiers = e.modifiers()
        if (e.nativeVirtualKey()==Qt.Key_W):
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif (e.nativeVirtualKey()==Qt.Key_F):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        elif (e.nativeVirtualKey()==Qt.Key_S):
            self.is_scene_shown_ = not self.is_scene_shown_
        elif (e.nativeVirtualKey()==Qt.Key_N):
            self.figures_num = (self.figures_num + 1) % 5
            self.is_cube_initialized = False        
            self.is_ball_initialized = False
            self.is_sphere_initialized = False
            self.cube_points_list.clear()
            self.sphere_points_list.clear()
            self.ball_points_list.clear()
        self.updateGL()

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
    