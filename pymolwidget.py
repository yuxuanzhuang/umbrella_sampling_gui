## Source: https://gist.github.com/masci/6437112#file-pymolwidget-py

from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import *

from PyQt5.QtGui import QSurfaceFormat
from PyQt5 import QtCore
from PyQt5.Qt import Qt
from OpenGL.GL import *
import pymol2

buttonMap = {
    Qt.LeftButton:0,
    Qt.MidButton:1,
    Qt.RightButton:2,
}

class PyMolWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(PyMolWidget, self).__init__()

    def initializeGL(self):
        self._pymol = pymol2.PyMOL(scheme='widget')
        self._pymol.start()

#        self._pymol.cmd.set("internal_gui", 0)
#        self._pymol.cmd.set("internal_feedback", 0)
#        self._pymol.cmd.button("double_left", "None", "None")
#        self._pymol.cmd.button("single_right", "None", "None")

        self._pymol.reshape(self.width(), self.height())
        self.resizeGL(self.width(), self.height())
        self._pymolProcess()

    def paintGL(self):
        glViewport(0, 0, self.width(), self.height())
        self._pymol.idle()
        self._pymol.draw()

    def resizeGL(self, w, h):
        self._pymol.reshape(w, h, True)
        self._pymolProcess()

    def loadMolFile(self, mol_file,**argv):
        self._pymol.cmd.load(str(mol_file),**argv)
        self._pymol.cmd.hide("all")

        self._pymolProcess()

    def ShowSelect(self, representation = "nb_spheres", select = "all"):
        self._pymol.cmd.show(representation,select)
        self._pymolProcess()

    def HideSelect(self, representation = "nb_spheres", select = "all"):
        self._pymol.cmd.hide(representation,select)
        self._pymolProcess()

    def HideAll(self, select = "all"):
        self._pymol.cmd.hide(select)
        self._pymolProcess()

    def DeleteSelect(self,name = "all"):
        self._pymol.cmd.delete(name)
        self._pymolProcess()

    def CalculateDistance(self,name,sele1,sele2,mode=4):
        distance = self._pymol.cmd.distance(name = name,selection1 = sele1,selection2 = sele2,cutoff = 1000, mode = mode)
        return distance

    def _pymolProcess(self):
        self._pymol.idle()
        self.update()

    def mouseMoveEvent(self, ev):
        self._pymol.drag(ev.x(), self.height() - ev.y(), 0)
        self._pymolProcess()

    def mousePressEvent(self, ev):
        self._pymol.button(buttonMap[ev.button()], 0, ev.x(), self.height() - ev.y(), 0)
        self._pymolProcess()

    def mouseReleaseEvent(self, ev):
        self._pymol.button(buttonMap[ev.button()], 1, ev.x(), self.height() - ev.y(), 0)
        self._pymolProcess()

    def wheelEvent(self, ev):
        button = 3 if (ev.angleDelta().x() > 0 or ev.angleDelta().y() > 0) else 4
        self._pymol.button(button, 0, ev.x(), ev.y(), 0)
        self._pymolProcess()
