import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

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

Base = declarative_base()

engine = sqlalchemy.create_engine('sqlite:///' + r"D:\sqlite\db\task3.db", echo=False)

Session = sessionmaker(bind=engine)
session = Session()


class Performer(Base):
    __tablename__ = 'performers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    contry = Column(String)
    years = Column(Integer)
    books = relationship('Book', back_populates='performer')

    def __repr__(self):
        return "<Performer(name='%s', desc='%s')>" % (
            self.name, self.desc)


class Password(Base):
    __tablename__ = 'passwords'

    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<Password(name='%s', desc='%s')>" % (
            self.name, self.desc)


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    pages = Column(Integer)
    release = Column(String)
    release_year = Column(Integer)
    perfid = Column(Integer, ForeignKey('performers.id'))
    performer = relationship('Performer', back_populates='books')

    def __repr__(self):
        return "<Book(name='%s', year='%d')>" % (
            self.name, self.release_year)


def insert_records_via_ORM():
    performer = Performer(name="Pushkin", contry='Russia', years=1998)
    session.add(performer)
    session.commit()

    pass1 = Password(login="login", password="login")
    session.add(pass1)
    session.commit()

    performer = session.query(Performer).filter(Performer.name == "Pushkin").first()
    if performer:
        album = Book(name="Alisa", release_year=1888, pages=234, release="zarya")
        performer.books.append(album)
        session.add(album)
        session.flush()
        session.commit()
    else:
        print('No such performer!')


def select_records_via_ORM():
    performers = [(performer.id, performer.name, performer.contry, performer.years) for performer in
                  session.query(Performer)]
    albums = [(album.performer.name, album.name, album.release_year, album.pages, album.release)
              for album in session.query(Book)]
    return performers, albums


def select_passwords():
    psswor = [(passw.login, passw.password) for passw in session.query(Password)]
    return psswor


def adau(_name, _contry, _year):
    performer = Performer(name=_name, contry=_contry, years=int(_year))
    session.add(performer)
    session.commit()


def adbo(_name, _pages, _release, _release_year, auid):
    performer = session.query(Performer).filter(Performer.name == auid).first()
    if performer:
        album = Book(name=_name, release_year=int(_release_year), pages=int(_pages), release=_release)
        performer.books.append(album)
        session.add(album)
        session.flush()
        session.commit()
    else:
        print('No such performer!')


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
        performers, albums = select_records_via_ORM()
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
        self.label_5.setText(_translate("Form", "author_name"))


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
        performers, albums = select_records_via_ORM()
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
        performers, albums = select_records_via_ORM()
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
        self.pushButton_6.clicked.connect(self.select3)
        self.pushButton_4.clicked.connect(self.select1)
        self.pushButton_5.clicked.connect(self.select2)
        self.pushButton_7.clicked.connect(self.select4)
        performers, albums = select_records_via_ORM()
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

    def select3(self):
        albums = [(album.performer.name, album.name, album.release_year, album.pages, album.release)
                  for album in session.query(Book).filter(Book.pages > 380)]
        self.listWidget_2.clear()
        for alb in albums:
            out = " ".join(str(x) for x in alb)
            self.listWidget_2.addItem(out)

    def select1(self):
        performers1 = [(performer.id, performer.name, performer.contry, performer.years) for performer in
                       session.query(Performer).filter(Performer.years > 1600).filter(Performer.years < 2000).all()]
        self.listWidget.clear()
        for per in performers1:
            out = " ".join(str(x) for x in per)
            self.listWidget.addItem(out)

    def select2(self):
        albums = [(album.performer.name, album.name, album.release_year, album.pages, album.release)
                  for album in session.query(Book).join(Performer).filter(Performer.contry == "Russia")]
        self.listWidget_2.clear()
        for alb in albums:
            out = " ".join(str(x) for x in alb)
            self.listWidget_2.addItem(out)

    def select4(self):
        performers1 = [(performer.books, performer.id, performer.name, performer.contry, performer.years) for performer
                       in session.query(Performer)]
        self.listWidget.clear()
        for per in performers1:
            if len(per[0]) > 2:
                out = " ".join(str(x) for x in per[1:5])
                self.listWidget.addItem(out)


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
