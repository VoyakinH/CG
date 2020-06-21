import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import design
from math import fabs

class Visual(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label.setPalette(QtGui.QPalette(QtCore.Qt.white))
        self.white = QtGui.QColor(QtCore.Qt.white)
        self.black = QtGui.QColor(QtCore.Qt.black)

        self.pm = QtGui.QPixmap(541, 436)
        self.pm.fill(self.white)
        self.img = self.pm.toImage()

        # Связи кнопок и функций.
        self.pushButtonScreenClean.clicked.connect(self.clean_screen)
        self.pushButtonDraw.clicked.connect(self.proc)

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

    def proc(self):
        self.img = self.pm.toImage()
        self.AlgHor()
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)
        self.label.repaint()

    def hor(self, x1, y1, x2, y2, top, bottom):
        if x2 - x1 == 0:
            top[x2] = max(top[x2], y2)
            bottom[x2] = min(bottom[x2], y2)
        else:
            t = (y2 - y1) / (x2 - x1)
            for x in range(x1, x2 + 1):
                y = t * (x - x1) + y1
                top[x] = max(top[x], y)
                bottom[x] = min(bottom[x], y)

    def obr_r(self, x, y, x_reb, y_reb, top, bottom):
        if x_reb != -1:
            self.hor(x_reb, y_reb, x, y, top, bottom)
        return x, y

    def visability(self, x, y, top, bottom):
        if bottom[x] < y < top[x]:
            return 0
        elif y >= top[x]:
            return 1
        elif y <= bottom[x]:
            return -1

    def crossing(self, x1, y1, x2, y2, hor):
        if x2 - x1 == 0:
            xi = x2
            yi = hor[x2]
        else:
            t = (y2 - y1) / (x2 - x1)
            y_sign = sign(y1 + t - hor[x1 + 1])
            c_sign = y_sign
            yi = y1 + t
            xi = x1 + 1
            while c_sign == y_sign:
                yi += t
                xi += 1
                c_sign = sign(yi - hor[xi])
            if fabs(yi - t - hor[xi - 1]) <= fabs(yi - hor[xi]):
                yi -= t
                xi -= 1
        return xi, yi

    def AlgHor(self):
        h = 556
        top = [0]
        bottom = [h]
        x_left = -1
        y_left = -1
        x_right = -1
        y_right = -1
        for z in range(int(self.lineEditZend.text()), int(self.lineEditZstart.text()) - 1, -int(self.lineEditZstep.text())):
            x_prev = int(self.lineEditXstart.text())
            y_prev = self.f(x_prev, z)
            x_prev, y_prev = self.obr_r(x_prev, y_prev, x_left, y_left, top, bottom)
            flag_vis = self.visability(x_prev, y_prev, top, bottom)
            for x in range(int(self.lineEditZstart.text()), int(self.lineEditXend.text()), int(self.lineEditXstep.text())):
                y = self.f(x, z)
                flag_t = self.visability(x, y, top, bottom)
                if flag_t == flag_vis:
                    if flag_t == 1 or flag_t == -1:
                        self.bres_int(x_prev, y_prev, x, y, self.black)
                        self.hor(x_prev, y_prev, x, y, top, bottom)
                else:
                    if flag_t == 0:
                        if flag_vis == 1:
                            xi, yi = self.crossing(x_prev, y_prev, x, y, top)
                        else:
                            xi, yi = self.crossing(x_prev, y_prev, x, y, bottom)
                        self.bres_int(x_prev, y_prev, xi, yi, self.black)
                        self.hor(x_prev, y_prev, xi, yi, top, bottom)
                    else:
                        if flag_t == 1:
                            if flag_vis == 0:
                                xi, yi = self.crossing(x_prev, y_prev, x, y)
                                self.bres_int(x_prev, y_prev, xi, yi, self.black)
                                self.hor(xi, yi, x, y, top, bottom)
                            else:
                                xi, yi = self.crossing(x_prev, y_prev, x, y, bottom)
                                self.bres_int(x_prev, y_prev, xi, yi, self.black)
                                self.hor(x_prev, y_prev, xi, yi, top, bottom)
                                xi, yi = self.crossing(x_prev, y_prev, x, y, top)
                                self.bres_int(xi, yi, x, y, self.black)
                                self.hor(xi, yi, x, y, top, bottom)
                        else:
                            if flag_vis == 0:
                                xi, yi = self.crossing(x_prev, y_prev, x, y, top)
                                self.bres_int(xi, yi, x, y, self.black)
                                self.hor(xi, yi, x, y, top, bottom)
                            else:
                                xi, yi = self.crossing(x_prev, y_prev, x, y, top)
                                self.bres_int(x_prev, y_prev, xi, yi, self.black)
                                self.hor(x_prev, y_prev, xi, yi, top, bottom)
                                xi, yi = self.crossing(x_prev, y_prev, x, y, bottom)
                                self.bres_int(xi, yi, x, y, self.black)
                                self.hor(xi, yi, x, y, top, bottom)
                flag_vis = flag_t
                x_prev = x
                y_prev = y
            self.obr_r(x, y, x_right, y_right, top, bottom)

    def clean_screen(self):
        self.pm.fill(self.white)
        self.img = self.pm.toImage()
        self.label.setPixmap(self.pm)
        self.label.repaint()

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
