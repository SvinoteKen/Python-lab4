import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import win  # Это наш конвертированный файл дизайна
import os
import sqlite3
import simplejson
import auth
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets


def create_database():
    # создаем базу данных sqlite 
    # (присоединяемся к ней первый раз)
    db = sqlite3.connect(r"D:\sqlite\db\mydb.db")

    with db:
        # Получаем объект курсора
        cursor = db.cursor()

        # SQL-запрос #1:
        cursor.execute('''
            CREATE TABLE performers(id INTEGER PRIMARY KEY, 
                                    name TEXT, 
                                    contry TEXT,
                                    years INTEGER)
        ''')
        db.commit()

        cursor.execute('''
            CREATE TABLE passwords(id INTEGER PRIMARY KEY, 
                                    login TEXT, 
                                    password TEXT)
        ''')
        db.commit()

        # SQL-запрос #2:
        cursor.execute('''
               CREATE TABLE books(
               id INTEGER PRIMARY KEY, 
               name TEXT,
               pages INTEGER,
               release TEXT,
               release_year INTEGER,
               perfid INTEGER,
               FOREIGN KEY(perfid) REFERENCES performers(id))
               ''')
        db.commit()


def insert_records():
    db = sqlite3.connect(r"D:\sqlite\db\mydb.db")
    with db:
        cursor = db.cursor()
        cursor.execute('INSERT INTO performers VALUES(NULL, "Pushkin", "Russia", 45)')
        db.commit()

        cursor.execute('INSERT INTO books VALUES(NULL, "Alisa", 334, "zarya", 2000, 1)')
        db.commit()

        cursor.execute('INSERT INTO passwords VALUES(NULL, "login", "login")')
        db.commit()


def select_records():
    db = sqlite3.connect(r"D:\sqlite\db\mydb.db")

    with db:
        cursor = db.cursor()
        cursor.execute('SELECT id, name, contry, years from performers')
        performers = cursor.fetchall()

        cursor.execute('''
                SELECT performers.name, books.name, books.pages, books.release, books.release_year
                from books INNER JOIN performers ON books.perfID = performers.id
                ''')
        books = cursor.fetchall()
        return performers, books


def select_passwords():
    db = sqlite3.connect(r"D:\sqlite\db\mydb.db")

    with db:
        cursor = db.cursor()
        cursor.execute('SELECT login, password from passwords')
        passwords = cursor.fetchall()
        return passwords


def adau(name, contry, year):
    db = sqlite3.connect(r"D:\sqlite\db\mydb.db")
    with db:
        cursor = db.cursor()
        perfID = int(year)
        albumname = name
        albumyear = contry
        # Здесь лучше: делаем параметризированный запрос
        cursor.execute('INSERT INTO performers VALUES(NULL, ?, ?, ?)',
                       (albumname, albumyear, perfID))
        db.commit()


def adbo(name, pages, release, release_year, auid):
    db = sqlite3.connect(r"D:\sqlite\db\mydb.db")
    with db:
        cursor = db.cursor()
        rly = int(release_year)
        albumname = name
        albumyear = int(pages)
        rrl = release
        idd = auid
        # Здесь лучше: делаем параметризированный запрос
        cursor.execute('INSERT INTO books VALUES(NULL, ?, ?, ?, ?, ?)',
                       (albumname, albumyear, rrl, rly, auid))
        db.commit()


