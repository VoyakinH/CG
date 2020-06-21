import sys
from copy import deepcopy
from PyQt5 import QtWidgets, QtCore
from math import sin, cos, pi, radians
import design

class Visual(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.graphicsView.scale(1, -1)
        self.arr_walls = []  # Массив точек для стен дома.
        self.arr_l_wind = []  # Массив точек левого окна.
        self.arr_l_ell = []  # Массив точек левого эллипса.
        self.arr_r_wind = []  # Массив точек правого окна.
        self.arr_r_ell = []  # Массив точек правого эллипса.
        self.arr_u_ell = []  # Массив точек верхнего эллипса.
        self.arr_hatch = []  # Массив штрихов у верхнего эллипса.

        # Массивы для возврата на один шаг назад.
        self.arr_walls_buff = []; self.arr_l_wind_buff = []; self.arr_l_ell_buff = []; self.arr_r_wind_buff = []
        self.arr_r_ell_buff = []; self.arr_u_ell_buff = []; self.arr_hatch_buff = []

        # Связи кнопок и функций.
        self.pushButton_draw_base.clicked.connect(self.draw_base)
        self.pushButton_back.clicked.connect(self.step_back)
        self.button_move.clicked.connect(self.move_func)
        self.button_scale.clicked.connect(self.scale_func)
        self.button_rotate.clicked.connect(self.rotate_func)

    # Вычисление начальных координат фигуры.
    def init_base_data(self):
        self.arr_walls = [[-50, 100], [-100, 30], [-100, -100], [100, -100], [100, 30]]
        self.arr_l_wind = [[-50, 10], [-85, -5], [-85, -65], [-50, -65], [-15, -65], [-15, -5], [-50, -5]]
        self.arr_r_wind = [[50, 10], [30, -27.5], [50, -65], [70, -27.5], [50, -27.5]]
        self.arr_hatch = [[-54.6, 63.4], [-43.4, 74.6], [-53.2, 52.8], [-32.8, 73.2], [-47.2, 46.8], [-26.8, 67.2],
                          [-36.6, 45.4], [-25.4, 56.6]]
        self.arr_l_ell.clear()
        self.arr_r_ell.clear()
        self.arr_u_ell.clear()
        a = 35; b = 15; t = 0; xc = -50; yc = -5; h = 1 / 35
        while t <= pi:
            x = xc + a * cos(t)
            y = yc + b * sin(t)
            self.arr_l_ell.append([x, y])
            t += h
        a = 20; b = 37.5; t = 0; xc = 50; yc = -27.5; h = 1 / 37.5
        while t <= 2 * pi:
            x = xc + a * cos(t)
            y = yc + b * sin(t)
            self.arr_r_ell.append([x, y])
            t += h
        a = 15; b = 15; t = 0; xc = -40; yc = 60; h = 1 / 15
        while t <= 2 * pi:
            x = xc + a * cos(t)
            y = yc + b * sin(t)
            self.arr_u_ell.append([x, y])
            t += h

    # Рисование фигуры.
    def draw(self):
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(scene)
        h = self.graphicsView.height()
        w = self.graphicsView.width()
        scene.setSceneRect(-w/2, -h/2, w - 2, h - 2)
        if len(self.arr_walls) == 0:
            self.lineEdit_center_x.setText("0")
            self.lineEdit_center_y.setText("0")
            self.graphicsView.repaint()
            return

        # Рисование стен дома.
        scene.addLine(self.arr_walls[0][0], self.arr_walls[0][1], self.arr_walls[1][0], self.arr_walls[1][1])
        scene.addLine(self.arr_walls[1][0], self.arr_walls[1][1], self.arr_walls[2][0], self.arr_walls[2][1])
        scene.addLine(self.arr_walls[2][0], self.arr_walls[2][1], self.arr_walls[3][0], self.arr_walls[3][1])
        scene.addLine(self.arr_walls[3][0], self.arr_walls[3][1], self.arr_walls[4][0], self.arr_walls[4][1])
        scene.addLine(self.arr_walls[4][0], self.arr_walls[4][1], self.arr_walls[0][0], self.arr_walls[0][1])
        scene.addLine(self.arr_walls[4][0], self.arr_walls[4][1], self.arr_walls[1][0], self.arr_walls[1][1])

        # Рисование левого окна.
        scene.addLine(self.arr_l_wind[1][0], self.arr_l_wind[1][1], self.arr_l_wind[2][0], self.arr_l_wind[2][1])
        scene.addLine(self.arr_l_wind[2][0], self.arr_l_wind[2][1], self.arr_l_wind[4][0], self.arr_l_wind[4][1])
        scene.addLine(self.arr_l_wind[4][0], self.arr_l_wind[4][1], self.arr_l_wind[5][0], self.arr_l_wind[5][1])
        scene.addLine(self.arr_l_wind[5][0], self.arr_l_wind[5][1], self.arr_l_wind[1][0], self.arr_l_wind[1][1])
        scene.addLine(self.arr_l_wind[0][0], self.arr_l_wind[0][1], self.arr_l_wind[3][0], self.arr_l_wind[3][1])
        for i in range(len(self.arr_l_ell) - 1):
            scene.addLine(self.arr_l_ell[i][0], self.arr_l_ell[i][1], self.arr_l_ell[i+1][0], self.arr_l_ell[i+1][1])

        # Рисование правого окна.
        scene.addLine(self.arr_r_wind[0][0], self.arr_r_wind[0][1], self.arr_r_wind[2][0], self.arr_r_wind[2][1])
        scene.addLine(self.arr_r_wind[1][0], self.arr_r_wind[1][1], self.arr_r_wind[3][0], self.arr_r_wind[3][1])
        for i in range(len(self.arr_r_ell) - 1):
            scene.addLine(self.arr_r_ell[i][0], self.arr_r_ell[i][1], self.arr_r_ell[i+1][0], self.arr_r_ell[i+1][1])

        # Рисование верхнего окна.
        for i in range(len(self.arr_u_ell) - 1):
            scene.addLine(self.arr_u_ell[i][0], self.arr_u_ell[i][1], self.arr_u_ell[i+1][0], self.arr_u_ell[i+1][1])
        for i in range(0, 7, 2):
            scene.addLine(self.arr_hatch[i][0], self.arr_hatch[i][1], self.arr_hatch[i+1][0], self.arr_hatch[i+1][1])

        self.graphicsView.repaint()

        # Обновление информации о центре фигуры.
        x = QtCore.QPointF.x(QtCore.QRectF.center(scene.itemsBoundingRect())) + 0.1
        y = QtCore.QPointF.y(QtCore.QRectF.center(scene.itemsBoundingRect()))
        self.lineEdit_center_x.setText(str(int(x)))
        self.lineEdit_center_y.setText(str(int(y)))
        self.repaint()

    # Копирование массивов для возврата на шаг назад.
    def copy(self):
        self.arr_walls_buff = deepcopy(self.arr_walls)
        self.arr_l_wind_buff = deepcopy(self.arr_l_wind)
        self.arr_l_ell_buff = deepcopy(self.arr_l_ell)
        self.arr_r_wind_buff = deepcopy(self.arr_r_wind)
        self.arr_r_ell_buff = deepcopy(self.arr_r_ell)
        self.arr_u_ell_buff = deepcopy(self.arr_u_ell)
        self.arr_hatch_buff = deepcopy(self.arr_hatch)

    # Обработчик события рисования исходного изображения.
    def draw_base(self):
        self.copy()
        self.init_base_data()
        self.draw()

    # Обработчик события возврата на шаг назад.
    def step_back(self):
        self.arr_walls_buff, self.arr_walls = self.arr_walls, self.arr_walls_buff
        self.arr_l_wind_buff, self.arr_l_wind = self.arr_l_wind, self.arr_l_wind_buff
        self.arr_l_ell_buff, self.arr_l_ell = self.arr_l_ell, self.arr_l_ell_buff
        self.arr_r_wind_buff, self.arr_r_wind = self.arr_r_wind, self.arr_r_wind_buff
        self.arr_r_ell_buff, self.arr_r_ell = self.arr_r_ell, self.arr_r_ell_buff
        self.arr_u_ell_buff, self.arr_u_ell = self.arr_u_ell, self.arr_u_ell_buff
        self.arr_hatch_buff, self.arr_hatch = self.arr_hatch, self.arr_hatch_buff
        self.draw()

    # Обработчик события перемещения фигуры
    def move_func(self):
        try:
            dx = int(self.lineEdit_dx.text())
            dy = int(self.lineEdit_dy.text())
        except:
            QtWidgets.QMessageBox.critical(self, "", "Расстояние переноса должно быть целым числом.")
            return
        self.copy()
        for i in range(len(self.arr_walls)):
            self.arr_walls[i][0] += dx; self.arr_walls[i][1] += dy
        for i in range(len(self.arr_l_wind)):
            self.arr_l_wind[i][0] += dx; self.arr_l_wind[i][1] += dy
        for i in range(len(self.arr_r_wind)):
            self.arr_r_wind[i][0] += dx; self.arr_r_wind[i][1] += dy
        for i in range(len(self.arr_hatch)):
            self.arr_hatch[i][0] += dx; self.arr_hatch[i][1] += dy
        for i in range(len(self.arr_l_ell)):
            self.arr_l_ell[i][0] += dx; self.arr_l_ell[i][1] += dy
        for i in range(len(self.arr_r_ell)):
            self.arr_r_ell[i][0] += dx; self.arr_r_ell[i][1] += dy
        for i in range(len(self.arr_u_ell)):
            self.arr_u_ell[i][0] += dx; self.arr_u_ell[i][1] += dy
        self.draw()

    # Обработчик события масштабирования фигуры.
    def scale_func(self):
        try:
            kx = float(self.lineEdit_KX.text())
            ky = float(self.lineEdit_KY.text())
            xm = float(self.lineEdit_XM.text())
            ym = float(self.lineEdit_YM.text())
        except:
            QtWidgets.QMessageBox.critical(self, "", "Коэффиценты масштабирования и координаты центра масштабирования "
                                                     "должны быть целыми или вещественными числами")
            return
        self.copy()
        for i in range(len(self.arr_walls)):
            self.arr_walls[i][0] = self.arr_walls[i][0] * kx + (1 - kx) * xm
            self.arr_walls[i][1] = self.arr_walls[i][1] * ky + (1 - ky) * ym
        for i in range(len(self.arr_l_wind)):
            self.arr_l_wind[i][0] = self.arr_l_wind[i][0] * kx + (1 - kx) * xm
            self.arr_l_wind[i][1] = self.arr_l_wind[i][1] * ky + (1 - ky) * ym
        for i in range(len(self.arr_r_wind)):
            self.arr_r_wind[i][0] = self.arr_r_wind[i][0] * kx + (1 - kx) * xm
            self.arr_r_wind[i][1] = self.arr_r_wind[i][1] * ky + (1 - ky) * ym
        for i in range(len(self.arr_hatch)):
            self.arr_hatch[i][0] = self.arr_hatch[i][0] * kx + (1 - kx) * xm
            self.arr_hatch[i][1] = self.arr_hatch[i][1] * ky + (1 - ky) * ym
        for i in range(len(self.arr_l_ell)):
            self.arr_l_ell[i][0] = self.arr_l_ell[i][0] * kx + (1 - kx) * xm
            self.arr_l_ell[i][1] = self.arr_l_ell[i][1] * ky + (1 - ky) * ym
        for i in range(len(self.arr_r_ell)):
            self.arr_r_ell[i][0] = self.arr_r_ell[i][0] * kx + (1 - kx) * xm
            self.arr_r_ell[i][1] = self.arr_r_ell[i][1] * ky + (1 - ky) * ym
        for i in range(len(self.arr_u_ell)):
            self.arr_u_ell[i][0] = self.arr_u_ell[i][0] * kx + (1 - kx) * xm
            self.arr_u_ell[i][1] = self.arr_u_ell[i][1] * ky + (1 - ky) * ym
        self.draw()

    # Обработчик события вращения фигуры.
    def rotate_func(self):
        try:
            deg = float(self.lineEdit_dg.text())
            xc = float(self.lineEdit_XC.text())
            yc = float(self.lineEdit_YC.text())
        except:
            QtWidgets.QMessageBox.critical(self, "", "Угол поворота и координаты центра поворота должны быть целыми "
                                                     "или вещественными числами.")
            return
        self.copy()
        SIN = sin(radians(deg))
        COS = cos(radians(deg))
        for i in range(len(self.arr_walls)):
            x1 = xc + (self.arr_walls[i][0] - xc) * COS + (self.arr_walls[i][1] - yc) * SIN
            self.arr_walls[i][1] = yc + (self.arr_walls[i][1] - yc) * COS - (self.arr_walls[i][0] - xc) * SIN
            self.arr_walls[i][0] = x1
        for i in range(len(self.arr_l_wind)):
            x1 = xc + (self.arr_l_wind[i][0] - xc) * COS + (self.arr_l_wind[i][1] - yc) * SIN
            self.arr_l_wind[i][1] = yc + (self.arr_l_wind[i][1] - yc) * COS - (self.arr_l_wind[i][0] - xc) * SIN
            self.arr_l_wind[i][0] = x1
        for i in range(len(self.arr_r_wind)):
            x1 = xc + (self.arr_r_wind[i][0] - xc) * COS + (self.arr_r_wind[i][1] - yc) * SIN
            self.arr_r_wind[i][1] = yc + (self.arr_r_wind[i][1] - yc) * COS - (self.arr_r_wind[i][0] - xc) * SIN
            self.arr_r_wind[i][0] = x1
        for i in range(len(self.arr_hatch)):
            x1 = xc + (self.arr_hatch[i][0] - xc) * COS + (self.arr_hatch[i][1] - yc) * SIN
            self.arr_hatch[i][1] = yc + (self.arr_hatch[i][1] - yc) * COS - (self.arr_hatch[i][0] - xc) * SIN
            self.arr_hatch[i][0] = x1
        for i in range(len(self.arr_l_ell)):
            x1 = xc + (self.arr_l_ell[i][0] - xc) * COS + (self.arr_l_ell[i][1] - yc) * SIN
            self.arr_l_ell[i][1] = yc + (self.arr_l_ell[i][1] - yc) * COS - (self.arr_l_ell[i][0] - xc) * SIN
            self.arr_l_ell[i][0] = x1
        for i in range(len(self.arr_r_ell)):
            x1 = xc + (self.arr_r_ell[i][0] - xc) * COS + (self.arr_r_ell[i][1] - yc) * SIN
            self.arr_r_ell[i][1] = yc + (self.arr_r_ell[i][1] - yc) * COS - (self.arr_r_ell[i][0] - xc) * SIN
            self.arr_r_ell[i][0] = x1
        for i in range(len(self.arr_u_ell)):
            x1 = xc + (self.arr_u_ell[i][0] - xc) * COS + (self.arr_u_ell[i][1] - yc) * SIN
            self.arr_u_ell[i][1] = yc + (self.arr_u_ell[i][1] - yc) * COS - (self.arr_u_ell[i][0] - xc) * SIN
            self.arr_u_ell[i][0] = x1
        self.draw()

# Точка входа.
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Visual()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
