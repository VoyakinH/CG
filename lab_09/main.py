import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import design
from numpy.linalg import inv
from numpy import dot
from math import fabs
from trace_goto import goto, label

class Visual(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label.setPalette(QtGui.QPalette(QtCore.Qt.white))
        self.white = QtGui.QColor(QtCore.Qt.white)

        self.colour_line_out = QtGui.QColor(QtCore.Qt.red)
        self.colour_line_in = QtGui.QColor(QtCore.Qt.darkGreen)
        self.colour_cutter = QtGui.QColor(QtCore.Qt.black)

        self.labelColourCutter.setPalette(QtGui.QPalette(QtCore.Qt.black))
        self.labelColourLineIn.setPalette(QtGui.QPalette(QtCore.Qt.darkBlue))
        self.labelColourLineOut.setPalette(QtGui.QPalette(QtCore.Qt.red))

        self.pm = QtGui.QPixmap(541, 436)
        self.pm.fill(self.white)
        self.img = self.pm.toImage()

        self.horizontal = False
        self.vertical = False

        self.p_x = []
        self.p_y = []
        self.cutter_x = []
        self.cutter_y = []

        # Связи кнопок и функций.
        self.pushButtonScreenClean.clicked.connect(self.clean_screen)
        self.pushButtonProc.clicked.connect(self.proc)

    def bres_int(self, x_start, y_start, x_end, y_end, colour):
        dx = x_end - x_start
        dy = y_end - y_start
        sx = sign(dx)
        sy = sign(dy)
        dx = fabs(dx)
        dy = fabs(dy)
        if dy >= dx:
            dx, dy = dy, dx
            fl = 1
        else:
            fl = 0
        f = 2 * dy - dx
        x = round(x_start)
        y = round(y_start)
        i = 1
        while i <= dx + 1:
            self.img.setPixel(x, y, colour.rgb())
            if f >= 0:
                if fl == 1:
                    x += sx
                else:
                    y += sy
                f -= 2 * dx
            if f <= 0:
                if fl == 1:
                    y += sy
                else:
                    x += sx
                f += 2 * dy
            i += 1

    def mousePressEvent(self, press):
        if press.pos().x() < self.label.pos().x() or press.pos().y() < self.label.pos().y():
            return
        self.img = self.pm.toImage()
        if press.button() == QtCore.Qt.LeftButton:
            if self.vertical and len(self.p_x) > 0:
                self.p_x.append(self.p_x[len(self.p_x) - 1])
            else:
                self.p_x.append((press.pos() - self.label.pos()).x())
            if self.horizontal and len(self.p_y) > 0:
                self.p_y.append(self.p_y[len(self.p_y) - 1])
            else:
                self.p_y.append((press.pos() - self.label.pos()).y())
            if len(self.p_x) > 1:
                self.bres_int(self.p_x[len(self.p_x) - 2], self.p_y[len(self.p_y) - 2],
                              self.p_x[len(self.p_x) - 1], self.p_y[len(self.p_y) - 1], self.colour_line_out)
        elif press.button() == QtCore.Qt.RightButton:
            self.cutter_x.append((press.pos() - self.label.pos()).x())
            self.cutter_y.append((press.pos() - self.label.pos()).y())
            if len(self.cutter_x) > 1:
                self.bres_int(self.cutter_x[len(self.cutter_x) - 2], self.cutter_y[len(self.cutter_y) - 2],
                              self.cutter_x[len(self.cutter_x) - 1], self.cutter_y[len(self.cutter_y) - 1],
                              self.colour_cutter)
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)

    def keyPressEvent(self, press):
        self.img = self.pm.toImage()
        if int(press.key()) == QtCore.Qt.Key_H:
            self.horizontal = not self.horizontal
            self.vertical = False
        elif int(press.key()) == QtCore.Qt.Key_V:
            self.vertical = not self.vertical
            self.horizontal = False
        elif int(press.key()) == QtCore.Qt.Key_Shift:
            self.bres_int(self.cutter_x[0], self.cutter_y[0], self.cutter_x[len(self.cutter_x) - 1],
                          self.cutter_y[len(self.cutter_y) - 1], self.colour_cutter)
        elif int(press.key()) == QtCore.Qt.Key_Control:
            self.bres_int(self.p_x[0], self.p_y[0], self.p_x[len(self.p_x) - 1],
                          self.p_y[len(self.p_y) - 1], self.colour_line_out)
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)

    def proc(self):
        self.img = self.pm.toImage()
        self.makeCut()
        for i in range(0, len(self.p_x) - 1):
            self.bres_int(self.p_x[i], self.p_y[i], self.p_x[i + 1], self.p_y[i + 1], self.colour_line_in)
        self.bres_int(self.p_x[0], self.p_y[0], self.p_x[len(self.p_x) - 1], self.p_y[len(self.p_y) - 1],
                      self.colour_line_in)
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)
        self.label.repaint()

    def visibility(self, x, y, w1_x, w1_y, w2_x, w2_y):
        buff_1 = (x - w1_x) * (w2_y - w1_y)
        buff_2 = (y - w1_y) * (w2_x - w1_x)
        buff_1 -= buff_2
        return sign(buff_1)

    def is_crossing(self, s_x, s_y, buff_x, buff_y, w1_x, w1_y, w2_x, w2_y):
        vis_1 = self.visibility(s_x, s_y, w1_x, w1_y, w2_x, w2_y)
        vis_2 = self.visibility(buff_x, buff_y, w1_x, w1_y, w2_x, w2_y)
        if vis_1 * vis_2 < 0:
            return True
        return False

    def crossing(self, p1_x, p1_y, p2_x, p2_y, w1_x, w1_y, w2_x, w2_y):
        coef = [[p2_x - p1_x, w1_x - w2_x], [p2_y - p1_y, w1_y - w2_y]]
        prav = [w1_x - p1_x, w1_y - p1_y]
        coef = inv(coef)
        param = coef.dot(prav)
        return p1_x + (p2_x - p1_x) * param[0], p1_y + (p2_x - p1_x) * param[0]

    def makeCut(self):
        for i in range(0, len(self.cutter_x)):
            q_x = []; q_y = []
            w1_x = self.cutter_x[i]; w1_y = self.cutter_y[i]
            w2_x = self.cutter_x[(i + 1) % len(self.cutter_x)]; w2_y = self.cutter_y[(i + 1) % len(self.cutter_y)]
            for j in range(0, len(self.p_x)):
                if j != 0:
                    goto .q1
                buff_x = self.p_x[j]; buff_y = self.p_y[j]
                goto .q2

                label .q1
                if not self.is_crossing(s_x, s_y, self.p_x[j], self.p_y[j], w1_x, w1_y, w2_x, w2_y):
                    goto .q2
                per = self.crossing(s_x, s_y, self.p_x[j], self.p_y[j], w1_x, w1_y, w2_x, w2_y)
                q_x.append(per[0]); q_y.append(per[1])

                label .q2
                s_x = self.p_x[j]; s_y = self.p_y[j]
                if self.visibility(s_x, s_y, w1_x, w1_y, w2_x, w2_y) < 0:
                    goto .q3
                q_x.append(s_x); q_y.append(s_y)

            label .q3
            if len(q_x) == 0:
                goto .q4
            if not self.is_crossing(s_x, s_y, buff_x, buff_y, w1_x, w1_y, w2_x, w2_y):
                goto .q4
            per = self.crossing(s_x, s_y, buff_x, buff_y, w1_x, w1_y, w2_x, w2_y)
            q_x.append(per[0]); q_y.append(per[1])

            label .q4
            self.p_x = q_x; self.p_y = q_y


    def clean_screen(self):
            self.pm.fill(self.white)
            self.img = self.pm.toImage()
            self.label.setPixmap(self.pm)
            self.label.repaint()
            self.p_x = []
            self.p_y = []
            self.cutter_x = []
            self.cutter_y = []

def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    return 0

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Visual()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
