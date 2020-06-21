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
        self.white = QtGui.QColor(QtCore.Qt.white)
        self.black = QtGui.QColor(QtCore.Qt.black)
        self.colour_fill = QtGui.QColor(QtCore.Qt.black)
        self.colour_edge = QtGui.QColor(QtCore.Qt.black)

        self.labelColourEdges.setPalette(QtGui.QPalette(QtCore.Qt.black))
        self.labelColourFill.setPalette(QtGui.QPalette(QtCore.Qt.black))

        self.pm = QtGui.QPixmap(541, 436)
        self.pm.fill(self.white)
        self.img = self.pm.toImage()

        self.horizontal = False
        self.vertical = False

        self.objX = np.array([], dtype=int)
        self.objY = np.array([], dtype=int)
        self.pixel_x = 0
        self.pixel_y = 0

        # Связи кнопок и функций.
        self.pushButtonScreenClean.clicked.connect(self.clean_screen)
        self.pushButtonChooseColourEdges.clicked.connect(self.choose_color_edge)
        self.pushButtonChooseColourFill.clicked.connect(self.choose_color_fill)
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
            self.img.setPixel(x, y, self.colour_edge.rgb())
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

    def choose_color_fill(self):
        self.colour_fill = QtWidgets.QColorDialog.getColor()
        self.labelColourFill.setPalette(QtGui.QPalette(self.colour_fill))

    def choose_color_edge(self):
        self.colour_edge = QtWidgets.QColorDialog.getColor()
        self.labelColourEdges.setPalette(QtGui.QPalette(self.colour_edge))

    def mousePressEvent(self, press):
        self.img = self.pm.toImage()
        if press.button() == QtCore.Qt.LeftButton:
            if self.vertical:
                self.objX = np.append(self.objX, self.objX[self.objX.size - 1])
            else:
                self.objX = np.append(self.objX, (press.pos() - self.label.pos()).x())
            if self.horizontal:
                self.objY = np.append(self.objY, self.objY[self.objY.size - 1])
            else:
                self.objY = np.append(self.objY, (press.pos() - self.label.pos()).y())
            if self.objX.size >= 2:
                self.bres_int(self.objX[self.objX.size - 2], self.objY[self.objY.size - 2],
                              self.objX[self.objX.size - 1], self.objY[self.objY.size - 1])
        elif press.button() == QtCore.Qt.RightButton:
            self.pixel_x = (press.pos() - self.label.pos()).x()
            self.pixel_y = (press.pos() - self.label.pos()).y()
            self.img.setPixel(self.pixel_x, self.pixel_y, self.black.rgb())
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)

    def keyPressEvent(self, press):
        self.img = self.pm.toImage()
        if int(press.key()) == QtCore.Qt.Key_Shift:
            if self.objX.size >= 3:
                self.bres_int(self.objX[0], self.objY[0], self.objX[self.objX.size - 1], self.objY[self.objY.size - 1])
            self.objX = np.array([], dtype=int)
            self.objY = np.array([], dtype=int)
        elif int(press.key()) == QtCore.Qt.Key_H:
            self.horizontal = not self.horizontal
            self.vertical = False
        elif int(press.key()) == QtCore.Qt.Key_V:
            self.vertical = not self.vertical
            self.horizontal = False
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)

    def wait(self):
        t = int(self.lineEditDelay.text())
        if t > 0:
            self.update_image()
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(t, loop.quit)
        loop.exec_()

    def update_image(self):
        self.pm = self.pm.fromImage(self.img)
        self.label.setPixmap(self.pm)
        self.label.repaint()

    def fill(self):
        stack = [self.pixel_y, self.pixel_x]                        # Стек с начальным затр. пикселем.
        while len(stack) != 0:                                      # Цикл пока стек не пуст.
            p_x = stack.pop(); p_y = stack.pop()                    # Pop координат затравочного пиксела из стека.
            x = p_x; y = p_y                                        # Получение координат затравочного пиксела.
            x_buff = x                                              # Сохранение начальной позиции.
            while self.img.pixelColor(x, y).rgb() \
                    != self.colour_edge.rgb():                      # Цикл пока цвет пиксела отличен от цвета грани.
                if x == 0:
                    return
                self.img.setPixel(x, y, self.colour_fill.rgb())     # Высвечиваем пиксел цветом заполнения.
                x -= 1                                              # Движемся влево.
            x_left = x + 1                                          # Запомнили левую границу.
            x = x_buff + 1                                          # Вернулись на исходное положение заполнения + 1.
            while self.img.pixelColor(x, y).rgb() \
                    != self.colour_edge.rgb():                      # Цикл пока цвет пиксела отличен от цвета грани.
                self.img.setPixel(x, y, self.colour_fill.rgb())     # Высвечивание пиксела цветом заполнения.
                x += 1                                              # Движемся вправо.
            x_right = x - 1                                         # Запомнили правую границу.
            x = x_left; y += 1                                      # Переходим на строку выше в левую границу.
            for i in range(0, 2):                                   # Обрабатываем две строки (Выше и ниже).
                while x <= x_right:                                 # Цикл до правой границы.
                    flag = False                                    # Наличие пикселов для высвечивания.
                    while self.img.pixelColor(x, y).rgb() != self.colour_edge.rgb() and \
                            self.img.pixelColor(x, y).rgb() != self.colour_fill.rgb() and \
                            x <= x_right:                           # Цикл пока пиксел пуст.
                        flag = True                                 # Пикселы для высвечивания есть.
                        x += 1                                      # Движемся вправо.
                    if flag:                                        # Если есть пикселы для высвечивания.
                        if self.img.pixelColor(x, y).rgb() != self.colour_edge.rgb() and \
                                self.img.pixelColor(x, y).rgb() != self.colour_fill.rgb() and \
                                x == x_right:                    # Если достигли правой границы и пуст.
                            stack.append(y); stack.append(x)     # Заносим пиксел в стек.
                        else:
                            stack.append(y); stack.append(x - 1) # Иначе заносим предыдущий пиксел в стек.
                    x_buff = x                                      # Сохраняем текущий X.
                    while self.img.pixelColor(x, y).rgb() == self.colour_fill.rgb() and \
                           x < x_right:                             # Пока встречены заполненные пикселы.
                        x += 1                                      # Движемся вправо.
                    if x == x_buff:                                 # Если X не изменился.
                        x += 1                                      # Сдвигаемся вправо.
                y -= 2                                              # Переходим на строку вниз от начальной.
                x = x_left                                          # Переходим на левую границу.
                self.wait()                                         # Задержка если она больше 0
            self.update_image()                                     # Обновление изображения

    def count_time(self):
        start = time.time()
        self.fill()
        self.lineEditTime.setText(str(round(time.time() - start, 4)))
        self.lineEditTime.repaint()

    def clean_screen(self):
        self.pm.fill(self.white)
        self.img = self.pm.toImage()
        self.label.setPixmap(self.pm)
        self.label.repaint()
        self.objX = np.array([], dtype=int)
        self.objY = np.array([], dtype=int)

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
