#bspline3.py
from __future__ import print_function
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQGLViewer import *
from OpenGL.GL import *

def clamp(value, minval, maxval):
    return max(minval, min(value, maxval))

class BSpline2:

    def __init__(self, reference_points, discrete_num = 10, closed = False):
        self.points = reference_points
        self.d_num = int(discrete_num)
        self.closed = closed
        
        # Генерация коэффициентов для сгенеренных вершин B-сплайна 3 порядка
        self.coefs = [];
        for i in range(self.d_num):
            spline_segm_coef = self.calc_spline2_coef(i/self.d_num)
            self.coefs.append(spline_segm_coef)
            
            
    def move_point(self, selected_point_id, x_diff, y_diff, z_diff):
        self.points[selected_point_id][0] = self.points[selected_point_id][0] + x_diff
        self.points[selected_point_id][1] = self.points[selected_point_id][1] + y_diff
        self.points[selected_point_id][2] = self.points[selected_point_id][2] + z_diff

            
    def draw_reference(self, selected_point_id):
        # Draw the baseline
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_LINES)
        glColor3f(0.22, 0.78 , 0.0)
        points_count = int(len(self.points))
        for i in range(1, points_count):
            glVertex3f(self.points[i - 1][0], self.points[i - 1][1], self.points[i - 1][2])
            glVertex3f(self.points[i][0], self.points[i][1], self.points[i][2])

        glEnd()

        # Draw all points
        glPointSize(4)
        glBegin(GL_POINTS)
        for i in range(points_count):
            glVertex3f(self.points[i][0], self.points[i][1], self.points[i][2])
        glEnd()
    

        # Draw selected point
        glPointSize(15)
        glBegin(GL_POINTS)
        glColor3f(0.11, 0.32 , 0.57)
        glVertex3f(self.points[selected_point_id][0], self.points[selected_point_id][1], self.points[selected_point_id][2])
        glEnd()
            

    def calc_spline2_coef(self, t):
        coefs = [0,0,0,0]
        coefs[0] = (1.0-t)*(1.0-t) / 2.0;
        coefs[1] = (-2.0 * t * t + 2 * t + 1) / 2.0;
        coefs[2] = t * t / 2.0;
        return coefs
    
    def draw_spline_curve(self):
        if not self.closed:     
            segmentsCount = len(self.points) - 1
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glBegin(GL_LINE_STRIP)
            glColor3f(1.0, 0.0 , 0.0)
        else:
            segmentsCount = len(self.points) #Сегмент между первой и последней вершиной
            glBegin(GL_LINE_LOOP)  
        for i in range(segmentsCount):
            self.draw_glvertex_for_one_segment_of_spline(i);
        glEnd()

    def draw_glvertex_for_one_segment_of_spline(self, segment_id):
        pNum = len(self.points)
        # Вычисление номеров вершин в списке вершин для построения сплайна
        if not self.closed:
            p0 = clamp(segment_id - 1, 0, pNum - 1)
            p1 = clamp(segment_id, 0, pNum - 1)
            p2 = clamp(segment_id + 1, 0, pNum - 1)
        else:
            p0 = (segment_id - 1 + pNum) % pNum
            p1 = (segment_id + pNum) % pNum
            p2 = (segment_id + 1 + pNum) % pNum
        # По заранее вычисленным коэффициентам 
        # вычисляем промежуточные точки сплайна
        # и выводим их в OpenGL
        for i in range(self.d_num):
            x = self.coefs[i][0] * self.points[p0][0] \
                + self.coefs[i][1] * self.points[p1][0] \
                + self.coefs[i][2] * self.points[p2][0]
            y = self.coefs[i][0] * self.points[p0][1] \
                + self.coefs[i][1] * self.points[p1][1] \
                + self.coefs[i][2] * self.points[p2][1]
            z = self.coefs[i][0] * self.points[p0][2] \
            + self.coefs[i][1] * self.points[p1][2] \
            + self.coefs[i][2] * self.points[p2][2]
 
            glVertex3f(x, y, z)

