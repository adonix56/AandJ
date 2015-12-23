from PyQt4 import QtGui, QtCore
import os
import sys
import datetime
import Category as cc
import AandJTrading as AJT

files=[]

class NewListing(QtGui.QWidget):
    def __init__(self,p):
        QtGui.QWidget.__init__(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setGeometry(100,100,720,700)
        self.setWindowTitle("New Listing")
        self.setWindowIcon(QtGui.QIcon('icons/plus.png'))
        self.createWidgets(p)

    def createWidgets(self,p):
        #Values
        self.CategoryValue = 0
        #List Widgets
        self.Picture_lw = QtGui.QListWidget()
        self.Picture_lw.setIconSize(QtCore.QSize(100,100))
        self.Picture_lw.setViewMode(QtGui.QListView.IconMode)
        self.Picture_lw.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        """TODO: Get directories from config file"""
        for file in os.listdir("D:\\Projects\\AandJ\\Pictures"):
            if file.endswith(".JPG"):
                #files.append(os.path.join(os.getcwd(),file))
                files.append(os.path.join("D:\\Projects\\AandJ\\Pictures",file))
        files.sort(key=lambda x: os.path.getmtime(x))

        for x in files:
            item = QtGui.QListWidgetItem()
            item.setIcon(QtGui.QIcon(x))
            item.setText(x[27:])
            self.Picture_lw.addItem(item)


        #Group Boxs
        Title_groupbox = QtGui.QGroupBox('Title')
        Req_groupbox = QtGui.QGroupBox('eBay Required Fields')
        AandJ_groupbox = QtGui.QGroupBox('AandJ Convenience Fields')
        Ship_groupbox = QtGui.QGroupBox('Shipping')
        
        #Labels
        '''Title'''
        self.PartNumber_label = QtGui.QLabel('*Part Number/UPC:')
        self.Model_label = QtGui.QLabel('*Model:')
        self.Description_label = QtGui.QLabel('*Description:')
        '''eBay req'''
        self.Price_label = QtGui.QLabel('*Price:')
        self.Quantity_label = QtGui.QLabel('*Quantity:')
        self.Category_label = QtGui.QLabel('*Category:')# eBay Motors>Parts & Accessories>')
        self.CategoryValue_label = QtGui.QLabel('None Selected...')
        self.Condition_label = QtGui.QLabel('*Condition:')
        self.CondDetail_label = QtGui.QLabel('Condition Details:')
        self.Picture_label = QtGui.QLabel('*Add Picture:\n(Minimum 1 required)')
        self.Dimension_label = QtGui.QLabel('*Dimensions(LxWxH):')
        self.DimenInX_label = QtGui.QLabel('in. X ')
        self.DimenInX2_label = QtGui.QLabel('in. X ')
        self.DimenIn_label = QtGui.QLabel('in.')
        self.Weight_label = QtGui.QLabel('*Custom Weight:')
        self.WeightLbs_label = QtGui.QLabel('lbs.')
        self.WeightOz_label = QtGui.QLabel('oz.')
        self.Ship_label = QtGui.QLabel('Please Choose at least 1:')
        '''AandJ'''
        self.ItemID_label = QtGui.QLabel('Item ID Number:')
        self.Location_label = QtGui.QLabel('Location:')
        '''main'''
        self.Req_label = QtGui.QLabel('* - Required Fields')

        #SpinBox
        self.Price_sbox = QtGui.QDoubleSpinBox()
        self.Price_sbox.setRange(0.00,99999.99)
        self.Price_sbox.setPrefix('$')
        self.Quantity_sbox = QtGui.QSpinBox()
        self.Quantity_sbox.setRange(0,9999)
        self.DimensionL_sbox = QtGui.QSpinBox()
        self.DimensionL_sbox.setRange(0,999)
        self.DimensionW_sbox = QtGui.QSpinBox()
        self.DimensionW_sbox.setRange(0,999)
        self.DimensionH_sbox = QtGui.QSpinBox()
        self.DimensionH_sbox.setRange(0,999)
        self.WeightLbs_sbox = QtGui.QSpinBox()
        self.WeightLbs_sbox.setRange(0,999)
        self.WeightOz_sbox = QtGui.QSpinBox()
        self.WeightOz_sbox.setRange(0,999)

        #TextBox
        '''Title'''
        self.PartNumber_ledit = QtGui.QLineEdit()
        self.Model_ledit = QtGui.QLineEdit()
        self.Description_ledit = QtGui.QLineEdit()
        '''eBay req'''
        self.CondDetail_tedit = QtGui.QTextEdit()
        '''AandJ'''
        self.ItemID_ledit = QtGui.QLineEdit()
        self.Location_ledit = QtGui.QLineEdit()
        
        #Button
        self.Cancel_button = QtGui.QPushButton("Cancel", self)
        self.Cancel_button.clicked.connect(self.Cancel)
        self.AddList_button = QtGui.QPushButton("Add Listing", self)
        self.AddList_button.clicked.connect(lambda:self.AddListing(p))
        self.Category_button = QtGui.QPushButton("Choose New Category",self)
        self.Category_button.clicked.connect(self.ChooseCat)

        #ComboBox
        self.Condition_cbox = QtGui.QComboBox()
        self.Condition_cbox.addItem('-')
        self.Condition_cbox.addItem('New')
        self.Condition_cbox.addItem('New other (see Details)')
        self.Condition_cbox.addItem('Manufacturer refurbished')
        self.Condition_cbox.addItem('Seller refurbished')
        self.Condition_cbox.addItem('Used')
        self.Condition_cbox.addItem('For parts or not working')

        #Checkbox
        self.Ship1_chbox = QtGui.QCheckBox('USPS Priority (1-4 days)')
        self.Ship2_chbox = QtGui.QCheckBox('UPS Ground (1-6 days)')
        self.Ship3_chbox = QtGui.QCheckBox('USPS Priority Large Flat Rate(1-4 days)')
        self.IntShip1_chbox = QtGui.QCheckBox('USPS Priority International')
        self.IntShip2_chbox = QtGui.QCheckBox('USPS Priority International Large Flat Rate')
        self.FShip_chbox = QtGui.QCheckBox('Free Shipping')
        self.BestOffer_chbox = QtGui.QCheckBox('Add Best Offer')

        #Grid Layout
        Main_grid = QtGui.QGridLayout()
        Main_grid.setSpacing(10)
        Buttons_hlay = QtGui.QHBoxLayout()
        Title_grid = QtGui.QGridLayout()
        Title_grid.setSpacing(10)
        Req_grid = QtGui.QGridLayout()
        Req_grid.setSpacing(10)
        AandJ_grid = QtGui.QGridLayout()
        AandJ_grid.setSpacing(10)
        Ship_grid = QtGui.QGridLayout()
        Ship_grid.setSpacing(10)

        Ship_grid.addWidget(self.Ship_label,1,0)
        Ship_grid.addWidget(self.Ship1_chbox,2,0,1,2)
        Ship_grid.addWidget(self.Ship2_chbox,3,0,1,2)
        Ship_grid.addWidget(self.Ship3_chbox,4,0,1,2)
        Ship_grid.addWidget(self.IntShip1_chbox,2,2,1,2)
        Ship_grid.addWidget(self.IntShip2_chbox,3,2,1,2)
        Ship_grid.addWidget(self.FShip_chbox,1,1)
        Ship_groupbox.setLayout(Ship_grid)
        
        Title_grid.addWidget(self.PartNumber_label,1,0,QtCore.Qt.AlignRight)
        Title_grid.addWidget(self.PartNumber_ledit,1,1,1,5)
        Title_grid.addWidget(self.Model_label,2,0,QtCore.Qt.AlignRight)
        Title_grid.addWidget(self.Model_ledit,2,1,1,5)
        Title_grid.addWidget(self.Description_label,3,0,QtCore.Qt.AlignRight)
        Title_grid.addWidget(self.Description_ledit,3,1,1,5)
        Title_groupbox.setLayout(Title_grid)

        Req_grid.addWidget(self.Price_label,1,0,QtCore.Qt.AlignRight)
        Req_grid.addWidget(self.Price_sbox,1,1,1,2)
        Req_grid.addWidget(self.Quantity_label,1,3,QtCore.Qt.AlignRight)
        Req_grid.addWidget(self.Quantity_sbox,1,4)
        Req_grid.addWidget(self.BestOffer_chbox,1,5)
        Req_grid.addWidget(self.Category_label,2,0,2,1,QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        Req_grid.addWidget(self.CategoryValue_label,2,1,1,5)
        Req_grid.addWidget(self.Category_button,3,1,1,2)
        Req_grid.addWidget(self.Condition_label,4,0,QtCore.Qt.AlignRight)
        Req_grid.addWidget(self.Condition_cbox,4,1,1,2)
        Req_grid.addWidget(self.CondDetail_label,5,0,QtCore.Qt.AlignRight)
        Req_grid.addWidget(self.CondDetail_tedit,5,1,5,7)
        Req_grid.addWidget(self.Picture_label,10,0,QtCore.Qt.AlignRight)
        Req_grid.addWidget(self.Picture_lw,10,1,5,7)
        Req_grid.addWidget(self.Dimension_label,15,0,QtCore.Qt.AlignRight)
        Req_grid.addWidget(self.DimensionL_sbox,15,1,1,1)
        Req_grid.addWidget(self.DimenInX_label,15,2,QtCore.Qt.AlignLeft)
        Req_grid.addWidget(self.DimensionW_sbox,15,3,1,1)
        Req_grid.addWidget(self.DimenInX2_label,15,4,QtCore.Qt.AlignLeft)
        Req_grid.addWidget(self.DimensionH_sbox,15,5,1,1)
        Req_grid.addWidget(self.DimenIn_label,15,6,QtCore.Qt.AlignLeft)
        Req_grid.addWidget(self.Weight_label,16,0,QtCore.Qt.AlignRight)
        Req_grid.addWidget(self.WeightLbs_sbox,16,1,1,1)
        Req_grid.addWidget(self.WeightLbs_label,16,2,QtCore.Qt.AlignLeft)
        Req_grid.addWidget(self.WeightOz_sbox,16,3,1,1)
        Req_grid.addWidget(self.WeightOz_label,16,4,QtCore.Qt.AlignLeft)
        Req_grid.addWidget(Ship_groupbox,17,0,1,8)
        Req_groupbox.setLayout(Req_grid)
        
        AandJ_grid.addWidget(self.ItemID_label,1,0,QtCore.Qt.AlignRight)
        AandJ_grid.addWidget(self.ItemID_ledit,1,1,1,5)
        AandJ_grid.addWidget(self.Location_label,2,0,QtCore.Qt.AlignRight)
        AandJ_grid.addWidget(self.Location_ledit,2,1,1,5)
        AandJ_groupbox.setLayout(AandJ_grid)

        Main_grid.addWidget(Title_groupbox,1,0,10,5)
        Main_grid.addWidget(AandJ_groupbox,1,5,10,5)
        Main_grid.addWidget(Req_groupbox,11,0,10,10)
        Main_grid.addLayout(Buttons_hlay,21,6,1,4)
        Buttons_hlay.insertStretch(0)
        Buttons_hlay.insertWidget(1,self.Cancel_button)
        Buttons_hlay.insertWidget(2,self.AddList_button)
        Main_grid.addWidget(self.Req_label,22,9,QtCore.Qt.AlignRight)
        
        self.setLayout(Main_grid)

    def closeEvent(self,event):
        del files[:]

    def Cancel(self):
        self.close()

    def ChooseCat(self):
        """Choose Category Window"""
        self.w = cc.ChooseCategory(self)
        self.w.show()

    def AddListing(self,p):
        """Add Listing on Ebay"""

        #AJT.CatFeatures(self)
        message = ""
        add = True
        if(len(self.PartNumber_ledit.text()) == 0):
            message = message + "Please enter a Part Number.\n"
            add = False
        if(len(self.Model_ledit.text()) == 0):
            message = message + "Please enter the Model. \n"
            add = False
        if(len(self.Description_ledit.text()) == 0):
            message = message + "Please enter the Description.\n"
            add = False
        if(len(self.ItemID_ledit.text()) == 0):
            message = message + "Please specify the Item ID Number.\n"
            add = False
        if(len(self.Location_ledit.text()) == 0):
            message = message + "Please specify the Location of the item.\n"
            add = False
        if(self.Price_sbox.value() == 0.00):
            message = message + "Please set a Price.\n"
            add = False
        if(self.Quantity_sbox.value() == 0):
            message = message + "Please specify the Quantity.\n"
            add = False
        if(self.CategoryValue == 0):
            message = message + "Please choose a Category.\n"
            add = False
        if(self.Condition_cbox.currentIndex() == 0):
            message = message + "Please specify the Condition.\n"
            add = False
        if(len(self.Picture_lw.selectedItems()) == 0):
            message = message + "Please choose at least 1 photo.\n"
            add = False
        if(self.DimensionL_sbox.value() == 0 and
           self.DimensionW_sbox.value() == 0 and
           self.DimensionH_sbox.value() == 0):
            message = message + "Please specify the Dimensions.\n"
            add = False
        if(self.WeightLbs_sbox.value() == 0 and
           self.WeightOz_sbox.value() == 0):
            message = message + "Please specify the Weight.\n"
            add = False
        if(not self.Ship1_chbox.isChecked() and
           not self.Ship2_chbox.isChecked() and
           not self.Ship2_chbox.isChecked()):
            message = message + "Please choose a Shipping option."
            add = False
        if(add):
            AJT.AddListing(self)
            p.UpdateInventory()
            self.close()
        else:
            Msgbox = QtGui.QMessageBox.information(self,"New Listing Error",message)
            
