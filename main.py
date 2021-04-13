#pyuic5 design.ui -o design.py
#pyrcc5 Icones.qrc -o Icones_rc.py
from sys import argv
from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QTableWidgetItem, QMessageBox, QStyledItemDelegate, QHeaderView
from PyQt5 import QtGui, QtCore
from design import Ui_MainWindow
from sqlStructure import sqliteFunctions


class main(QMainWindow, Ui_MainWindow, sqliteFunctions):
    def __init__(self, parent = None):
        super().__init__(parent)
        super().setupUi(self)
        super()
        self.sql = sqliteFunctions()

        # Set Page Navigate Buttons
        self.bt_searchPage.clicked.connect(lambda: self.pages.setCurrentWidget(self.pageSearch))
        self.bt_addPage.clicked.connect(lambda: self.pages.setCurrentWidget(self.pageAdd))
        self.bt_updatePage.clicked.connect(lambda: self.pages.setCurrentWidget(self.pageUpdate)) 

        # Set Search Page Buttons
        self.btSearch.clicked.connect(self.showTable)
        self.btSearchName.clicked.connect(self.changeOptions)


        # Set Add Page Buttons
        self.bt_save.clicked.connect(lambda: self.saveAddValues(getValuesAddPage(self)))
        
        # Set Update Page Buttons
        #self.bt_updateInfo.clicked.connect(lambda: printando(self, getValuesUpdatePage(self)))

        # ComboBox with the area list on the Search Page
        areaList = self.sql.readTxt()
        for area in areaList:
            self.cb_search.addItem(area)
            self.addPageCBox.addItem(area)
            self.updatePageCBox.addItem(area)
                        
        # Set the headers to a stretch size
        header = self.infoTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        header.setSectionResizeMode(6, QHeaderView.Stretch)
        header.setSectionResizeMode(7, QHeaderView.Stretch)

        # Getting the inputs on the Add Page
        def getValuesAddPage(self):
            id = self.ipt_addID.text()
            name = self.ipt_addName.text()
            area = self.addPageCBox.currentText()
            address = self.ipt_addAddress.text()
            email = self.ipt_addEmail.text()
            phone = self.ipt_addPhone1.text()
            phone2 = self.ipt_addPhone2.text()
            website = self.ipt_addWebsite.text()
            return [id,name,area, address, email, phone, phone2, website]
            
        # Getting the inputs on the Update Page
        def getValuesUpdatePage(self):
            id = self.ipt_updateId.text()
            name = self.ipt_updateName.text()
            area = self.updatePageCBox.currentText()
            address = self.ipt_updateAddress.text()
            email = self.ipt_updateEmail.text()
            phone = self.ipt_updatePhone1.text()
            phone2 = self.ipt_updatePhone2.text()
            website = self.ipt_updateWebsite.text()
            return [id,name,area, address, email, phone, phone2, website]
        
    # Essa função deverá mudar a listagem pra nomes, mas se clicado novamente, deve mudar de volta pra area
    def changeOptions(self):
        optionName = False
        if optionName == False:
            nameList = self.sql.searchListNames()
            self.cb_search.clear()
            for name in nameList:
                self.cb_search.addItem(name[0])
            optionName = True
        else:
            areaList = self.sql.readTxt()
            for area in areaList:
                self.cb_search.clear()
                self.cb_search.addItem(area)
            optionName = False

    # Function to save the data from Add Page on the database
    def saveAddValues(self, listValues):
        if '' in listValues[:6]:
                self.popup('Please insert all required data!')
        else:
            try:
                self.sql.startDb()
                self.sql.insertValues(listValues)
                self.popup('Information Successful Saved!')
            except:
                self.popup('You are trying to inser a duplicated ID. Please change the Id to save.')
            finally:
                self.sql.closeConnection()

    # Function to consult the database and put data on a table
   

    def showTable(self):
         
        area = self.cb_search.currentText()
        data = self.sql.searchSqlArea(area)
        information = [info for info in data]
        
        row, index = 0,0
        self.infoTable.setRowCount(len(information))
        for info in information:
            self.infoTable.setItem(row, 0, QTableWidgetItem(information[index][0]))
            self.infoTable.setItem(row, 1, QTableWidgetItem(information[index][1]))
            self.infoTable.setItem(row, 2, QTableWidgetItem(information[index][2]))
            self.infoTable.setItem(row, 3, QTableWidgetItem(information[index][3]))
            self.infoTable.setItem(row, 4, QTableWidgetItem(information[index][4]))
            self.infoTable.setItem(row, 5, QTableWidgetItem(information[index][5]))
            self.infoTable.setItem(row, 6, QTableWidgetItem(information[index][6]))
            self.infoTable.setItem(row, 7, QTableWidgetItem(information[index][7]))
            row +=1
            index +=1           
        
    def searchName(self):
        self.cb_search.setText('Funciona!')


    def popup(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Information")
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

if __name__ == '__main__':
    qt = QApplication(argv)
    screen = main()
    screen.show()
    qt.exec_()