class BSpline3:

    def __init__(self, reference_points, discrete_num = 10, closed = False):
        self.points = reference_points
        self.d_num = int(discrete_num)
        self.closed = closed
        
        # Генерация коэффициентов для сгенеренных вершин B-сплайна 3 порядка
        self.coefs = [];
        for i in range(self.d_num):
            spline_segm_coef = self.calc_spline3_coef(i/self.d_num)
            self.coefs.append(spline_segm_coef)

    def calc_spline3_coef(self, t):
        coefs = [0,0,0,0]
        coefs[0] = (1.0-t)*(1.0-t)*(1.0-t)/6.0;
        coefs[1] = (3.0*t*t*t - 6.0*t*t + 4)/6.0;
        coefs[2] = (-3.0*t*t*t + 3*t*t + 3*t+1)/6.0;
        coefs[3] = t*t*t/6.0;
        return coefs
    
    def draw_spline_curve(self):
        if not self.closed:     
            segmentsCount = len(self.points) - 1
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glBegin(GL_LINE_STRIP)
            glColor3f(0.0, 0.0 , 1.0)
        else:
            segmentsCount = len(self.points) #Сегмент между первой и последней вершиной
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glBegin(GL_LINE_LOOP)  
            glColor3f(0.0, 0.0 , 1.0)
        for i in range(segmentsCount):
            self.draw_glvertex_for_one_segment_of_spline(i);
        glEnd()

    def draw_glvertex_for_one_segment_of_spline(self, segment_id):
        pNum = len(self.points)
        # Вычисление номеров вершин в списке вершин для построения сплайна
        if not self.closed:
            p0 = clamp(segment_id - 1, 0, pNum - 1)
            p1 = clamp(segment_id, 0, pNum - 1)
            p2 = clamp(segment_id + 1, 0, pNum - 1)
            p3 = clamp(segment_id + 2, 0, pNum - 1)
        else:
            p0 = (segment_id - 1 + pNum) % pNum
            p1 = (segment_id + pNum) % pNum
            p2 = (segment_id + 1 + pNum) % pNum
            p3 = (segment_id + 2 + pNum) % pNum
        # По заранее вычисленным коэффициентам 
        # вычисляем промежуточные точки сплайна
        # и выводим их в OpenGL
        for i in range(self.d_num):
            x = self.coefs[i][0] * self.points[p0][0] \
                + self.coefs[i][1] * self.points[p1][0] \
                + self.coefs[i][2] * self.points[p2][0] \
                + self.coefs[i][3] * self.points[p3][0] 
            y = self.coefs[i][0] * self.points[p0][1] \
                + self.coefs[i][1] * self.points[p1][1] \
                + self.coefs[i][2] * self.points[p2][1] \
                + self.coefs[i][3] * self.points[p3][1]
            z = self.coefs[i][0] * self.points[p0][2] \
            + self.coefs[i][1] * self.points[p1][2] \
            + self.coefs[i][2] * self.points[p2][2] \
            + self.coefs[i][3] * self.points[p3][2] \
 
            glVertex3f(x, y, z)

# Make spline
n = int(7)
points_r = ((0,0,0),(0,3,0),(1,3,0),(1,1,0),(2,1,0),(3,2,0),(3,0,0))
points = []
for i in range(n):
    points.append([])
    points[i].append(0)
    points[i].append(0)
    points[i].append(0)
    points[i][0] = points_r[i][0]
    points[i][1] = points_r[i][1]
    points[i][2] = points_r[i][2]
#points[0][0] = 0
#points[0][0] = 0
spline2 =  BSpline2(points, 10, False)
spline3 =  BSpline3(points, 10, False)

class Viewer(QGLViewer):

    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
        self.current_point_id = 0
        
    def draw(self):
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_TEXTURE_2D)
        spline2.draw_spline_curve()
        spline3.draw_spline_curve()
        spline2.draw_reference(self.current_point_id)
        
    def keyPressEvent(self,e):
        modifiers = e.modifiers()
        if (e.nativeVirtualKey()==Qt.Key_N):
            self.current_point_id = (self.current_point_id + 1) % int(len(points))
            spline2.draw_reference(self.current_point_id)
        elif (e.nativeVirtualKey()==Qt.Key_P):
            self.current_point_id = (self.current_point_id - 1) % int(len(points))
            spline2.draw_reference(self.current_point_id)
        elif (e.nativeVirtualKey()==Qt.Key_W):
            spline2.move_point(self.current_point_id, 0, 1, 0)
        elif (e.nativeVirtualKey()==Qt.Key_A):
            spline2.move_point(self.current_point_id, -1, 0, 0)
        elif (e.nativeVirtualKey()==Qt.Key_S):
            spline2.move_point(self.current_point_id, 0, -1, 0)
        elif (e.nativeVirtualKey()==Qt.Key_D):
            spline2.move_point(self.current_point_id, 1, 0, 0)
        self.updateGL()
        
  
def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()