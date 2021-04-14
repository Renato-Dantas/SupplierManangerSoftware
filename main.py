#pyuic5 design.ui -o design.py
#pyrcc5 Icones.qrc -o Icones_rc.py
from sys import argv
from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QTableWidgetItem, QMessageBox, QStyledItemDelegate, QHeaderView
from PyQt5 import QtGui, QtCore
from design import Ui_MainWindow
from sqlStructure import sqliteFunctions
from loginDesign import Ui_loginWindow

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
        self.rb_areaSearch.clicked.connect(self.areaSearch)
        self.rb_nameSearch.clicked.connect(self.nameSearch)

        # Set Add Page Buttons
        self.bt_save.clicked.connect(self.saveAddValues)
        self.bt_cancel.clicked.connect(self.cancelAddPage)
        
        # Set Update Page Buttons
        self.bt_upload.clicked.connect(self.uploadValuesUpdatePage)
        self.bt_updateInfo.clicked.connect(self.updateValues)
        self.bt_deleteData.clicked.connect(self.deleteInfo)
        self.restartCbUpdate()

        # ComboBox with the area list on the Search Page
        for area in self.sql.readTxt():
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
    
    # Delete all information on the lines
    def cancelAddPage(self):
        self.ipt_addID.setText('')
        self.ipt_addName.setText('')
        self.addPageCBox.setCurrentIndex(0)
        self.ipt_addAddress.setText('')
        self.ipt_addEmail.setText('')
        self.ipt_addPhone1.setText('')
        self.ipt_addPhone2.setText('')
        self.ipt_addWebsite.setText('')
    
    # Upload data to fields on the Update Page table
    def uploadValuesUpdatePage(self):
        try:
            data = self.sql.searchSqlName(self.cb_searchName.currentText())
            data = list(data[0])
            self.ipt_updateId.setText(data[0])
            self.ipt_updateName.setText(data[1])
            self.updatePageCBox.setCurrentText(data[2])
            self.ipt_updateAddress.setText(data[3])
            self.ipt_updateEmail.setText(data[4])
            self.ipt_updatePhone1.setText(data[5])
            self.ipt_updatePhone2.setText(data[6])
            self.ipt_updateWebsite.setText(data[7])

        except IndexError:
            self.popup("This info doesn't exists on database anymore!")
    

    # Update the new values on the database    
    def updateValues(self):
        data = self.getValuesUpdatePage()
        data.append(self.cb_searchName.currentText())
        if '' in data[:6]:
            self.popup('Please insert all required data!')
        else:
            try:
                self.sql.startDb()
                self.sql.updateData(data)
                self.popup('Supplier Updated!')
            finally:
                self.sql.closeConnection()
                self.clearUpdateValues()

    # Clear all the fields after delete or update an info
    def clearUpdateValues(self):
        self.ipt_updateId.setText('')
        self.ipt_updateName.setText('')
        self.updatePageCBox.setCurrentIndex(0)
        self.ipt_updateAddress.setText('')
        self.ipt_updateEmail.setText('')
        self.ipt_updatePhone1.setText('')
        self.ipt_updatePhone2.setText('')
        self.ipt_updateWebsite.setText('')
        self.restartCbUpdate()

    def restartCbUpdate(self):
        self.cb_searchName.clear()
        for name in self.sql.searchListNames():
            self.cb_searchName.addItem(str(name[0]))       

    # Check Boxes to choose the search parameter on the Search Page
    def areaSearch(self):
        self.cb_search.clear()
        for area in self.sql.readTxt():
            self.cb_search.addItem(area)
    
    def nameSearch(self):
        self.cb_search.clear()
        for name in self.sql.searchListNames():
            self.cb_search.addItem(str(name[0]))

    # Function to save the data from Add Page on the database
    def saveAddValues(self):
        listValues = self.getValuesAddPage()
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
                self.cancelAddPage()
                self.restartCbUpdate()

    # Function to search on the database the info according the radio button selected
    def searchInfo(self):
        if self.rb_areaSearch.isChecked() == True:
            data = self.sql.searchSqlArea(self.cb_search.currentText())

        elif self.rb_nameSearch.isChecked() == True:
            data = self.sql.searchSqlName(self.cb_search.currentText())
        return data

    # Delete permanently all data from a supplier
    def deleteInfo(self):
        name = self.ipt_updateName.text()
        reply = self.question()
        if reply == QMessageBox.Yes:
            try:
                self.sql.deleteData(name)
                self.popup('Info deleted!')
            except:
                self.popup('You must upload a supplier data before delete!')
            finally:
                self.sql.closeConnection()
                self.clearUpdateValues()
                self.cb_searchName.setCurrentIndex(0)
        else:
            print('No clicked.')
            self.clearUpdateValues()
            self.cb_searchName.setCurrentIndex(0)
            pass
        
    # Function to consult the database and put data on a table
    def showTable(self, data):         
        try:
            data = self.searchInfo()
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
        except UnboundLocalError:
            self.popup('Please select on the right corner the search parameter!')

    # Funcion to show a popup on the screen        
    def popup(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Information")
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    # Popup with confirmation to delete an info
    def question(self):
        reply = QMessageBox.question(self, 'WARNING', "Do you really want to delete this info?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply


class login(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui =  Ui_loginWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.ui.bt_login.clicked.connect(self.mainApp)
        self.ui.bt_cancel.clicked.connect(self.close)

    def mainApp(self):
        if self.ui.ipt_password.text() == 'dantas' and self.ui.ipt_user.text() == 'adm':
            self.close()
            self.main = main()
            self.main.show()
        else:
            self.popup('Wrong Password!')

    def popup(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()


if __name__ == '__main__':
    qt = QApplication(argv)
    screen = login()
    screen.show()
    qt.exec_()