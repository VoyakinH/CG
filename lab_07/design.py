# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/Alex/Documents/КГ/lab_07/design.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(814, 482)
        MainWindow.setMinimumSize(QtCore.QSize(814, 482))
        MainWindow.setMaximumSize(QtCore.QSize(814, 482))
        MainWindow.setMouseTracking(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelWorkSpace = QtWidgets.QLabel(self.centralwidget)
        self.labelWorkSpace.setGeometry(QtCore.QRect(260, 13, 145, 16))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.labelWorkSpace.setFont(font)
        self.labelWorkSpace.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.labelWorkSpace.setFrameShadow(QtWidgets.QFrame.Plain)
        self.labelWorkSpace.setScaledContents(False)
        self.labelWorkSpace.setObjectName("labelWorkSpace")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(262, 35, 541, 436))
        self.label.setMouseTracking(True)
        self.label.setAutoFillBackground(True)
        self.label.setText("")
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(13, 13, 246, 426))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Manage = QtWidgets.QGroupBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Manage.sizePolicy().hasHeightForWidth())
        self.Manage.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Manage.setFont(font)
        self.Manage.setObjectName("Manage")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.Manage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.labelCutter = QtWidgets.QLabel(self.Manage)
        self.labelCutter.setObjectName("labelCutter")
        self.horizontalLayout_6.addWidget(self.labelCutter)
        self.frame = QtWidgets.QFrame(self.Manage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelColourCutter = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelColourCutter.sizePolicy().hasHeightForWidth())
        self.labelColourCutter.setSizePolicy(sizePolicy)
        self.labelColourCutter.setAutoFillBackground(True)
        self.labelColourCutter.setText("")
        self.labelColourCutter.setObjectName("labelColourCutter")
        self.horizontalLayout_3.addWidget(self.labelColourCutter)
        self.horizontalLayout_6.addWidget(self.frame)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.labelLineOut = QtWidgets.QLabel(self.Manage)
        self.labelLineOut.setObjectName("labelLineOut")
        self.horizontalLayout_7.addWidget(self.labelLineOut)
        self.frame_2 = QtWidgets.QFrame(self.Manage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.labelColourLineOut = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelColourLineOut.sizePolicy().hasHeightForWidth())
        self.labelColourLineOut.setSizePolicy(sizePolicy)
        self.labelColourLineOut.setAutoFillBackground(True)
        self.labelColourLineOut.setText("")
        self.labelColourLineOut.setObjectName("labelColourLineOut")
        self.horizontalLayout_4.addWidget(self.labelColourLineOut)
        self.horizontalLayout_7.addWidget(self.frame_2)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.labelLineIn = QtWidgets.QLabel(self.Manage)
        self.labelLineIn.setObjectName("labelLineIn")
        self.horizontalLayout_8.addWidget(self.labelLineIn)
        self.frame_3 = QtWidgets.QFrame(self.Manage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.labelColourLineIn = QtWidgets.QLabel(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelColourLineIn.sizePolicy().hasHeightForWidth())
        self.labelColourLineIn.setSizePolicy(sizePolicy)
        self.labelColourLineIn.setAutoFillBackground(True)
        self.labelColourLineIn.setText("")
        self.labelColourLineIn.setObjectName("labelColourLineIn")
        self.horizontalLayout_5.addWidget(self.labelColourLineIn)
        self.horizontalLayout_8.addWidget(self.frame_3)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.pushButtonProc = QtWidgets.QPushButton(self.Manage)
        self.pushButtonProc.setMaximumSize(QtCore.QSize(16777215, 30))
        self.pushButtonProc.setObjectName("pushButtonProc")
        self.verticalLayout.addWidget(self.pushButtonProc)
        self.pushButtonScreenClean = QtWidgets.QPushButton(self.Manage)
        self.pushButtonScreenClean.setMaximumSize(QtCore.QSize(16777215, 30))
        self.pushButtonScreenClean.setObjectName("pushButtonScreenClean")
        self.verticalLayout.addWidget(self.pushButtonScreenClean)
        self.verticalLayout_3.addWidget(self.Manage)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Лабораторная работа №7"))
        self.labelWorkSpace.setText(_translate("MainWindow", "Рабочее пространство"))
        self.Manage.setTitle(_translate("MainWindow", "Управление"))
        self.labelCutter.setText(_translate("MainWindow", "Отсекатель:"))
        self.labelLineOut.setText(_translate("MainWindow", "Отсекаемое:"))
        self.labelLineIn.setText(_translate("MainWindow", "Отсечённое:"))
        self.pushButtonProc.setText(_translate("MainWindow", "Выполнить"))
        self.pushButtonScreenClean.setText(_translate("MainWindow", "Очистить экран"))
