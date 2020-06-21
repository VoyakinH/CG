import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import design
from math import fabs, inf
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
            if len(self.p_x) % 2 == 0:
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
        if int(press.key()) == QtCore.Qt.Key_H:
            self.horizontal = not self.horizontal
            self.vertical = False
        elif int(press.key()) == QtCore.Qt.Key_V:
            self.vertical = not self.vertical
            self.horizontal = False
        elif int(press.key()) == QtCore.Qt.Key_Shift:
            self.img = self.pm.toImage()
            self.bres_int(self.cutter_x[0], self.cutter_y[0], self.cutter_x[len(self.cutter_x) - 1],
                          self.cutter_y[len(self.cutter_y) - 1], self.colour_cutter)
            self.pm = self.pm.fromImage(self.img)
            self.label.setPixmap(self.pm)

    def proc(self):
        self.img = self.pm.toImage()
        obh = -1
        xv1 = self.cutter_x[1] - self.cutter_x[0]
        yv1 = self.cutter_y[1] - self.cutter_y[0]
        xv2 = self.cutter_x[2] - self.cutter_x[1]
        yv2 = self.cutter_y[2] - self.cutter_y[1]
        if xv1 * yv2 - yv1 * xv2 > 0:
            obh = 1
        for i in range(0, len(self.p_x), 2):
            self.makeCut(self.p_x[i], self.p_y[i], self.p_x[i + 1], self.p_y[i + 1], obh)
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)
        self.label.repaint()

    def makeCut(self, p1_x, p1_y, p2_x, p2_y, obh):
        t_begin = 0
        t_end = 1
        t = 0
        d_x = p2_x - p1_x
        d_y = p2_y - p1_y
        for i in range(0, len(self.cutter_x)):
            w_x = p1_x - self.cutter_x[i]; w_y = p1_y - self.cutter_y[i]
            n_x = (-self.cutter_y[(i + 1) % len(self.cutter_y)] + self.cutter_y[i]) * obh
            n_y = (self.cutter_x[(i + 1) % len(self.cutter_x)] - self.cutter_x[i]) * obh
            Wsc = w_x * n_x + w_y * n_y
            Dsc = d_x * n_x + d_y * n_y
            if Dsc == 0:
                goto .q2
            t = - Wsc / Dsc
            if Dsc > 0:
                goto .q1
            if t < 0:
                goto .q4
            t_end = min(t, t_end)
            goto .q3

            label .q1
            if t > 1:
                goto .q4
            t_begin = max(t, t_begin)
            goto .q3

            label .q2
            if Wsc < 0:
                goto .q4

            label .q3
        if t_begin > t_end:
            goto .q4
        self.bres_int(p1_x + (p2_x - p1_x) * t_end, p1_y + (p2_y - p1_y) * t_end,
                      p1_x + (p2_x - p1_x) * t_begin, p1_y + (p2_y - p1_y) * t_begin, self.colour_line_in)

        label .q4
        return

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
