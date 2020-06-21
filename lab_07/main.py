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
        self.labelColourLineIn.setPalette(QtGui.QPalette(QtCore.Qt.darkGreen))
        self.labelColourLineOut.setPalette(QtGui.QPalette(QtCore.Qt.red))

        self.pm = QtGui.QPixmap(541, 436)
        self.pm.fill(self.white)
        self.img = self.pm.toImage()

        self.horizontal = False
        self.vertical = False

        self.p_x = []
        self.p_y = []

        self.left_click_num = 0
        self.cutter_ld_x = 0
        self.cutter_ld_y = 0
        self.cutter_ru_x = 0
        self.cutter_ru_y = 0

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
            if self.vertical:
                self.p_x.append(self.p_x[len(self.p_x) - 1])
            else:
                self.p_x.append((press.pos() - self.label.pos()).x())
            if self.horizontal:
                self.p_y.append(self.p_y[len(self.p_y) - 1])
            else:
                self.p_y.append((press.pos() - self.label.pos()).y())
            if len(self.p_x) % 2 == 0:
                self.bres_int(self.p_x[len(self.p_x) - 2], self.p_y[len(self.p_y) - 2],
                              self.p_x[len(self.p_x) - 1], self.p_y[len(self.p_y) - 1], self.colour_line_out)
        elif press.button() == QtCore.Qt.RightButton:
            if self.left_click_num == 0:
                self.cutter_ld_x = (press.pos() - self.label.pos()).x()
                self.cutter_ld_y = (press.pos() - self.label.pos()).y()
            elif self.left_click_num == 1:
                self.cutter_ru_x = (press.pos() - self.label.pos()).x()
                self.cutter_ru_y = (press.pos() - self.label.pos()).y()
                self.bres_int(self.cutter_ld_x, self.cutter_ld_y, self.cutter_ld_x, self.cutter_ru_y, self.colour_cutter)
                self.bres_int(self.cutter_ld_x, self.cutter_ld_y, self.cutter_ru_x, self.cutter_ld_y, self.colour_cutter)
                self.bres_int(self.cutter_ld_x, self.cutter_ru_y, self.cutter_ru_x, self.cutter_ru_y, self.colour_cutter)
                self.bres_int(self.cutter_ru_x, self.cutter_ld_y, self.cutter_ru_x, self.cutter_ru_y, self.colour_cutter)
            self.left_click_num += 1
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)

    def keyPressEvent(self, press):
        if int(press.key()) == QtCore.Qt.Key_H:
            self.horizontal = not self.horizontal
            self.vertical = False
        elif int(press.key()) == QtCore.Qt.Key_V:
            self.vertical = not self.vertical
            self.horizontal = False

    def proc(self):
        self.img = self.pm.toImage()
        for i in range(0, len(self.p_x), 2):
            self.makeCut(self.p_x[i], self.p_y[i], self.p_x[i + 1], self.p_y[i + 1])
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)
        self.label.repaint()

    def makeCut(self, p1_x, p1_y, p2_x, p2_y):
        t1 = [0, 0, 0, 0]
        t2 = [0, 0, 0, 0]
        p1res_x = p1_x
        p1res_y = p1_y
        p2res_x = p2_x
        p2res_y = p2_y
        sum1 = 0
        sum2 = 0
        mult = 0
        flag = True
        number = 0
        m = inf
        if p1_x < self.cutter_ld_x: t1[3] = 1
        if p1_x > self.cutter_ru_x: t1[2] = 1
        if p1_y < self.cutter_ld_y: t1[1] = 1
        if p1_y > self.cutter_ru_y: t1[0] = 1
        if p2_x < self.cutter_ld_x: t2[3] = 1
        if p2_x > self.cutter_ru_x: t2[2] = 1
        if p2_y < self.cutter_ld_y: t2[1] = 1
        if p2_y > self.cutter_ru_y: t2[0] = 1
        for i in range(0, 4):
            sum1 += t1[i]
            sum2 += t2[i]
        if sum1 == 0 and sum2 == 0:
            goto .q7
        for i in range(0, 4):
            mult += (t1[i] + t2[i]) // 2
            if mult != 0:
                flag = False
                goto .q7
        if sum1 == 0:
            number = 1
            p1res_x = p1_x; p1res_y = p1_y
            p_x = p2_x; p_y = p2_y
            goto .q2
        if sum2 == 0:
            number = 2
            p1res_x = p2_x; p1res_y = p2_y
            p_x = p1_x; p_y = p1_y
            goto .q2
        number = 0

        label .q1
        if number != 0:
            if number == 1: p1res_x = p_x; p1res_y = p_y
            else: p2res_x = p_x; p2res_y = p_y
        number += 1
        if number > 2:
            goto .q7
        if number == 1: p_x = p1_x; p_y = p1_y
        else: p_x = p2_x; p_y = p2_y

        label .q2
        if p2_x - p1_x == 0:
            goto .q4
        m = (p2_y - p1_y) / (p2_x - p1_x)
        if self.cutter_ld_x < p_x:
            goto .q3
        y = m * (self.cutter_ld_x - p_x) + p_y
        if self.cutter_ru_y < y < self.cutter_ld_y:
            goto .q3
        p_y = y; p_x = self.cutter_ld_x
        goto .q1

        label .q3
        if self.cutter_ru_x > p_x:
            goto .q4
        y = m * (self.cutter_ru_x - p_x) + p_y
        if self.cutter_ru_y < y < self.cutter_ld_y:
            goto .q4
        p_y = y; p_x = self.cutter_ru_x
        goto .q1

        label .q4
        if self.cutter_ru_y > p_y:
            goto .q5
        x = (1 / m) * (self.cutter_ru_y - p_y) + p_x
        if self.cutter_ru_x < x < self.cutter_ld_x:
            goto .q5
        p_x = x; p_y = self.cutter_ru_y
        goto .q1

        label .q5
        if self.cutter_ld_y < p_y:
            return
        x = (1 / m) * (self.cutter_ld_y - p_y) + p_x
        if self.cutter_ru_x < x < self.cutter_ld_x:
            goto .q6
        p_x = x; p_y = self.cutter_ld_y
        goto .q1

        label .q6
        flag = False

        label .q7
        if not flag:
            goto .q8
        self.bres_int(p1res_x, p1res_y, p2res_x, p2res_y, self.colour_line_in)

        label .q8
        return

    def clean_screen(self):
        self.pm.fill(self.white)
        self.img = self.pm.toImage()
        self.label.setPixmap(self.pm)
        self.label.repaint()
        self.p_x = []
        self.p_y = []
        self.left_click_num = 0

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
