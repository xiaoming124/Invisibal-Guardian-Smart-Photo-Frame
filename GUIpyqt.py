# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     GUIpyqt
   Description :
   Author :       Kinddle
   date：          2020/9/27
-------------------------------------------------
   Change Activity:
                   2020/9/27:
-------------------------------------------------
"""
__author__ = 'Kinddle'

# coding:utf-8

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import qtawesome
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import re
import numpy as np
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt

class MainUi(QtWidgets.QMainWindow):
    left = 100
    top = 100
    width = 960
    height = 700
    output_breath=[0 for i in range(0, 100) ]
    output_heart=[0 for j in range(0, 100) ]
    # item=[]
    textforfall=['跌倒检测：\n', '', '', '']
    def __init__(self, datalink):
        super().__init__()
        self.datadic = datalink
        self.title = 'Contoller'

        self.init_ui()
        self.refresh(True, True, True)
        self.refresh(True, True, True)

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格
        self.left_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        # self.left_widget.(0, 100, 300, self.height)

        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格
        self.right_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        self.control_widget = QtWidgets.QWidget() #创建控制部件
        self.control_layout = QtWidgets.QGridLayout()
        self.control_widget.setLayout(self.control_layout)  # 设置控制部件布局为网格
        self.control_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main_layout.addWidget(self.left_widget, 0, 0, 13, 2)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 6)  # 右侧部件在第0行第3列，占8行9列

        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(1, 6)
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.lb1 = QtWidgets.QLabel("呼吸速率:0")
        self.lb2 = QtWidgets.QLabel("心跳速率:0")
        self.lb3 = QtWidgets.QLabel("跌倒检测：")
        self.lb4 = QtWidgets.QLabel('呼吸心跳雷达：')
        self.lb5 = QtWidgets.QLabel('航迹跌倒雷达：')
        self.lb6 = QtWidgets.QLabel('目标检测与跟踪')
        self.txt = QtWidgets.QLabel('')
        self.txt.setFixedWidth(int(self.width*1/3))
        self.txt.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.white)
        self.txt.setPalette(palette)
        # self.txt.setMaximumBlockCount(10)

        plot_Rate_breath = pg.PlotWidget()
        plot_Rate_heart = pg.PlotWidget()
        plot_Track, Trackdata = self._init_track()

        btn1 = QtWidgets.QPushButton("R up")
        btn1.clicked.connect(lambda : print(1))
        btn2 = QtWidgets.QPushButton('R down')
        btn2.clicked.connect(lambda : print(1))
        btn3 = QtWidgets.QPushButton('FT up')
        btn3.clicked.connect(lambda : print(1))
        btn4 = QtWidgets.QPushButton('FT down')
        btn4.clicked.connect(lambda : print(1))


        #布局
        self.left_layout.addWidget(self.lb1, 0, 0, 1, 2)
        self.left_layout.addWidget(plot_Rate_breath, 1, 0, 3, 2)
        self.left_layout.addWidget(self.lb2, 4, 0, 1, 2)
        self.left_layout.addWidget(plot_Rate_heart, 5, 0, 3, 2)
        self.left_layout.addWidget(self.lb3, 8, 0 ,1, 2)
        self.left_layout.addWidget(self.txt, 9, 0, 4, 2)
        self.left_layout.setRowStretch(0, 1)
        self.left_layout.setRowStretch(1, 4)
        self.left_layout.setRowStretch(4, 1)
        self.left_layout.setRowStretch(5, 4)
        self.left_layout.setRowStretch(8, 1)
        self.left_layout.setRowStretch(9, 4)

        self.right_layout.addWidget(self.lb6, 0, 0, 1, 6)
        self.right_layout.addWidget(plot_Track, 1, 0, 10, 6)
        self.right_layout.addWidget(self.control_widget, 11, 0, 1, 6)
        self.right_layout.setRowStretch(1, 0)
        self.right_layout.setRowStretch(2, 5)
        self.right_layout.setRowStretch(11,0)

        self.control_layout.addWidget(self.lb4,0,0,1,2)
        self.control_layout.addWidget(self.lb5,0,2,1,2)
        self.control_layout.addWidget(btn1, 1, 0)
        self.control_layout.addWidget(btn2, 1, 1)
        self.control_layout.addWidget(btn3, 1, 2)
        self.control_layout.addWidget(btn4, 1, 3)
        self.right_layout.setRowStretch(0, 1)
        self.right_layout.setRowStretch(1, 1)

        # self.plot_Rate_breath = self.pw.plot()
        # plot_Rate_heart.setYRange(max=1, min=0)
        # plot_Rate_breath.setYRange(max=1, min=0)
        # self.plot_Track = plot_Track.plot([0])
        self.plot_Rate_breath = plot_Rate_breath.plot()
        self.plot_Rate_heart = plot_Rate_heart.plot()

        self.plot_Track = plot_Track
        self.plot_Track_data = Trackdata
        self.plot_Track_count = 0

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        #缩放窗口事件！
        new_width = max(int(a0.size().width() * 2/3), 300)
        self.plot_Track.setFixedWidth(new_width)

        self.txt.setFixedWidth(int(self.width*1/3))

    def _init_track(self):
        w = gl.GLViewWidget()
        w.opts['distance'] = 40
        # w.resize(600,600)
        w.setFixedWidth(int(self.width * 2/3))
        w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #坐标系
        # gx = gl.GLGridItem()
        # gx.rotate(90, 0, 1, 0)
        # gx.translate(-0, 0, 0)
        # w.addItem(gx)
        # gy = gl.GLGridItem()
        # gy.rotate(90, 1, 0, 0)
        # gy.translate(0, -0, 0)
        # w.addItem(gy)
        # gz = gl.GLGridItem()
        # gz.translate(0, 0, -0)
        # w.addItem(gz)

        ggx = gl.GLLinePlotItem(pos=np.array([[-1, 0, 0], [1., 0, 0]]), color = (1., 1., 1., 1.), width = 2)
        ggy = gl.GLLinePlotItem(pos=np.array([[0, -1, 0], [0, 1, 0]]), color = (1., 1., 1., 1.), width = 2)
        ggz = gl.GLLinePlotItem(pos=np.array([[0, 0, -1], [0, 0, 1]]), color = (1., 1., 1., 1.), width = 2)

        w.addItem(ggx)
        w.addItem(ggy)
        w.addItem(ggz)

        plt = [gl.GLLinePlotItem(color = pg.glColor(235, (5+ i*49)%255, 66, 200), width = 4) for i in range(100)]
        for i in plt:
            w.addItem(i)

        return w, plt

    def draw_track(self, data):
        # for j in self.item:
            # self.plot_Track.removeItem(j)
        tracknum = len(data)
        if tracknum < self.plot_Track_count:
            for i in range(tracknum, self.plot_Track_count):
                self.plot_Track_data[i].setData(pos=None)
        self.plot_Track_count = tracknum
        for i in range(tracknum):
            pts = np.vstack(data[i])
            pts = pts
            self.plot_Track_data[i].setData(pos=pts)

            # plt = gl.GLLinePlotItem(pos=pts, color=pg.glColor((1, 9 * 1.3)), width=(30) / 10., antialias=True)
            # self.item.append(plt)
            # self.plot_Track.addItem(plt)

    def refresh(self, T=False, R=False, F=False):
        if T:
            self.draw_track(self.datadic['T'])
        if R:
            self.lb1.setText('呼吸率：%d' % self.datadic['R'][2])
            self.lb2.setText('心率:%d' % self.datadic['R'][3])

            self.output_breath=self.output_breath[1:]
            self.output_breath.append(self.datadic['R'][0])
            self.plot_Rate_breath.setData(self.output_breath,
                                          pen='r', symbol=None, symbolBrush='g')

            self.output_heart=self.output_heart[1:]
            self.output_heart.append(self.datadic['R'][1])
            self.plot_Rate_heart.setData(self.output_heart,
                                         pen='r', symbol=None, symbolBrush='g')
            # self.plot_Rate_breath = self.pw.plot()
            # self.Rate_breath.set('呼吸率：%d' % self.datadic['R'][2])
            # self.Rate_heart.set('心率:%d' % self.datadic['R'][3])
        if F:
            stat = self.datadic['F'][0]
            weight = self.datadic['F'][1]
            # weight = self.txt.blockCount()
            txt_insert = ('平静' if stat==0 else '慢蹲或坐下' if stat == 1 else '跌倒！！' if stat == 2 else "未知数据")\
                        + ' 跌倒概率：' + str(1-weight)
            # now_txt = self.txt.toPlainText()
            # sp_txt = re.split('\n', now_txt)
            # for i in range(0, min(len(sp_txt), 5)):
            #     txt_insert += '\n'+sp_txt[i]
            # if self.txt.blockCount() > 20:
            #
            #     self.txt.clear()
            self.textforfall[1]=self.textforfall[2]
            self.textforfall[2]=self.textforfall[3]
            self.textforfall[3]=txt_insert + '\n'
            txtnow=''.join(self.textforfall)
            self.txt.setText(txtnow)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    datainit = {"T": [[[0, 0, 0], [1, 1.24, 1], [1, 2, 1]], [[3, 3, 3], [3, 3, 2], [3, 2, 1], [3, 3, 3]]],
                'R': [0.45, 0.68, 60, 120],
                'F': [0,0]}
    gui = MainUi(datainit)
    gui.show()
    print('end')
    sys.exit(app.exec_())