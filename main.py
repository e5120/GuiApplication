# -*- coding: utf-8 -*-
"""
PCA Calculator
version: 1.0
Sailab Application
Created on Mon March 14 14:43:19 2016
"""
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import sys
import os
import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import calc

# global変数
f_name = []
material = []
calc = calc.Calc()


# タブ表示の親クラス
class TabMain(QtGui.QWidget):
    def __init__(self, parent=None):
        super(TabMain, self).__init__()
        self.count = 0
        self.createbutton()
        self.createform()
        self.createtable()
        self.addwidget()

    def createbutton(self):
        pass

    def createform(self):
        self.ledit = QtGui.QLineEdit("")
        self.ledit.resize(140, 20)
        self.ledit.setReadOnly(True)

    def createtable(self):
        pass

    def creategraph(self, item=1, width=0.2):
        self.x = np.arange(item)
        self.w = width
        self.figure, self.axes = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

    def addwidget(self):
        pass

    def autolabel(self, smps):
        for smp in smps:
            height = smp.get_height()
            self.axes.text(smp.get_x() + smp.get_width()/2., 1.05*height, '%d' % int(height),ha='center', va='bottom')

    def increment(self):
        global f_name
        self.count += 1
        if self.count >= len(f_name):
            self.count = 0
        self.pathdraw()

    def decrement(self):
        global f_name
        self.count -= 1
        if self.count < 0:
            self.count = len(f_name) - 1
        self.pathdraw()


# ファイル追加用タブ
class Tab1Widget(TabMain):
    def __init__(self, parent=None):
        super(Tab1Widget, self).__init__()

    def createbutton(self):
        self.referBtn = QtGui.QPushButton('Refer')
        self.referBtn.clicked.connect(self.open_filedialog)
        self.addBtn = QtGui.QPushButton("Add")
        self.addBtn.clicked.connect(self.add_file)

    def createform(self):
        self.ledit = QtGui.QLineEdit("")

    def createtable(self):
        self.table = QtGui.QTableWidget(0, 1)
        self.tableItem = QtGui.QTableWidgetItem()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

    def updatetable(self):
        global f_name
        self.table.setHorizontalHeaderLabels(["path"])
        self.table.setRowCount(len(f_name))
        for i in range(len(f_name)):
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(f_name[i]))

        if ("Not Found" in f_name) is True:
            f_name.remove("Not Found")

    def addwidget(self):
        grid = QtGui.QGridLayout()
        grid.addWidget(self.ledit, 1, 3)
        grid.addWidget(self.referBtn, 1, 4)
        grid.addWidget(self.addBtn, 2, 4)
        grid.addWidget(self.table, 4, 3)
        self.setLayout(grid)

    def open_filedialog(self):
        # filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', os.path.expanduser('~') + '/Desktop/')
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', './resources')
        self.ledit.setText(filename)

    def add_file(self):
        global f_name, material, calc
        if self.ledit.text() != "":
            if os.path.exists(self.ledit.text()) is True:
                material = calc.addFile(self.ledit.text())
                f_name.append(self.ledit.text())
            else:
                f_name.append("Not Found")
        self.updatetable()
        self.ledit.setText("")


# リスト表示用タブ
class Tab2Widget(TabMain):
    def __init__(self, parent=None):
        super(Tab2Widget, self).__init__()

    def createbutton(self):
        self.updataBtn = QtGui.QPushButton('Updata')
        self.updataBtn.clicked.connect(self.pathdraw)
        self.nextBtn = QtGui.QPushButton('Next')
        self.nextBtn.clicked.connect(self.increment)
        self.backBtn = QtGui.QPushButton("Back")
        self.backBtn.clicked.connect(self.decrement)
        self.saveBtn = QtGui.QPushButton("Save")
        # self.saveBtn.clicked.connect(self.add_File)

    def createtable(self):
        self.table = QtGui.QTableWidget(2, 5)
        self.tableItem = QtGui.QTableWidgetItem()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

    def pathdraw(self):
        global f_name
        if len(f_name) != 0:
            self.ledit.setText(f_name[self.count])
            self.tabledraw()

    def tabledraw(self):
        global material
        self.table.clear()
        self.table.setHorizontalHeaderLabels(["", "写真数", "判定数", "一致数", "一致率"])
        if len(material) > 0:
            for i in range(len(material[0])-1):
                for j in range(len(material[0][0])):
                    self.table.setItem(i, j, QtGui.QTableWidgetItem(str(material[self.count][i][j])))

    def addwidget(self):
        grid = QtGui.QGridLayout()
        grid.addWidget(self.updataBtn, 1, 2)
        grid.addWidget(self.nextBtn, 1, 3)
        grid.addWidget(self.backBtn, 1, 1)
        grid.addWidget(self.ledit, 2, 2)
        grid.addWidget(self.saveBtn, 3, 3)
        grid.addWidget(self.table, 3, 2)
        self.setLayout(grid)


