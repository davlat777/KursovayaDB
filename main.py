import sqlite3
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QFileDialog
from PyQt5 import QtWidgets
import Регистрация
import Вход
from Отчеты import Ui_Отчеты
from Пользователи import Ui_Пользователи
from Продукты import Ui_Продукты
from Работники import Ui_Работники
from Задачи import Ui_Задачи
from Заказы import Ui_Заказы

db = sqlite3.connect('database.db')
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users(login TEXT, password TEXT)''')
db.commit()

class Registration(QtWidgets.QMainWindow, Регистрация.Ui_Регистрация):  # регистрация
    def __init__(self):
        super(Registration, self).__init__()
        self.setupUi(self)
        self.patronymic_2.setPlaceholderText('Введите логин')
        self.patronymic_3.setPlaceholderText('Введите пароль')
        self.pushButton_2.pressed.connect(self.reg)  # регитрация
        self.pushButton.pressed.connect(self.login)  # переход на вход

    def login(self):  # показ класса логин (вход)
        self.login = Login()
        self.login.show()
        self.hide()

    def reg(self):  # регитрация
        try:
           user_login = self.patronymic_2.text()
           user_password = self.patronymic_3.text()

           if len(user_login) == 0:
               return
           if len(user_password) == 0:
               return
           cursor.execute(f'SELECT login FROM users WHERE login = "{user_login}" ')
           if cursor.fetchone() is None:
               cursor.execute(f'INSERT INTO users VALUES("{user_login}","{user_password}")')
               self.label_9.setText(f'Аккаунт {user_login} успешно зарегистрирован')
               db.commit()
           else:
               self.label_9.setText('Такая запись уже имеется')
        except Exception as e:
            self.label_9.setText(f'Аккаунт {user_login} успешно зарегистрирован')

class Login(QtWidgets.QMainWindow, Вход.Ui_Вход):  # вход
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.patronymic_2.setPlaceholderText('Введите логин')
        self.patronymic_3.setPlaceholderText('Введите пароль')
        self.pushButton.pressed.connect(self.login)
        self.pushButton_2.pressed.connect(self.reg)

    def reg(self):
        self.reg = Registration()
        self.reg.show()
        self.hide()

    def login(self):
        try:
            user_login = self.patronymic_2.text()
            user_password = self.patronymic_3.text()

            if len(user_login) == 0:
                return
            if len(user_password) == 0:
                return

            cursor.execute(f'SELECT password FROM users WHERE login = "{user_login}"')
            check_pass = cursor.fetchall()

            cursor.execute(f'SELECT login FROM users WHERE login = "{user_login}"')
            check_login = cursor.fetchall()
            print(check_login)
            print(check_pass)

            if check_pass[0][0] == user_password and check_login[0][0] == user_login:
                self.label_9.setText(f'Успешная авториазация')
                self.Отчеты = Отчеты()
                self.Отчеты.show()
                self.hide()
            else:
                self.label_9.setText(f'Ошибка авторизации')
        except Exception as e:
            self.label_9.setText(f'Ошибка авторизации')

POISKOT = ['ID_otcheta', 'Nazvanie', 'Data', 'Status', 'ID_zadaci']
class Отчеты(QWidget, Ui_Отчеты):
    def __init__(self):
        super(Отчеты, self).__init__()
        self.setupUi(self)
        self.pbopen.clicked.connect(self.open_otcheti)
        self.pbinsert.clicked.connect(self.insert_otcheti)
        self.pbdelete.clicked.connect(self.delete_otcheti)
        self.cbfind.addItems(POISKOT)
        self.pbfind.clicked.connect(self.search_otcheti)
        self.pbchange.clicked.connect(self.update_otcheti)

        self.pbpolzovateli.clicked.connect(self.show_Pz)


    def open_otcheti(self):  # кнопка
        try:
            self.conn = sqlite3.connect('proizvodstvo.db')
            cur = self.conn.cursor()
            data = cur.execute("select * from Отчеты;")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print("Ошибки с подключением к БД")
            return e
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elen in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elen)))
        self.tableWidget.resizeColumnsToContents()

    def update(self, query="select * from Отчеты"):  # после добавление сразу видно запись
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as d:
            print(f"Проблемы с подкл {d}")
            return d
        self.tableWidget.setRowCount(0)  # обнулмяем все данные из таблцы
        # заносим по новой
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elen in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elen)))
        self.tableWidget.resizeColumnsToContents()

    def insert_otcheti(self):  # кнопка добавить
        row = [self.lenazvanie.text(), self.ledata.text(), self.lestatus.text(), self.leidzadaci.text()]

        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into Отчеты( Nazvanie, Data, Status, ID_zadaci)
            values('{row[0]}','{row[1]}','{row[2]}','{row[3]}')""")
            self.conn.commit()
            cur.close()
        except Exception as r:
            print("Не смогли добавить запись")
            return r
        self.update()  # обращаемся к update чтобы сразу увидеть изменения в БД

    def delete_otcheti(self):
        id = self.ledelete.text()
        conn = sqlite3.connect('proizvodstvo.db')
        c = conn.cursor()
        c.execute("DELETE FROM Отчеты WHERE ID_otcheta=?", (id,))
        conn.commit()
        conn.close()
        self.update()

    def search_otcheti(self):
        column_name = self.cbfind.currentText()
        column_index = self.tableWidget.horizontalHeaderItem(self.tableWidget.currentColumn())
        search_text = self.lefind.text()
        query = f"select * from Отчеты where {column_name} like '%{search_text}%'"
        self.update(query)

    def update_otcheti(self):  # изменение
        # Открываем соединение с базой данных
        conn = sqlite3.connect('proizvodstvo.db')
        cursor = conn.cursor()

        Название = self.lenazvanie.text()
        Дата = self.ledata.text()
        Статус = self.lestatus.text()
        ID_Задачи =  self.leidzadaci.text()


        # Получаем ID из поля ввода
        ID_otcheta = self.lechange.text()

        # Обновляем запись в таблице
        try:
            cursor.execute(
                """UPDATE Отчеты SET Nazvanie=?, Data=?, Status=?, ID_zadaci=? WHERE ID_otcheta=?""",
                (Название, Дата, Статус, ID_Задачи, ID_otcheta))
            conn.commit()
        except Exception as e:
            print("Ошибка при обновлении записи в таблице:", e)
        finally:
            cursor.close()
            conn.close()

        # Обновляем данные в таблице на форме
        self.update()

    def show_Pz(self): # Показать таблицу Пользователи
        self.SH_pz = Пользователи()
        self.SH_pz.show()


POISKPO = ['ID_polzovatelya', 'Imya', 'Login', 'Parol', 'Email']
class Пользователи(QWidget, Ui_Пользователи):

    def __init__(self):
        super(Пользователи, self).__init__()
        self.setupUi(self)
        self.pbopen.clicked.connect(self.open_polzovateli)
        self.pbinsert.clicked.connect(self.insert_polzovateli)
        self.pbdelete.clicked.connect(self.delete_polzovateli)
        self.cbfind.addItems(POISKPO)
        self.pbfind.clicked.connect(self.search_polzovateli)
        self.pbchange.clicked.connect(self.update_polzovateli)

    def open_polzovateli(self):  # кнопка
        try:
            self.conn = sqlite3.connect('proizvodstvo.db')
            cur = self.conn.cursor()
            data = cur.execute("select * from Пользователи;")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print("Ошибки с подключением к БД")
            return e
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elen in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elen)))
        self.tableWidget.resizeColumnsToContents()

    def update(self, query="select * from Пользователи"):  # после добавление сразу видно запись
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as d:
            print(f"Проблемы с подкл {d}")
            return d
        self.tableWidget.setRowCount(0)  # обнулмяем все данные из таблцы
        # заносим по новой
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elen in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elen)))
        self.tableWidget.resizeColumnsToContents()

    def insert_polzovateli(self):  # кнопка добавить
        row = [self.leemail.text(), self.leimya.text(), self.lelogin.text(), self.leparol.text()]

        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into Пользователи( Email, Imya, Login, Parol)
               values('{row[0]}','{row[1]}','{row[2]}','{row[3]}')""")
            self.conn.commit()
            cur.close()
        except Exception as r:
            print("Не смогли добавить запись")
            return r
        self.update()  # обращаемся к update чтобы сразу увидеть изменения в БД

    def delete_polzovateli(self):
        id = self.ledelete.text()
        conn = sqlite3.connect('proizvodstvo.db')
        c = conn.cursor()
        c.execute("DELETE FROM Пользователи WHERE ID_polzovatelya=?", (id,))
        conn.commit()
        conn.close()
        self.update()

    def search_polzovateli(self):
        column_name = self.cbfind.currentText()
        column_index = self.tableWidget.horizontalHeaderItem(self.tableWidget.currentColumn())
        search_text = self.lefind.text()
        query = f"select * from Пользователи where {column_name} like '%{search_text}%'"
        self.update(query)

    def update_polzovateli(self):  # изменение
        # Открываем соединение с базой данных
        conn = sqlite3.connect('proizvodstvo.db')
        cursor = conn.cursor()

        Имя = self.leimya.text()
        Логин = self.lelogin.text()
        Пароль = self.leparol.text()
        Почта =  self.leemail.text()


        # Получаем ID из поля ввода
        ID_polzovatelya = self.lechange.text()

        # Обновляем запись в таблице
        try:
            cursor.execute(
                """UPDATE Пользователи SET Imya=?, Login=?, Parol=?, Email=? WHERE ID_polzovatelya=?""",
                (Имя, Логин, Пароль, Почта, ID_polzovatelya))
            conn.commit()
        except Exception as e:
            print("Ошибка при обновлении записи в таблице:", e)
        finally:
            cursor.close()
            conn.close()

        # Обновляем данные в таблице на форме
        self.update()



App = QtWidgets.QApplication([])
window = Login()
window.show()
App.exec()