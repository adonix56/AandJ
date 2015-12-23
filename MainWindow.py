from PyQt4 import QtGui, QtCore
import NewListing as nl
import AandJTrading as AJT
import sys
import urllib.request

testdata = {'Title':['50311-ZW1-040ZA, 50301-ZW1-040ZA L.&amp;R Stern &amp; Tilting Shaft, 2004 Honda 75HP','Ttest','T12754953','T16745821'],
            'Price':['$642.00','$31.77','$52.00','$5632.00'],
            'Quantity':['1','22','1','3'],
            'TimeStarted':['2015-05-05T17:22:27.000Z','OMC','Mercury','Yamaha'],
            'TimeLeft':['67d 23h 46m 32s','149.99','179.99','4999.99'],
            'ListDuration':['Forever','Forever','90 Days','Forever']}

comparedata = {'Listing Title':['NEW! GENUINE OEM OMC P/N 328584 RUBBER SHOCK MOUNT LOWER COVER EVINRUDE JOHNSON',
                                '0349557 328584 Evinrude Johnson Outboard Lower Engine Cover Motor Mounts',
                                '328584, Mount, 1997 Evinrude 150hp (XL) M#E150|XEUC',
                                'Johnson Evinrude Lower Cover Mount & Stud 329743 & 328584 1985-2001 90-250 HP'],
               'Seller':['petersonmarinepinellas','outboardheaven','aandjproparts-us','scoutboards'],
               'Price':['US$9.50','US$14.95','US$2.75','US$13.00'],
               'Shipping Price':['US$3.00','US$11.16','US$4.14','FREE'],
               'BuyItNow/Auction':['B','B','B','B'],
               '# of Bids':['N/A','N/A','N/A','N/A'],
               'Quantity':['1','1','2','2'],
               'Sold':['N/A','N/A','N/A','N/A']}

