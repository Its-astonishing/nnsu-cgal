#convex_hull_2d.py
from __future__ import print_function
from CGAL.CGAL_Kernel import Point_3
from CGAL.CGAL_Polyhedron_3 import Polyhedron_3
from CGAL import CGAL_Convex_hull_3
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQGLViewer import *
from OpenGL.GL import *
import random

class Points:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Viewer(QGLViewer):

    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
        self.is_points_generated = False
        self.is_hull_generated = False
        self.points = []
        self.convex_hull = Polyhedron_3()
        
    def generate_points(self):
        points_count = 100
        for i in range(points_count):
            x = random.uniform(0.0, 1.0)
            y = random.uniform(0.0, 1.0)
            z = random.uniform(0.0, 1.0)
            self.points.append(Point_3(x, y, z))
            
        self.is_points_generated = True
           
    def draw_points(self):
        if (not self.is_points_generated):
            self.generate_points()
        glBegin(GL_POINTS)
        for point in self.points:
            glVertex3f(point.x(), point.y(), point.z())
        glEnd()
        
    def create_convex_hull(self):
        CGAL_Convex_hull_3.convex_hull_3(self.points, self.convex_hull)
        self.is_hull_generated = False
        
    def draw_convex_hull(self):
        if (not self.is_hull_generated):
            self.create_convex_hull()

        #points_count = self.convex_hull.size_of_vertices()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_COLOR, GL_ONE_MINUS_SRC_COLOR)
        glBegin(GL_TRIANGLES)
        glColor3f(0.0, 0.0, 0.6)
        
        for face in self.convex_hull.facets():
            p1 = face.halfedge()
            glVertex3f(p1.vertex().point().x(), p1.vertex().point().y(), p1.vertex().point().z())
            p2 = p1.next()
            glVertex3f(p2.vertex().point().x(), p2.vertex().point().y(), p2.vertex().point().z())
            p3 = p2.next()
            glVertex3f(p3.vertex().point().x(), p3.vertex().point().y(), p3.vertex().point().z())
        glEnd()
        glDisable(GL_BLEND)
    
    def draw(self):
        glPointSize(4)
        self.draw_points()
        self.draw_convex_hull()

    def keyPressEvent(self,e):
        modifiers = e.modifiers()
        if (e.nativeVirtualKey()==Qt.Key_G):
            self.is_points_generated = False
            self.points.clear()
        self.updateGL()

def print_2d_points(points):
    for p in points:
        print(f"({p})", end = " ")
    print()
    print("====")
 




def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()