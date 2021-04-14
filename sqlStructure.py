import sqlite3


class sqliteFunctions:

    def startDb(self):
        self.connector = sqlite3.connect('supplier.db')
        self.cursor = self.connector.cursor()
        
    def insertValues(self,info):
        insert = 'INSERT INTO supplier VALUES (?,?,?,?,?,?,?,?)'
        self.cursor.execute(insert, info)
        self.connector.commit()

    def selectAllData(self):
        self.startDb()
        self.cursor.execute('SELECT * FROM supplier')
        data = self.cursor.fetchall()
        return data
    
    def searchSqlArea(self, area):
        self.startDb()
        select = 'SELECT * FROM supplier WHERE area = ?'
        self.cursor.execute(select, [area])
        data = self.cursor.fetchall()
        return data
    
    def searchSqlName(self, name):
        self.startDb()
        select = 'SELECT * FROM supplier WHERE name = ?'
        self.cursor.execute(select, [name])
        data = self.cursor.fetchall()
        return data

    def updateData(self, data):
        #self.startDb()
        update = 'UPDATE supplier SET id = ?, name = ?, area = ?, city = ?, email = ?, phone1 = ?, phone2 = ?, link = ? WHERE name = ?'
        self.cursor.execute(update, data)
        self.connector.commit()

    def deleteData(self, name):
        self.startDb()
        delete = 'DELETE from supplier WHERE name = ?'
        self.cursor.execute(delete, [name])
        self.connector.commit()

    # Retorna uma lista com as áreas possíveis
    def readTxt(self):
        with open ('area.txt', encoding='UTF-8') as file:
            areaList = []
            for line in file:
                areaList.append(line.strip('\n'))
        return areaList

    def searchListNames(self):
        self.startDb()
        search = "SELECT name FROM supplier"
        self.cursor.execute(search)
        names = self.cursor.fetchall()
        return names

    def closeConnection(self):
        self.cursor.close()
        self.connector.close()