class AandJ(QtGui.QMainWindow):

    def __init__(self):
        super(AandJ, self).__init__()
        self.setGeometry(50,50,1700,1000)
        self.setWindowTitle("AandJ eBay Application")
        self.setWindowIcon(QtGui.QIcon('icons/AandJ.ico'))
        self.testvalue = "boo yah"
        self.createMenu()
        self.createToolBar()
        self.createWidgets()
        self.UpdateInventory()
        self.show()

    def createMenu(self):
        """Create Menu Bar and Status Bar"""
        #Actions
        newAction = QtGui.QAction("&New...",self)
        newAction.setShortcut("Ctrl+N")
        newAction.setStatusTip('Create New Listing')
        newAction.triggered.connect(self.NewListing)
        updAction = QtGui.QAction("&Update...",self)
        updAction.setShortcut("Ctrl+U")
        updAction.setStatusTip('Update Inventory')
        updAction.triggered.connect(self.UpdateInventory)

        #Initiate and add actions
        self.statusBar()
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(updAction)
        editMenu = mainMenu.addMenu('&Edit')

    def createToolBar(self):
        """Create Toolbar"""
        #Actions
        newAction = QtGui.QAction(QtGui.QIcon('icons/plus.png'),"New Listing",self)
        newAction.triggered.connect(self.NewListing)
        updAction = QtGui.QAction(QtGui.QIcon('icons/Update.png'),"Update Inventory",self)
        updAction.triggered.connect(self.UpdateInventory)

        #Initiate and add actions
        self.toolBar = self.addToolBar("Test")
        self.toolBar.addAction(newAction)
        self.toolBar.addAction(updAction)
    
    def createWidgets(self):
        """Create Widgets for Main Window"""
        #Compare Widgets
        Search_label = QtGui.QLabel('Search Keyword(s):')
        Search_ledit = QtGui.QLineEdit()
        Search_button = QtGui.QPushButton('Search',self)
        Search_button.clicked.connect(self.SearchKeyword)
        
        #Inventory Tables
        self.Table = {}
        self.Inventory = QtGui.QTableWidget(100,6)
        #horHeaders = []
        self.horHeaders = ['Title','Price','Quantity','TimeStarted','TimeLeft','ListDuration']
        self.Inventory.setHorizontalHeaderLabels(self.horHeaders)
        self.Inventory.setColumnWidth(0,550) #Title Width
        self.Inventory.setColumnWidth(1,100) #Price Width
        self.Inventory.setColumnWidth(2,70)  #Quantity Width
        self.Inventory.setColumnWidth(3,160) #Time Started Width
        self.Inventory.setColumnWidth(4,110) #Time Left Width
        self.Inventory.setColumnWidth(5,80)  #List Duration Width
        self.Inventory.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.Inventory.cellClicked.connect(self.selectRow)
        '''i = 0
        while(i != self.Inventory.columnCount()):
            self.Inventory.setColumnWidth(i,self.Inventory.sizeHintForColumn(i))
            i = i + 1'''

        Compare = QtGui.QTableWidget(100,8,self)
        comHeaders = []
        for n, key in enumerate(sorted(comparedata.keys())):
            comHeaders.append(key)
            for m, item in enumerate(comparedata[key]):
                newitem = QtGui.QTableWidgetItem(item)
                Compare.setItem(m,n,newitem)
        Compare.setHorizontalHeaderLabels(comHeaders)
        
        #Tab Widget
        Main_tabwidget = QtGui.QTabWidget()
        Inventory_tab = QtGui.QWidget()
        Compare_tab = QtGui.QWidget()

        #Display
        self.currentSelection = "None"
        self.Display_groupbox = QtGui.QGroupBox('Item Details')
        self.Display_groupbox.setMaximumWidth(525)
        self.Thumbnail_pixmap = QtGui.QLabel('Choose an Item...')
        self.Thumbnail_image = QtGui.QImage()
        self.Description_label = QtGui.QLabel('Description:')
        self.PartNumber_label = QtGui.QLabel('Part Number/UPC:')
        self.Model_label = QtGui.QLabel('Model:')
        self.ItemID_label = QtGui.QLabel('Item ID Number:')
        self.Location_label = QtGui.QLabel('Location:')
        self.Quantity_label = QtGui.QLabel('Quantity:')
        self.Price_label = QtGui.QLabel('Price:')
        self.TimeStart_label = QtGui.QLabel('Time Started:')
        self.TimeEnd_label = QtGui.QLabel('Time End:')
        self.ListDuration_label = QtGui.QLabel('List Duration:')
        self.TimeLeft_label = QtGui.QLabel('Time Left:')
        self.Description_ledit = QtGui.QLineEdit()
        self.Description_ledit.setReadOnly(True)
        self.Model_ledit = QtGui.QLineEdit()
        self.Model_ledit.setReadOnly(True)
        self.PartNumber_ledit = QtGui.QLineEdit()
        self.PartNumber_ledit.setReadOnly(True)
        self.ItemID_ledit = QtGui.QLineEdit()
        self.ItemID_ledit.setReadOnly(True)
        self.Location_ledit = QtGui.QLineEdit()
        self.Location_ledit.setReadOnly(True)
        self.Quantity_ledit = QtGui.QLineEdit()
        self.Quantity_ledit.setReadOnly(True)
        self.Price_ledit = QtGui.QLineEdit()
        self.Price_ledit.setReadOnly(True)
        self.TimeStart_ledit = QtGui.QLineEdit()
        self.TimeStart_ledit.setReadOnly(True)
        self.TimeEnd_ledit = QtGui.QLineEdit()
        self.TimeEnd_ledit.setReadOnly(True)
        self.ListDuration_ledit = QtGui.QLineEdit()
        self.ListDuration_ledit.setReadOnly(True)
        self.TimeLeft_ledit = QtGui.QLineEdit()
        self.TimeLeft_ledit.setReadOnly(True)

        #Grid Layout
        self.Display_grid = QtGui.QGridLayout()
        self.Display_grid.addWidget(self.Thumbnail_pixmap,2,0,1,2,QtCore.Qt.AlignCenter)
        self.Display_grid.addWidget(self.Description_label,3,0,QtCore.Qt.AlignRight)
        self.Display_grid.addWidget(self.Description_ledit,3,1)
        self.Display_grid.addWidget(self.PartNumber_label,4,0,QtCore.Qt.AlignRight)
        self.Display_grid.addWidget(self.PartNumber_ledit,4,1)
        self.Display_grid.addWidget(self.Model_label,5,0,QtCore.Qt.AlignRight)
        self.Display_grid.addWidget(self.Model_ledit,5,1)
        self.Display_grid.addWidget(self.ItemID_label,6,0,QtCore.Qt.AlignRight)
        self.Display_grid.addWidget(self.ItemID_ledit,6,1)
        self.Display_grid.addWidget(self.Location_label,7,0,QtCore.Qt.AlignRight)
        self.Display_grid.addWidget(self.Location_ledit,7,1)
        self.Display_grid.addWidget(self.Quantity_label,8,0,QtCore.Qt.AlignRight)
        self.Display_grid.addWidget(self.Quantity_ledit,8,1)
        self.Display_grid.addWidget(self.Price_label,9,0,QtCore.Qt.AlignRight)
        self.Display_grid.addWidget(self.Price_ledit,9,1)
        self.Display_grid.addWidget(self.TimeStart_label,10,0,QtCore.Qt.AlignRight)
        self.Display_grid.addWidget(self.TimeStart_ledit,10,1)
        self.Display_grid.addWidget(self.TimeEnd_label,11,0,QtCore.Qt.AlignRight)
        self.Display_grid.addWidget(self.TimeEnd_ledit,11,1)
        self.Display_grid.addWidget(self.ListDuration_label,12,0,QtCore.Qt.AlignRight)
        self.Display_grid.addWidget(self.ListDuration_ledit,12,1)
        self.Display_grid.addWidget(self.TimeLeft_label,13,0,QtCore.Qt.AlignRight)
        self.Display_grid.addWidget(self.TimeLeft_ledit,13,1)
        self.Display_groupbox.setLayout(self.Display_grid)

        Inventory_grid = QtGui.QGridLayout(Inventory_tab)
        Inventory_grid.setSpacing(10)
        Inventory_grid.addWidget(self.Inventory,1,0)
        Inventory_grid.addWidget(self.Display_groupbox,1,1)

        Compare_grid = QtGui.QGridLayout(Compare_tab)
        Compare_grid.setSpacing(10)
        Compare_grid.addWidget(Search_label,1,0)
        Compare_grid.addWidget(Search_ledit,1,1)
        Compare_grid.addWidget(Search_button,1,2)
        Compare_grid.addWidget(Compare,2,0,1,3)
        Main_tabwidget.addTab(Inventory_tab,'Inventory')
        Main_tabwidget.addTab(Compare_tab,'Compare Items')
        
        self.setCentralWidget(Main_tabwidget)
        

    def UpdateInventory(self):
        """Update the Inventory"""
        self.Table = AJT.UpdateInventory(self)
        if(self.Table):
            self.Inventory.setRowCount(len(self.Table["Quantity"]))
            for n, key in enumerate(self.horHeaders):#enumerate(self.Table.keys()):
                #horHeaders.append(key)
                for m, item in enumerate(self.Table[key]):
                    newitem = QtGui.QTableWidgetItem(item)
                    self.Inventory.setItem(m,n,newitem)
        else:
            self.Inventory.setRowCount(0)
        #print(AJT.UpdateInventory(self))

    def NewListing(self):
        """Open New Window"""
        self.w = nl.NewListing(self)
        self.w.show()

    def SearchKeyword(self):
        """Search eBay Keywords"""
        print("TODO:Search Keyword")

    def selectRow(self):
        if(self.currentSelection != self.Inventory.currentRow()):
            self.currentSelection = self.Inventory.currentRow()
            print("NEW SELECTION!")
            row = AJT.getItemDetails(self.Table['ItemID'][self.currentSelection])
            i = self.Table['Title'][self.currentSelection]
            j = i[:i.find(' ')]
            i = i[i.find(' ')+1:]
            self.PartNumber_ledit.setText(j)
            j = i[:i.rfind(',')]
            i = i[i.rfind(',')+2:]
            self.Description_ledit.setText(j)
            self.Model_ledit.setText(i)
            self.ItemID_ledit.setText("")#TODO:Get ItemID
            self.Location_ledit.setText("")#TODO:Get Location
            self.Quantity_ledit.setText(self.Table['Quantity'][self.currentSelection])
            self.Price_ledit.setText(self.Table['Price'][self.currentSelection])
            self.TimeStart_ledit.setText(self.Table['TimeStarted'][self.currentSelection])
            self.ListDuration_ledit.setText(self.Table['ListDuration'][self.currentSelection])
            self.TimeLeft_ledit.setText(self.Table['TimeLeft'][self.currentSelection])
            self.TimeEnd_ledit.setText(row[0])
            data = urllib.request.urlopen(row[1]).read()
            self.Thumbnail_image.loadFromData(data)
            self.Thumbnail_pixmap.setPixmap(QtGui.QPixmap(self.Thumbnail_image))