# グラフ表示タブ１
class Tab3Widget(TabMain):
    def __init__(self, parent=None):
        self.creategraph(3, 0.4)
        super(Tab3Widget, self).__init__()

    def createbutton(self):
        self.updataBtn = QtGui.QPushButton('plot')
        self.updataBtn.clicked.connect(self.pathdraw)
        self.nextBtn = QtGui.QPushButton('Next')
        self.nextBtn.clicked.connect(self.increment)
        self.backBtn = QtGui.QPushButton("Back")
        self.backBtn.clicked.connect(self.decrement)
        self.saveBtn = QtGui.QPushButton("Save")
        self.saveBtn.clicked.connect(self.savegraph)

    def pathdraw(self):
        global f_name
        if len(f_name) != 0:
            self.ledit.setText(f_name[self.count])
            self.comparegraph()

    def addwidget(self):
        grid = QtGui.QGridLayout()
        grid.addWidget(self.updataBtn, 1, 2)
        grid.addWidget(self.nextBtn, 1, 3)
        grid.addWidget(self.backBtn, 1, 1)
        grid.addWidget(self.ledit, 2, 2)
        grid.addWidget(self.saveBtn, 3, 3)
        grid.addWidget(self.canvas, 3, 2)
        # grid.addWidget(self.toolbar, 4, 2)
        self.setLayout(grid)

    def comparegraph(self):
        global material
        if len(material):
            self.axes.clear()
            self.naminggraph()
            self.axes.grid()

            smp1 = self.axes.bar(self.x, material[self.count][0][1:4], color="r", width=self.w, label=material[self.count][0][0], align="center", alpha=0.44, picker=5)
            smp2 = self.axes.bar(self.x+self.w, material[self.count][1][1:4], color="b", width=self.w, label=material[self.count][1][0], align="center", alpha=0.44, picker=5)
            self.axes.legend(loc="best")
            self.autolabel(smp1)
            self.autolabel(smp2)
            self.canvas.draw()

    def naminggraph(self):
        self.axes.set_ylabel("Individual")
        self.axes.set_ylim([0, 2000])
        self.axes.set_title("Compare safe with danger")
        self.axes.set_xticks(self.x+self.w/2)
        self.axes.set_xticklabels(("image", "judge", "match"))

    def savegraph(self):
        global f_name
        if len(f_name):
            self.figure.savefig("results/result(compare)"+str(self.count+1)+".png")


# グラフ表示用タブ2
class Tab4Widget(TabMain):
    def __init__(self, parent=None):
        self.creategraph(1, 0.8)
        super(Tab4Widget, self).__init__()

    def createbutton(self):
        self.updataBtn = QtGui.QPushButton('plot')
        self.updataBtn.clicked.connect(self.pathdraw)
        self.nextBtn = QtGui.QPushButton('Next')
        self.nextBtn.clicked.connect(self.increment)
        self.backBtn = QtGui.QPushButton("Back")
        self.backBtn.clicked.connect(self.decrement)
        self.saveBtn = QtGui.QPushButton("Save")
        self.saveBtn.clicked.connect(self.savegraph)

    def pathdraw(self):
        global f_name
        if len(f_name) != 0:
            self.ledit.setText(f_name[self.count])
            self.comparegraph()

    def addwidget(self):
        grid = QtGui.QGridLayout()
        grid.addWidget(self.updataBtn, 1, 2)
        grid.addWidget(self.nextBtn, 1, 3)
        grid.addWidget(self.backBtn, 1, 1)
        grid.addWidget(self.ledit, 2, 2)
        grid.addWidget(self.saveBtn, 3, 3)
        grid.addWidget(self.canvas, 3, 2)
        # grid.addWidget(self.toolbar, 4, 2)
        self.setLayout(grid)

    def comparegraph(self):
        global material
        if len(material):
            self.axes.clear()
            self.naminggraph()
            self.axes.grid()

            smp1 = self.axes.bar(self.x, material[self.count][0][4], color="r", width=self.w, label=material[self.count][0][0], align="center", alpha=0.44, picker=5)
            smp2 = self.axes.bar(self.x+self.w, material[self.count][1][4], color="b", width=self.w, label=material[self.count][1][0], align="center", alpha=0.44, picker=5)
            self.axes.legend(loc="best")

            self.autolabel(smp1)
            self.autolabel(smp2)
            self.canvas.draw()

    def naminggraph(self):
        self.axes.set_ylabel("Percent")
        self.axes.set_ylim([0, 100])
        self.axes.set_title("Compare safe with danger(rate)")
        self.axes.set_xticks(self.x+self.w/2)
        self.axes.set_xticklabels(("match_rate"))

    def savegraph(self):
        global f_name
        if len(f_name):
            self.figure.savefig("results/result(rate)"+str(self.count+1)+".png")



# メインウインドウクラス
class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        qtab = QtGui.QTabWidget()
        qtab.addTab(Tab1Widget(parent=self), 'Input')
        qtab.addTab(Tab2Widget(parent=self), 'Table')
        qtab.addTab(Tab3Widget(parent=self), 'Graph1')
        qtab.addTab(Tab4Widget(parent=self), 'Graph2')

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(qtab)

        self.setLayout(hbox)

        self.setGeometry(300, 300, 720, 480)
        self.setWindowTitle('SaiLab')
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
