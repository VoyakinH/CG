import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import design
import numpy as np
from math import fabs
import time

class Visual(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.label.setPalette(QtGui.QPalette(QtCore.Qt.white))
        self.black = QtGui.QColor(QtCore.Qt.black)
        self.white = QtGui.QColor(QtCore.Qt.white)
        self.colour = QtGui.QColor(QtCore.Qt.black)
        self.labelColour.setPalette(QtGui.QPalette(QtCore.Qt.black))
        self.labelColour.setAutoFillBackground(True)

        self.pm = QtGui.QPixmap(541, 436)
        self.pm.fill(self.white)
        self.img = self.pm.toImage()
        self.imgbg = self.pm.toImage()

        self.maxX = 0
        self.minX = 1500
        self.maxY = 0
        self.minY = 1500
        self.objX = np.array([], dtype=int)
        self.objY = np.array([], dtype=int)

        # Связи кнопок и функций.
        self.pushButtonScreenClean.clicked.connect(self.clean_screen)
        self.pushButtonChooseColour.clicked.connect(self.choose_color)
        self.pushButtonFill.clicked.connect(self.fill)
        self.pushButtonTime.clicked.connect(self.count_time)

    def bres_int(self, x_start, y_start, x_end, y_end):
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
            self.img.setPixel(x, y, self.black.rgb())
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

    def bres_int_special(self, x_start, y_start, x_end, y_end):
        dx = fabs(x_end - x_start)
        dy = fabs(y_end - y_start)
        stepx = sign(x_end - x_start)
        stepy = sign(y_end - y_start)
        if dy > dx:
            dx, dy = dy, dx
            flag = 1
        else:
            flag = 0
        e = 2 * dy - dx
        lasty = y_start
        x = x_start
        y = y_start
        for i in range(0, round(dx)):
            if lasty != y:
                lasty = y
                self.imgbg.setPixel(x, y, self.black.rgb())
            if e >= 0:
                if flag == 1:
                    x += stepx
                else:
                    y += stepy
                e -= 2 * dx
            if e < 0:
                if flag == 1:
                    y += stepy
                else:
                    x += stepx
            e += 2 * dy

    def add_extra_pixels(self, minX, minY, maxX, maxY):
        for y in range(minY, maxY + 1):
            flag = False
            for x in range(minX, maxX + 1):
                if flag and self.imgbg.pixelColor(x, y) == self.black:
                    flag = False
                    continue
                if self.imgbg.pixelColor(x, y) == self.black:
                    flag = True
                    bx = x
                    by = y
            if flag:
                self.imgbg.setPixel(bx + 1, by, self.black.rgb())


    def choose_color(self):
        self.colour = QtWidgets.QColorDialog.getColor()
        self.labelColour.setPalette(QtGui.QPalette(self.colour))

    def mousePressEvent(self, press):
        self.img = self.pm.toImage()
        if press.button() == QtCore.Qt.LeftButton:
            self.objX = np.append(self.objX, (press.pos() - self.label.pos()).x())
            self.objY = np.append(self.objY, (press.pos() - self.label.pos()).y())
            if self.objX.size >= 2:
                self.bres_int(self.objX[self.objX.size - 2], self.objY[self.objY.size - 2],
                              self.objX[self.objX.size - 1], self.objY[self.objY.size - 1])
                self.bres_int_special(self.objX[self.objX.size - 2], self.objY[self.objY.size - 2],
                                      self.objX[self.objX.size - 1], self.objY[self.objY.size - 1])
        elif press.button() == QtCore.Qt.RightButton:
            if self.objX.size >= 3:
                self.bres_int(self.objX[0], self.objY[0], self.objX[self.objX.size - 1], self.objY[self.objY.size - 1])
                self.bres_int_special(self.objX[0], self.objY[0],
                                      self.objX[self.objX.size - 1], self.objY[self.objY.size - 1])
                self.add_extra_pixels(min(self.objX), min(self.objY), max(self.objX), max(self.objY))
            if self.minX > min(self.objX):
                self.minX = min(self.objX)
            if self.maxX < max(self.objX):
                self.maxX = max(self.objX)
            if self.minY > min(self.objY):
                self.minY = min(self.objY)
            if self.maxY < max(self.objY):
                self.maxY = max(self.objY)
            self.objX = np.array([], dtype=int)
            self.objY = np.array([], dtype=int)
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)

    def wait(self, t):
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(t, loop.quit)
        loop.exec_()

    def update_image(self):
        self.pm = self.pm.fromImage(self.imgbg)
        self.label.setPixmap(self.pm)
        self.label.repaint()

    def fill(self, draw=True, delay=True):
        for y in range(self.minY, self.maxY + 1):
            flag = False
            for x in range(self.minX, self.maxX + 1):
                if self.imgbg.pixelColor(x, y) == self.black:
                    flag = not flag
                if flag:
                    self.imgbg.setPixel(x, y, self.colour.rgb())
                else:
                    self.imgbg.setPixel(x, y, self.white.rgb())
            if delay and int(self.lineEditDelay.text()) > 0:
                self.update_image()
                self.wait(int(self.lineEditDelay.text()))
        self.update_image()

    def count_time(self):
        start = time.time()
        self.fill(True, False)
        self.lineEditTime.setText(str(round(time.time() - start, 4)))
        self.lineEditTime.repaint()

    def clean_screen(self):
        self.pm.fill(self.white)
        self.imgbg = self.pm.toImage()
        self.label.setPixmap(self.pm)
        self.label.repaint()
        self.objX = np.array([], dtype=int)
        self.objY = np.array([], dtype=int)
        self.minX = 1500
        self.minY = 1500
        self.maxX = 0
        self.maxY = 0

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