class Ui_Form1(object):
    def __init__(self, mai):
        self.ma = mai

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(445, 350)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(270, 120, 91, 31))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(40, 40, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(40, 100, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(40, 160, 113, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(40, 220, 113, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(Form)
        self.lineEdit_5.setGeometry(QtCore.QRect(40, 280, 113, 20))
        self.lineEdit_5.setObjectName("lineEdit_5")

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 10, 101, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 70, 101, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(40, 130, 101, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(40, 190, 101, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(40, 260, 101, 21))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.pushButton.clicked.connect(self.add_bo)

    def add_bo(self):
        adbo(self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(),
             self.lineEdit_5.text())
        self.ma.listWidget_2.clear()
        self.ma.listWidget.clear()
        performers, albums = select_records()
        for per in performers:
            out = " ".join(str(x) for x in per)
            self.ma.listWidget.addItem(out)
        for alb in albums:
            out = " ".join(str(x) for x in alb)
            self.ma.listWidget_2.addItem(out)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "ADD"))
        self.label.setText(_translate("Form", "Name"))
        self.label_2.setText(_translate("Form", "pages"))
        self.label_3.setText(_translate("Form", "release"))
        self.label_4.setText(_translate("Form", "release_year"))
        self.label_5.setText(_translate("Form", "author_id"))


class Ui_Form(object):
    def __init__(self, mai):
        self.ma = mai

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(445, 286)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(270, 120, 91, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(270, 170, 91, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(40, 90, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(40, 150, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(40, 210, 113, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 60, 101, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 180, 101, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(40, 120, 101, 21))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.pushButton.clicked.connect(self.add_au)
        self.pushButton_2.clicked.connect(self.parse)

    def add_au(self):
        adau(self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text())
        self.ma.listWidget.clear()
        self.ma.listWidget_2.clear()
        performers, albums = select_records()
        for per in performers:
            out = " ".join(str(x) for x in per)
            self.ma.listWidget.addItem(out)
        for alb in albums:
            out = " ".join(str(x) for x in alb)
            self.ma.listWidget_2.addItem(out)

    def parse(self):
        filepath = QtWidgets.QFileDialog.getOpenFileName(self.ma, "Выберите file")
        tree = ET.parse(filepath[0])
        root = tree.getroot()
        adau(root[0].text, root[1].text, root[2].text)
        self.ma.listWidget.clear()
        self.ma.listWidget_2.clear()
        performers, albums = select_records()
        for per in performers:
            out = " ".join(str(x) for x in per)
            self.ma.listWidget.addItem(out)
        for alb in albums:
            out = " ".join(str(x) for x in alb)
            self.ma.listWidget_2.addItem(out)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "ADD"))
        self.pushButton_2.setText(_translate("Form", "Parse from file"))
        self.label.setText(_translate("Form", "Name"))
        self.label_2.setText(_translate("Form", "year"))
        self.label_3.setText(_translate("Form", "County"))


class ExampleApp(QtWidgets.QMainWindow, win.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton_3.clicked.connect(self.add_book)
        self.pushButton_2.clicked.connect(self.serial)
        self.pushButton.clicked.connect(self.add_author)
        performers, albums = select_records()
        for per in performers:
            out = " ".join(str(x) for x in per)
            self.listWidget.addItem(out)
        for alb in albums:
            out = " ".join(str(x) for x in alb)
            self.listWidget_2.addItem(out)

    def add_author(self):
        self.Form = QtWidgets.QWidget()
        self.ui = Ui_Form(self)
        self.ui.setupUi(self.Form)
        self.Form.show()

    def add_book(self):
        self.Form = QtWidgets.QWidget()
        self.ui = Ui_Form1(self)
        self.ui.setupUi(self.Form)
        self.Form.show()

    def serial(self):
        if self.radioButton.isChecked() == True:
            with open(r"D:\sqlite\db\data.json", 'w') as f:
                simplejson.dump(self.listWidget.currentItem().text(), f, indent=4)

        if self.radioButton_2.isChecked() == True:
            ll = self.listWidget.currentItem().text().split(' ')
            p = ET.Element('author')
            name = ET.SubElement(p, 'name')
            name.text = ll[1]
            contry = ET.SubElement(p, 'country')
            contry.text = ll[2]
            year = ET.SubElement(p, 'year')
            year.text = ll[3]
            tree = ET.ElementTree(p)
            tree.write(r"D:\sqlite\db\data.xml")


class ExampleApp1(QtWidgets.QMainWindow, auth.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.check_auth)

    def check_auth(self):
        passwords = select_passwords()
        for pa in passwords:
            if (pa[0] == self.lineEdit.text()) and (pa[1] == self.lineEdit_2.text()):
                self.hide()
                self.window = ExampleApp()
                self.window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp1()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно     
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()