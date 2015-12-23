from PyQt4 import QtGui, QtCore
import os
import sys
import datetime
import ebaysdk
from ebaysdk.utils import getNodeText
from ebaysdk.exception import ConnectionError
from ebaysdk.trading import Connection as Trading
import AandJTrading as AJT

class ChooseCategory(QtGui.QWidget):
    def __init__(self,p):
        QtGui.QWidget.__init__(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setGeometry(200,200,1000,400)
        self.setWindowTitle("Choose a Category")
        self.createWidgets(p)

    def createWidgets(self,p):
        #Values
        self.ccDefault = "Current Category: eBay Motors > "
        self.ccValue = self.ccDefault

        #Buttons
        self.ChooseCat_button = QtGui.QPushButton("Choose Category",self)
        self.ChooseCat_button.clicked.connect(lambda x = p: self.Choose(p))
        self.Cancel_button = QtGui.QPushButton("Cancel",self)
        self.Cancel_button.clicked.connect(self.Cancel)
        
        #Labels
        self.CurrentCat_label = QtGui.QLabel(self.ccValue)

        #List Widgets
        self.LW01 = QtGui.QListWidget()
        self.LW02 = QtGui.QListWidget()
        self.LW03 = QtGui.QListWidget()
        self.LW04 = QtGui.QListWidget()
        self.LW05 = QtGui.QListWidget()
        self.LW01.currentItemChanged.connect(self.LW01_changed)
        self.LW02.currentItemChanged.connect(self.LW02_changed)
        self.LW03.currentItemChanged.connect(self.LW03_changed)
        self.LW04.currentItemChanged.connect(self.LW04_changed)
        self.LW05.currentItemChanged.connect(self.LW05_changed)
        self.LW01_list =  AJT.getCat(6000,100,2)
        for x in self.LW01_list:
            self.LW01.addItem(x[1])
        self.LW01.setCurrentRow(5)
        
        #Grid Layout
        Buttons_hlay = QtGui.QHBoxLayout()
        Buttons_hlay.insertStretch(0)
        Buttons_hlay.insertWidget(1,self.ChooseCat_button)
        Buttons_hlay.insertWidget(2,self.Cancel_button)
        Main_grid = QtGui.QGridLayout()
        Main_grid.setSpacing(10)
        Main_grid.addWidget(self.CurrentCat_label,0,0,1,5,QtCore.Qt.AlignLeft)
        Main_grid.addWidget(self.LW01,1,0)
        Main_grid.addWidget(self.LW02,1,1)
        Main_grid.addWidget(self.LW03,1,2)
        Main_grid.addWidget(self.LW04,1,3)
        Main_grid.addWidget(self.LW05,1,4)
        Main_grid.addLayout(Buttons_hlay,2,4)
        self.setLayout(Main_grid)

    def LW01_changed(self,new,old):
        self.ccValue = ""
        self.LW02.clear()
        self.LW02_list = []
        self.LW03.clear()
        self.LW03_list = []
        self.LW04.clear()
        self.LW04_list = []
        self.LW05.clear()
        self.LW05_list = []
        self.LW02_list =AJT.getCat(self.LW01_list[self.LW01.currentRow()][0],100,3)
        for x in self.LW02_list:
            self.LW02.addItem(x[1])
        self.ccValue = (self.ccDefault +
                        self.LW01.currentItem().text())
        if (self.LW02.count() != 0):
            self.ccValue = self.ccValue + " > "
            self.ChooseCat_button.setDisabled(True)
        else:
            self.ChooseCat_button.setDisabled(False)
        self.CurrentCat_label.setText(self.ccValue)

    def LW02_changed(self,new,old):
        self.ccValue = ""
        self.LW03.clear()
        self.LW03_list = []
        self.LW04.clear()
        self.LW04_list = []
        self.LW05.clear()
        self.LW05_list = []
        self.LW03_list = AJT.getCat(self.LW02_list[self.LW02.currentRow()][0],100,4)
        for x in self.LW03_list:
            self.LW03.addItem(x[1])
        self.ccValue = (self.ccDefault +
                        self.LW01.currentItem().text() + " > " +
                        self.LW02.currentItem().text())
        if (self.LW03.count() != 0):
            self.ccValue = self.ccValue + " > "
            self.ChooseCat_button.setDisabled(True)
        else:
            self.ChooseCat_button.setDisabled(False)
        self.CurrentCat_label.setText(self.ccValue)

    def LW03_changed(self,new,old):
        self.ccValue = ""
        self.LW04.clear()
        self.LW04_list = []
        self.LW05.clear()
        self.LW05_list = []
        self.LW04_list = AJT.getCat(self.LW03_list[self.LW03.currentRow()][0],100,5)
        for x in self.LW04_list:
            self.LW04.addItem(x[1])
        self.ccValue = (self.ccDefault +
                        self.LW01.currentItem().text() + " > " +
                        self.LW02.currentItem().text() + " > " +
                        self.LW03.currentItem().text())
        if (self.LW04.count() != 0):
            self.ccValue = self.ccValue + " > "
            self.ChooseCat_button.setDisabled(True)
        else:
            self.ChooseCat_button.setDisabled(False)
        self.CurrentCat_label.setText(self.ccValue)

    def LW04_changed(self,new,old):
        self.ccValue = ""
        self.LW05.clear()
        self.LW05_list = []
        self.LW05_list =  AJT.getCat(self.LW04_list[self.LW04.currentRow()][0],100,6)
        for x in self.LW05_list:
            self.LW05.addItem(x[1])
        self.ccValue = (self.ccDefault +
                        self.LW01.currentItem().text() + " > " +
                        self.LW02.currentItem().text() + " > " +
                        self.LW03.currentItem().text() + " > " +
                        self.LW04.currentItem().text())
        if (self.LW05.count() != 0):
            self.ccValue = self.ccValue + " > "
            self.ChooseCat_button.setDisabled(True)
        else:
            self.ChooseCat_button.setDisabled(False)
        self.CurrentCat_label.setText(self.ccValue)

    def LW05_changed(self,new,old):
        self.ccValue = ""
        self.ccValue = (self.ccDefault +
                        self.LW01.currentItem().text() + " > " +
                        self.LW02.currentItem().text() + " > " +
                        self.LW03.currentItem().text() + " > " +
                        self.LW04.currentItem().text() + " > " +
                        self.LW05.currentItem().text())
        self.CurrentCat_label.setText(self.ccValue)
        self.ChooseCat_button.setDisabled(False)

    def Choose(self,p):
        p.CategoryValue_label.setText(self.ccValue)
        if (self.ccValue.count('>') == 1):
            p.CategoryValue = self.LW01_list[self.LW01.currentRow()][0]
        elif (self.ccValue.count('>') == 2):
            p.CategoryValue = self.LW02_list[self.LW02.currentRow()][0]
        elif (self.ccValue.count('>') == 3):
            p.CategoryValue = self.LW03_list[self.LW03.currentRow()][0]
        elif (self.ccValue.count('>') == 4):
            p.CategoryValue = self.LW04_list[self.LW04.currentRow()][0]
        elif (self.ccValue.count('>') == 5):
            p.CategoryValue = self.LW05_list[self.LW05.currentRow()][0]
        else:
            print("ERROR: Category exceeded 5 subcategories!")
        self.close()

    def Cancel(self):
        self.close()
