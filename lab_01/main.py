import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from math import atan, degrees, pi
import design
import copy


class Visual(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.graphicsView.scale(1, -1)

        # Хранение данных.
        self.coord_arr_1 = []
        self.coord_arr_2 = []

        # Связи кнопок с функциями.
        self.pushButton_clear_xy.clicked.connect(self.clear_xy)
        self.pushButton_add_1.clicked.connect(self.add_point_1)
        self.pushButton_add_2.clicked.connect(self.add_point_2)
        self.pushButton_rem_all_points_1.clicked.connect(self.rem_all_points_1)
        self.pushButton_rem_all_points_2.clicked.connect(self.rem_all_points_2)
        self.pushButton_rem_point_1.clicked.connect(self.rem_point_1)
        self.pushButton_rem_point_2.clicked.connect(self.rem_point_2)
        self.pushButton_change_point.clicked.connect(self.change_point)
        self.pushButton_get_ans.clicked.connect(self.solve)

        # Сигналы.
        self.listWidget_1.itemSelectionChanged.connect(self.lW_1_upd_sel_stat)
        self.listWidget_2.itemSelectionChanged.connect(self.lW_2_upd_sel_stat)


    def clear_xy(self):
        self.lineEdit_x.clear()
        self.lineEdit_y.clear()
        self.lineEdit_x.setFocus()
        self.repaint()

    def is_point_in_arr(self, x, y, arr):
        for i in range(len(arr)):
            if (arr[i][0] == x and arr[i][1] == y):
                return True
        return False

    def check_xy(self):
        err = True
        try:
            x = float(self.lineEdit_x.text())
        except:
            QtWidgets.QMessageBox.critical(self, "", "Координата X введённой точки должна быть целым или вещественным числом.")
            err = False
        try:
            y = float(self.lineEdit_y.text())
        except:
            QtWidgets.QMessageBox.critical(self, "", "Координата Y введённой точки должна быть целым или вещественным числом.")
            err = False
        return err

    def lW_1_upd_sel_stat(self):
        if self.listWidget_1.currentRow() == -1:
            self.pushButton_rem_point_1.setDisabled(True)
        else:
            self.pushButton_rem_point_1.setEnabled(True)
            self.listWidget_2.setCurrentRow(-1)
        if self.listWidget_1.currentRow() == -1 and self.listWidget_2.currentRow() == -1:
            self.pushButton_change_point.setDisabled(True)
        elif self.listWidget_1.currentRow() != -1 or self.listWidget_2.currentRow() != -1:
            self.pushButton_change_point.setEnabled(True)
    def lW_2_upd_sel_stat(self):
        if self.listWidget_2.currentRow() == -1:
            self.pushButton_rem_point_2.setDisabled(True)
        else:
            self.pushButton_rem_point_2.setEnabled(True)
            self.listWidget_1.setCurrentRow(-1)
        if self.listWidget_1.currentRow() == -1 and self.listWidget_2.currentRow() == -1:
            self.pushButton_change_point.setDisabled(True)
        elif self.listWidget_1.currentRow() != -1 or self.listWidget_2.currentRow() != -1:
            self.pushButton_change_point.setEnabled(True)

    def btn_upd_status(self):
        if len(self.coord_arr_1) == 0:
            self.pushButton_rem_all_points_1.setDisabled(True)
        else:
            self.pushButton_rem_all_points_1.setEnabled(True)
        if len(self.coord_arr_2) == 0:
            self.pushButton_rem_all_points_2.setDisabled(True)
        else:
            self.pushButton_rem_all_points_2.setEnabled(True)
        self.pushButton_rem_all_points_1.repaint()
        self.pushButton_rem_all_points_2.repaint()

    def change_point(self):
        if not self.check_xy():
            return
        x = float(self.lineEdit_x.text())
        y = float(self.lineEdit_y.text())
        if self.listWidget_1.currentRow() != -1:
            ind = self.listWidget_1.currentRow()
            if self.is_point_in_arr(x, y, self.coord_arr_1) and self.coord_arr_1[ind] != [x, y]:
                QtWidgets.QMessageBox.critical(self, "", "Введённая точка присутствует в множестве №1.")
                return
            self.listWidget_1.setCurrentRow(-1)
            self.coord_arr_1[ind] = [x, y]
            self.fill_widget_1()
        elif self.listWidget_2.currentRow() != -1:
            ind = self.listWidget_2.currentRow()
            if self.is_point_in_arr(x, y, self.coord_arr_2) and self.coord_arr_2[ind] != [x, y]:
                QtWidgets.QMessageBox.critical(self, "", "Введённая точка присутствует в множестве №2.")
                return
            self.listWidget_2.setCurrentRow(-1)
            self.coord_arr_2[ind] = [x, y]
            self.fill_widget_2()

    def fill_widget_1(self):
        self.listWidget_1.clear()
        for i in range(len(self.coord_arr_1)):
            text = str(i + 1) + '. (' + str(self.coord_arr_1[i][0]) + ', ' + str(self.coord_arr_1[i][1]) + ')'
            self.listWidget_1.addItem(text)
        self.btn_upd_status()
    def fill_widget_2(self):
        self.listWidget_2.clear()
        for i in range(len(self.coord_arr_2)):
            text = str(i + 1) + '. (' + str(self.coord_arr_2[i][0]) + ', ' + str(self.coord_arr_2[i][1]) + ')'
            self.listWidget_2.addItem(text)
        self.btn_upd_status()

    def add_point_1(self):
        if self.check_xy() != True:
            return
        x = float(self.lineEdit_x.text())
        y = float(self.lineEdit_y.text())
        if self.is_point_in_arr(x, y, self.coord_arr_1) == True:
            QtWidgets.QMessageBox.critical(self, "", "Введённая точка уже присутствует в множестве №1. "
                                                     "Все точки одного множества должны быть различные.")
            return
        self.coord_arr_1.append([x, y])
        self.fill_widget_1()
    def add_point_2(self):
        if self.check_xy() != True:
            return
        x = float(self.lineEdit_x.text())
        y = float(self.lineEdit_y.text())
        if self.is_point_in_arr(x, y, self.coord_arr_2) == True:
            QtWidgets.QMessageBox.critical(self, "", "Введённая точка уже присутствует в множестве №2."
                                                     " Все точки одного множества должны быть различные.")
            return
        self.coord_arr_2.append([x, y])
        self.fill_widget_2()

    def rem_all_points_1(self):
        self.listWidget_1.setCurrentRow(-1)
        self.coord_arr_1.clear()
        self.listWidget_1.clear()
        self.btn_upd_status()
    def rem_all_points_2(self):
        self.listWidget_2.setCurrentRow(-1)
        self.coord_arr_2.clear()
        self.listWidget_2.clear()
        self.btn_upd_status()

    def rem_point_1(self):
        ind_to_rem = self.listWidget_1.currentRow()
        self.listWidget_1.setCurrentRow(-1)
        del(self.coord_arr_1[ind_to_rem])
        self.fill_widget_1()
    def rem_point_2(self):
        ind_to_rem = self.listWidget_2.currentRow()
        self.listWidget_2.setCurrentRow(-1)
        if ind_to_rem < 0:
            QtWidgets.QMessageBox.critical(self, "", "Для удаления точки необходимо её выделить.")
        del(self.coord_arr_2[ind_to_rem])
        self.fill_widget_2()

    def check_num_of_coords(self):
        err = True
        if len(self.coord_arr_1) < 3:
            QtWidgets.QMessageBox.critical(self, "", "В множестве №1 недостаточно точек для построения треугольника. Необходимо хотя бы 3 точки.")
            err = False
        if len(self.coord_arr_2) < 3:
            QtWidgets.QMessageBox.critical(self, "", "В множестве №2 недостаточно точек для построения треугольника. Необходимо хотя бы 3 точки.")
            err = False
        return err

    def is_able_to_build(self, arr):
        for i in range(len(arr) - 2):
            for j in range(i + 1, len(arr) - 1):
                for k in range(j + 1, len(arr)):
                    x1 = arr[i][0]; y1 = arr[i][1]
                    x2 = arr[j][0]; y2 = arr[j][1]
                    x3 = arr[k][0]; y3 = arr[k][1]
                    if (x3 - x1) * (y2 - y1) != (y3 - y1) * (x2 - x1):
                        return False
        return True

    def draw_result(self, tr1, tr2):
        #init
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(scene)
        h = self.graphicsView.height()
        w = self.graphicsView.width()
        scene.setSceneRect(0, 0, w-2, h-2)

        #Рисование треугольника №1
        pen = QtGui.QPen(QtCore.Qt.blue, 3)
        scene.addLine(tr1[0][0], tr1[0][1], tr1[1][0], tr1[1][1], pen)
        scene.addLine(tr1[1][0], tr1[1][1], tr1[2][0], tr1[2][1], pen)
        scene.addLine(tr1[0][0], tr1[0][1], tr1[2][0], tr1[2][1], pen)

        # Рисование биссектрис треугольника №1
        pen.setWidth(1)
        pen.setStyle(QtCore.Qt.DashLine)
        scene.addLine(tr1[0][0], tr1[0][1], tr1[5][0], tr1[5][1], pen)
        scene.addLine(tr1[1][0], tr1[1][1], tr1[6][0], tr1[6][1], pen)
        scene.addLine(tr1[2][0], tr1[2][1], tr1[7][0], tr1[7][1], pen)

        # Рисование треугольника №2
        pen.setColor(QtCore.Qt.magenta)
        pen.setStyle(QtCore.Qt.SolidLine)
        pen.setWidth(3)
        scene.addLine(tr2[0][0], tr2[0][1], tr2[1][0], tr2[1][1], pen)
        scene.addLine(tr2[1][0], tr2[1][1], tr2[2][0], tr2[2][1], pen)
        scene.addLine(tr2[0][0], tr2[0][1], tr2[2][0], tr2[2][1], pen)

        # Рисование биссектрис треугольника №1
        pen.setWidth(1)
        pen.setStyle(QtCore.Qt.DashLine)
        scene.addLine(tr2[0][0], tr2[0][1], tr2[5][0], tr2[5][1], pen)
        scene.addLine(tr2[1][0], tr2[1][1], tr2[6][0], tr2[6][1], pen)
        scene.addLine(tr2[2][0], tr2[2][1], tr2[7][0], tr2[7][1], pen)

        # Рисование прямой соединяющей точки пересечения биссектрис
        pen.setColor(QtCore.Qt.green)
        pen.setWidth(4)
        pen.setStyle(QtCore.Qt.SolidLine)
        scene.addLine(tr1[3][0], tr1[3][1], tr2[3][0], tr2[3][1], pen)
        scene.addLine(tr1[3][0], tr1[3][1], tr1[4][0], tr1[4][1], pen)

        # Рисование точек пересечения биссектрис
        pen.setColor(QtCore.Qt.magenta)
        pen.setWidth(3)
        scene.addEllipse(tr2[3][0] - 2, tr2[3][1] - 2, 4, 4, pen)
        pen.setColor(QtCore.Qt.blue)
        scene.addEllipse(tr1[3][0] - 2, tr1[3][1] - 2, 4, 4, pen)

        # Рисование оси абсцисс
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(1)
        scene.addLine(-1, tr1[4][1], scene.width() + 1, tr1[4][1], pen)
        scene.addEllipse(tr1[4][0] - 2, tr1[4][1] - 2, 4, 4, pen)

        self.repaint()

    def count_one_side(self, x1, y1, x2, y2):
        return float(pow(pow(x2 - x1, 2) + pow(y2 - y1, 2), 0.5))

    def count_per_point(self, x1, y1, x2, y2, x11, y11, x22, y22):
        A1 = y1 - y2
        B1 = x2 - x1
        C1 = (x1 - x2) * y1 + (y2 - y1) * x1
        A2 = y11 - y22
        B2 = x22 - x11
        C2 = (x11 - x22) * y11 + (y22 - y11) * x11
        Xp = (B1 * C2 - B2 * C1) / (A1 * B2 - A2 * B1)
        Yp = (C1 * A2 - C2 * A1) / (A1 * B2 - A2 * B1)
        return [Xp, Yp]

    def count_data(self, arr):
        triag_ind = []
        centers = []
        for i in range(len(arr) - 2):
            for j in range(i + 1, len(arr) - 1):
                for k in range(j + 1, len(arr)):
                    x1 = arr[i][0]; y1 = arr[i][1]
                    x2 = arr[j][0]; y2 = arr[j][1]
                    x3 = arr[k][0]; y3 = arr[k][1]
                    if (x3 - x1) * (y2 - y1) == (y3 - y1) * (x2 - x1):
                        continue
                    triag_ind.append([i, j, k])
                    a = self.count_one_side(x2, y2, x3, y3)
                    b = self.count_one_side(x1, y1, x3, y3)
                    c = self.count_one_side(x1, y1, x2, y2)
                    x_c = float((x1 * a + x2 * b + x3 * c) / (a + b + c))
                    y_c = float((y1 * a + y2 * b + y3 * c) / (a + b + c))
                    centers.append([x_c, y_c])
        return triag_ind, centers

    def scale_points(self, tr1, tr2):
        Xmin = min(min(tr1, key = lambda i: i[0])[0], min(tr2, key = lambda i: i[0])[0])
        Xmax = max(max(tr1, key = lambda i: i[0])[0], max(tr2, key = lambda i: i[0])[0])
        Ymin = min(min(tr1, key = lambda i: i[1])[1], min(tr2, key = lambda i: i[1])[1])
        Ymax = max(max(tr1, key = lambda i: i[1])[1], max(tr2, key = lambda i: i[1])[1])

        KXmin = 0
        KXmax = self.graphicsView.width() - 40
        KYmin = self.graphicsView.height() - 40
        KYmax = 0

        KX = (KXmax - KXmin) / (Xmax - Xmin)
        KY = (KYmax - KYmin) / (Ymax - Ymin)
        K = min(abs(KX), abs(KY))
        KY *= -1

        for i in range(len(tr1)):
            tr1[i][0] = 20 + (tr1[i][0] - Xmin) * K * KX / abs(KX)
            tr1[i][1] = 20 + (Ymax - tr1[i][1]) * K * KY / abs(KY)
            tr2[i][0] = 20 + (tr2[i][0] - Xmin) * K * KX / abs(KX)
            tr2[i][1] = 20 + (Ymax - tr2[i][1]) * K * KY / abs(KY)

    def choose_triangles(self):
        arr_1 = copy.deepcopy(self.coord_arr_1)
        arr_2 = copy.deepcopy(self.coord_arr_2)
        triag_ind_1, centers_1 = self.count_data(arr_1)
        triag_ind_2, centers_2 = self.count_data(arr_2)
        angle = []
        for i in range(len(triag_ind_1)):
            for j in range(len(triag_ind_2)):
                A1 = centers_1[i][1] - centers_2[j][1]
                B1 = centers_2[j][0] - centers_1[i][0]
                if B1 == 0:
                    f = degrees(pi / 2)
                else:
                    f = degrees(atan(-A1/B1))
                angle.append([i, j, abs(f)])
        angle = min(angle, key = lambda i : i[2])
        triangle_1 = []; triangle_2 = []
        for i in range(3):
            triangle_1.append(arr_1[triag_ind_1[angle[0]][i]])
            triangle_2.append(arr_2[triag_ind_2[angle[1]][i]])
        triangle_1.append(centers_1[angle[0]])
        triangle_2.append(centers_2[angle[1]])
        triangle_1.append(self.count_per_point(centers_1[angle[0]][0], centers_1[angle[0]][1],
                                               centers_2[angle[1]][0], centers_2[angle[1]][1], 0, 0, 10, 0))
        triangle_2.append([0, 0])
        for i in range(3):
            triangle_1.append(
                self.count_per_point(arr_1[triag_ind_1[angle[0]][i]][0], arr_1[triag_ind_1[angle[0]][i]][1],
                                     centers_1[angle[0]][0], centers_1[angle[0]][1],
                                     arr_1[triag_ind_1[angle[0]][(i + 1) % 3]][0],
                                     arr_1[triag_ind_1[angle[0]][(i + 1) % 3]][1],
                                     arr_1[triag_ind_1[angle[0]][(i + 2) % 3]][0],
                                     arr_1[triag_ind_1[angle[0]][(i + 2) % 3]][1]))
            triangle_2.append(
                self.count_per_point(arr_2[triag_ind_2[angle[1]][i]][0], arr_2[triag_ind_2[angle[1]][i]][1],
                                     centers_2[angle[1]][0], centers_2[angle[1]][1],
                                     arr_2[triag_ind_2[angle[1]][(i + 1) % 3]][0],
                                     arr_2[triag_ind_2[angle[1]][(i + 1) % 3]][1],
                                     arr_2[triag_ind_2[angle[1]][(i + 2) % 3]][0],
                                     arr_2[triag_ind_2[angle[1]][(i + 2) % 3]][1]))
        self.scale_points(triangle_1, triangle_2)

        # Вывод ответа в текстовое поле
        text1 = "Треугольник №1 построен из точек с индексами: " + str(triag_ind_1[angle[0]][0] + 1) + ' ' + str(
            triag_ind_1[angle[0]][1] + 1) + ' ' + str(triag_ind_1[angle[0]][2] + 1) + '.'
        text2 = "Треугольник №2 построен из точек с индексами: " + str(triag_ind_2[angle[1]][0] + 1) + ' ' + str(
            triag_ind_2[angle[1]][1] + 1) + ' ' + str(triag_ind_2[angle[1]][2] + 1) + '.'
        text3 = "Полученный угол между прямой и осью абсцисс: " + str("%.2f" % angle[2]) + ' градусов.'
        self.listWidget_ans.clear()
        self.listWidget_ans.addItem(text1)
        self.listWidget_ans.addItem(text2)
        self.listWidget_ans.addItem(text3)
        self.listWidget_ans.repaint()

        self.draw_result(triangle_1, triangle_2)

    def solve(self):
        if not self.check_num_of_coords():
            return
        err = False
        if self.is_able_to_build(self.coord_arr_1):
            QtWidgets.QMessageBox.critical(self, "", "Невозможно построить ни одного треугольника из точек множества №1."
                                                     " Все точки множества №1 лежат на одной прямой.")
            err = True
        if self.is_able_to_build(self.coord_arr_2):
            QtWidgets.QMessageBox.critical(self, "", "Невозможно построить ни одного треугольника из точек множества №2."
                                                     " Все точки множества №2 лежат на одной прямой.")
            err = True
        if err:
            return
        self.choose_triangles()




def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Visual()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
