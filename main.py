# import pyodbc
# import pandas as pd
# from sqlalchemy import create_engine
# import pymysql
# from turtledemo import paint
from copy import copy
from functools import partial

import pyodbc
import sys
# import os
from PyQt5.QtCore import Qt, QTime, QSize
# from bitarray import bitarray
# from console_commands import *

from PyQt5.QtWidgets import QWidget, QApplication, QStackedWidget, QPushButton, QTableWidget, QTableWidgetItem, \
    QStyledItemDelegate, QDialog, QLabel, QMainWindow, QInputDialog, QMessageBox, QComboBox, QCheckBox, \
    QAbstractScrollArea, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QLineEdit, QHeaderView
from PyQt5.uic import loadUi, pyuic
from PyQt5 import QtCore, QtGui

# from CheckableCombobox import CheckableComboBox
from TrainsManager import *
from RoutesManager import *
from TimetableManager import *

#
# class EditRouteDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         loadUi("edit_route_dialog.ui", self)
#         self.stationsToRoute_table

def connectToDB(driver, ser_name, db_name, username, passwd):
    return pyodbc.connect("""DRIVER={};
                        SERVER={};
                        DATABASE={};
                        UID={};
                        PWD={}""".format(driver, ser_name, db_name, username, passwd))


AUTHORIZED = False
USR_LOGIN = None


class EditRouteDialog(QDialog):
    def __init__(self, route_id, route_manager, db_cursor: pyodbc.Cursor, parent=None):
        super().__init__(parent)
        self._route_id = route_id
        self._routes_manager = route_manager
        loadUi("edit_route_dialog.ui", self)
        self._db_cursor = db_cursor
        self.add_station_btn.clicked.connect(lambda state, r_id=self._route_id:
                                             self._routes_manager.add_station_to_route(r_id))

    def fillStatinosBox(self):
        stations = self._db_cursor.execute("""SELECT station_id, station_name FROM stations
                                            ORDER BY station_name""").fetchall()
        for st_id, st_name in stations:
            self.all_stationsBox.addItem(st_name, userData=st_id)

    def fill_stations_table(self, curr_stations):
        self.stationsToRoute_table.setRowCount(0)
        self.stationsToRoute_table.setColumnCount(3)
        self.stationsToRoute_table.setHorizontalHeaderLabels([
            "П.п", "Название", ""])
        i = 0
        for r_to_st_id, st_name, sort_order in curr_stations:
            self.stationsToRoute_table.insertRow(i)
            sort_order = QTableWidgetItem(str(sort_order))
            sort_order.setFlags((sort_order.flags() | QtCore.Qt.CustomizeWindowHint) &
                                ~QtCore.Qt.ItemIsEditable)
            self.stationsToRoute_table.setItem(i, 0, sort_order)
            station_name = QTableWidgetItem(st_name)
            station_name.setFlags((station_name.flags() | QtCore.Qt.CustomizeWindowHint) &
                                  ~QtCore.Qt.ItemIsEditable)
            self.stationsToRoute_table.setItem(i, 1, station_name)
            remove_route_button = QPushButton(text="Удалить", parent=self)
            remove_route_button.clicked.connect(lambda state, data=(r_to_st_id, self._route_id):
                                                self._routes_manager.delete_station_from_route(data))
            self.stationsToRoute_table.setCellWidget(i, 2, remove_route_button)
            i += 1


    #########################################
    ######################################
    ###################################
    ##############################

class EditTimetableDialog(QDialog):
    def __init__(self, db_cursor: pyodbc.Cursor, parent=None):
        super().__init__(parent)
        loadUi("editPassagesDialog.ui", self)
        self._db_cursor = db_cursor
        self.trains_comboBox.currentIndexChanged.connect(self.table_update)
        self.routes_comboBox.currentIndexChanged.connect(self.table_update)

        # self.add_station_btn.clicked.connect(lambda state, r_id=self._route_id:
        #                                      self._routes_manager.add_station_to_route(r_id))


    def table_update(self):
        route_id = self.routes_comboBox.itemData(self.routes_comboBox.currentIndex())
        train_id = self.trains_comboBox.itemData(self.trains_comboBox.currentIndex())

        passages = """SELECT * FROM passages p
                    INNER JOIN stations_to_routes str ON p.passage_first_station_to_route_id = str.id
                    WHERE str.route_id = ? AND p.train_id = ?"""

        self.passage_stations_tbl.setRowCount(0)
        self.passage_stations_tbl.setColumnCount(3)
        self.passage_stations_tbl.setHorizontalHeaderLabels([
            "Станция", "Время отправления", "Стоянка"])
        i = 0
        for r_to_st_id, st_name, sort_order in curr_stations:
            self.stationsToRoute_table.insertRow(i)
            sort_order = QTableWidgetItem(str(sort_order))
            sort_order.setFlags((sort_order.flags() | QtCore.Qt.CustomizeWindowHint) &
                                ~QtCore.Qt.ItemIsEditable)
            self.stationsToRoute_table.setItem(i, 0, sort_order)
            station_name = QTableWidgetItem(st_name)
            station_name.setFlags((station_name.flags() | QtCore.Qt.CustomizeWindowHint) &
                                  ~QtCore.Qt.ItemIsEditable)
            self.stationsToRoute_table.setItem(i, 1, station_name)
            remove_route_button = QPushButton(text="Удалить", parent=self)
            remove_route_button.clicked.connect(lambda state, data=(r_to_st_id, self._route_id):
                                                self._routes_manager.delete_station_from_route(data))
            self.stationsToRoute_table.setCellWidget(i, 2, remove_route_button)
            i += 1

    def fill_trains_box(self):
        trains = self._db_cursor.execute("""SELECT id, number FROM trains t
                                               ORDER BY number""").fetchall()
        for train_id, train_num in trains:
            self.trains_comboBox.addItem(train_num, userData=train_id)

    def fill_routes_box(self):
        routes = self._db_cursor.execute("""SELECT route_id, name FROM routes r
                                               ORDER BY name""").fetchall()
        for r_id, r_name in routes:
            self.routes_comboBox.addItem(r_name, userData=r_id)




    ##################################
    ##################################
    ##################################
    ##################################
    ##################################


class MainWindowUI(QWidget):

    class AddRouteDialog(QDialog):
        new_route_name: str
        new_route_number: str

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Добавление нового маршрута")
            self.main_layout = QVBoxLayout(self)
            self.number_line_layout = QHBoxLayout(self)
            self.number_line_layout.addWidget(QLabel("Введите номер маршрута: ", self))
            self.number_line_layout.addItem(QSpacerItem(10, 40, QSizePolicy.Fixed, QSizePolicy.Expanding))
            self.enter_number = QLineEdit(self)
            self.number_line_layout.addWidget(self.enter_number)

            self.name_line_layout = QHBoxLayout(self)
            self.name_line_layout.addWidget(QLabel("Введите название маршрута: ", self))
            self.name_line_layout.addItem(QSpacerItem(10, 40, QSizePolicy.Fixed, QSizePolicy.Expanding))
            self.enter_name = QLineEdit(self)
            self.name_line_layout.addWidget(self.enter_name)

            self.buttons_layout = QHBoxLayout(self)
            self.cancel_button = QPushButton("Отмена", self)
            self.apply_button = QPushButton("Добавить", self)

            self.buttons_layout.addItem(QSpacerItem(10, 50, QSizePolicy.Minimum, QSizePolicy.Fixed))
            self.buttons_layout.addWidget(self.apply_button)
            self.buttons_layout.addWidget(self.cancel_button)

            self.main_layout.addItem(self.number_line_layout)
            self.main_layout.addItem(self.name_line_layout)
            self.main_layout.addItem(self.buttons_layout)

            self.apply_button.clicked.connect(self.__apply_results)
            self.cancel_button.clicked.connect(self.__reject_results)

        def __apply_results(self):
            self.enter_name.setStyleSheet("background-color : #FFFFFF")
            self.enter_number.setStyleSheet("background-color : #FFFFFF")
            if len(self.enter_name.text().strip()) > 0 and len(self.enter_number.text().strip()) > 0:
                self.new_route_name = self.enter_name.text()
                self.new_route_number = self.enter_number.text()
                return self.accept()
            else:
                if len(self.enter_name.text().strip()) == 0:
                    self.enter_name.setStyleSheet("background-color : #FFcccc")
                if len(self.enter_number.text().strip()) == 0:
                    self.enter_number.setStyleSheet("background-color : #FFCCCC")

        def __reject_results(self):
            return self.reject()

    class AddTrainDialog(QDialog):
        new_train_number: str

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Добавление нового поезда")
            self.main_layout = QVBoxLayout(self)
            self.number_line_layout = QHBoxLayout(self)
            self.number_line_layout.addWidget(QLabel("Введите номер поезда: ", self))
            self.number_line_layout.addItem(QSpacerItem(10, 40, QSizePolicy.Fixed, QSizePolicy.Expanding))
            self.enter_number = QLineEdit(self)
            self.number_line_layout.addWidget(self.enter_number)


            self.buttons_layout = QHBoxLayout(self)
            self.cancel_button = QPushButton("Отмена", self)
            self.apply_button = QPushButton("Добавить", self)

            self.buttons_layout.addItem(QSpacerItem(10, 50, QSizePolicy.Minimum, QSizePolicy.Fixed))
            self.buttons_layout.addWidget(self.apply_button)
            self.buttons_layout.addWidget(self.cancel_button)

            self.main_layout.addItem(self.number_line_layout)
            self.main_layout.addItem(self.buttons_layout)

            self.apply_button.clicked.connect(self.__apply_results)
            self.cancel_button.clicked.connect(self.__reject_results)

        def __apply_results(self):
            self.enter_number.setStyleSheet("background-color : #FFFFFF")
            if len(self.enter_number.text().strip()) > 0:
                self.new_train_number = self.enter_number.text()
                return self.accept()
            else:
                if len(self.enter_number.text().strip()) == 0:
                    self.enter_number.setStyleSheet("background-color : #FFCCCC")

        def __reject_results(self):
            return self.reject()

    def __init__(self):
        super(MainWindowUI, self).__init__()
        loadUi("menu.ui", self)
        self.stackedWidget.setCurrentIndex(0)
        self.icon_btns.setIconSize(QSize(16, 16))
        self.authorization_menu_btn.clicked.connect(self.open_authorization_page)
        # self.delRoutebtn.clicked.connect(self.del_selected_route)
        self.registration_menu_btn.clicked.connect(self.open_registration_page)
        self.buy_tickets_menu_btn.clicked.connect(self.open_ticket_purchase_page)
        # self.apply_rt_changes_btn.clicked.connect(self.apply_routesDB_changes)
        self.edit_routes_menu_btn.clicked.connect(self.open_routes_managment_page)
        self.edit_trains_menu_btn.clicked.connect(self.open_trains_managment_page)
        self.edit_timetable_menu_btn.clicked.connect(self.open_timetable_managment_page)

        # self.add_routes_btn.clicked.connect(self.add_new_route)
        # self.update_routesForm.clicked.connect(self.update_routes_form)
        self.__main_app: ApplicationBack = None
        self.back_button_on_routePage.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.back_button_on_timetable_Page.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.back_button_on_trains_Page.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.back_button_on_routePage.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        ##########################
        #TODO PAGE : Route Managment
        ##########################

    def init2(self, mainApp):
        self.__main_app = mainApp
        self.update_routesForm.clicked.connect(self.__main_app.route_manager.update_routes)
        self.add_routes_btn.clicked.connect(self.__add_route)
        self.add_new_train_btn.clicked.connect(self.__add_train)
        self.update_trains_table_btn.clicked.connect(self.__main_app.trains_manager.update_trains_table)

    #########################################
    ######################################
    #TODO СТАРТОВАЯ СТРАНИЦА
    ###################################

    @QtCore.pyqtSlot()
    def open_routes_managment_page(self):
        self.stackedWidget.setCurrentIndex(1)
        self.__main_app.start_route_managment()

    @QtCore.pyqtSlot()
    def open_authorization_page(self):
        index = self.stackedWidget.indexOf(self.authorization_page)
        self.stackedWidget.setCurrentIndex(index)

    @QtCore.pyqtSlot()
    def open_registration_page(self):
        index = self.stackedWidget.indexOf(self.registration_page)
        self.stackedWidget.setCurrentIndex(index)
        pass

    @QtCore.pyqtSlot()
    def open_ticket_purchase_page(self):
        index = self.ui.stackedWidget.indexOf(self.buy_tickets_page)
        self.stackedWidget.setCurrentIndex(index)
        pass

    @QtCore.pyqtSlot()
    def open_trains_managment_page(self):
        index = self.stackedWidget.indexOf(self.trains_form)
        self.stackedWidget.setCurrentIndex(index)
        self.__main_app.start_trains_managment()

    @QtCore.pyqtSlot()
    def open_timetable_managment_page(self):
        index = self.stackedWidget.indexOf(self.timetable_form)
        self.stackedWidget.setCurrentIndex(index)
        self.__main_app.start_timetable_managment()

    #########################################
    ######################################
    # СТРАНИЦА МАРШРУТОВ
    ###################################

    @QtCore.pyqtSlot()
    def fill_routeManagment_table(self, routes):
        self.routes_table.setRowCount(0)
        self.routes_table.setColumnCount(4)
        self.routes_table.setHorizontalHeaderLabels([
            "Номер", "Название", "", ""])
        header = self.routes_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setCascadingSectionResizes(True)
        header.setDefaultSectionSize(140)
        header.setHighlightSections(False)
        header.setMinimumSectionSize(100)
        header.setSortIndicatorShown(False)
        header.setStretchLastSection(False)
        i = 0
        for route_id, name, num in routes:
            self.routes_table.insertRow(i)
            self.routes_table.setItem(i, 0, QTableWidgetItem(name))
            self.routes_table.setItem(i, 1, QTableWidgetItem(str(num)))
            edit_route_button = QPushButton(text="Ред.", parent=self)
            edit_route_button.clicked.connect(
                lambda state, r_id=route_id: self.__main_app.route_manager.open_edit_route_Dialog(r_id))

            remove_route_button = QPushButton(text="Удалить", parent=self)
            remove_route_button.clicked.connect(
                lambda state, r_id=route_id: self.__main_app.route_manager.delete_route(r_id))

            # edit_route_passages_button = QPushButton(text="Рейсы", parent=self)
            # edit_route_passages_button.clicked.connect(
            #     lambda state, r_id=route_id: self.__main_app.route_manager.start_timetable_manager(r_id))

            self.routes_table.setCellWidget(i, 2, edit_route_button)
            self.routes_table.setCellWidget(i, 3, remove_route_button)
            # self.routes_table.setCellWidget(i, 4, edit_route_passages_button)

            i += 1

    @QtCore.pyqtSlot()
    def __add_route(self):  # TODO: Перенести в BackEnd
        addRoute_dialog = self.AddRouteDialog(self)
        if addRoute_dialog.exec_():
            new_name: str = addRoute_dialog.new_route_name
            new_number: str = addRoute_dialog.new_route_number
            try:
                cursor.execute("""INSERT INTO routes (name, number) VALUES (?,?)""", new_name, new_number)
                cursor.commit()
            except pyodbc.Error as exc:
                cursor.rollback()
                return
            self.__main_app.route_manager.update_routes()
        else:
            print("...Ничего не делаем")    # TODO


    #########################################
    ######################################
    #TODO СТРАНИЦА РЕЙСОВ
    ###################################\

    def fill_admin_timetable(self, passages):  # passage_number, train_number
        self.admin_timetable.setRowCount(0)
        self.admin_timetable.setColumnCount(5)
        self.admin_timetable.setHorizontalHeaderLabels([  # TODO Добавить время в пути и общее кол-во станций
            "Поезд №", "Маршрут", "", ""])
        header = self.admin_timetable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setCascadingSectionResizes(True)
        header.setDefaultSectionSize(140)
        header.setHighlightSections(False)
        header.setMinimumSectionSize(100)
        header.setSortIndicatorShown(False)
        header.setStretchLastSection(False)
        i = 0
        for passage_number, train_num in passages:
            self.admin_timetable.insertRow(i)
            self.admin_timetable.setItem(i, 0, QTableWidgetItem(str(passage_number)))
            self.admin_timetable.setItem(i, 1, QTableWidgetItem(str(train_num)))
            edit_passage_button = QPushButton(text="Ред.", parent=self)
            edit_passage_button.clicked.connect(
                lambda state, pass_num=passage_number: self.__main_app.route_manager.
                    timetable_manager.open_pass_editor(pass_num))

            remove_passage_button = QPushButton(text="Удалить", parent=self)
            remove_passage_button.clicked.connect(
                lambda state, pass_num=passage_number: self.__main_app.route_manager.
                    timetable_manager.delete_passage(pass_num))

            self.admin_timetable.setCellWidget(i, 2, edit_passage_button)
            self.admin_timetable.setCellWidget(i, 3, remove_passage_button)
            i += 1


    #########################################
    ######################################
    #TODO СТРАНИЦА ПОЕЗДОВ
    ###################################\

    @QtCore.pyqtSlot()
    def __add_train(self):  # TODO: Перенести в BackEnd
        add_train_dialog = self.AddTrainDialog(self)
        ok = False
        while not ok:
            if add_train_dialog.exec_():
                new_number: str = add_train_dialog.new_train_number
                try:
                    amount = cursor.execute("""SELECT COUNT(*) cnt FROM trains
                                    WHERE number = ?""",new_number).fetchone()[0]
                    if amount > 0:
                        QMessageBox.warning(self, "You can't add that Train!",
                                         "Train already exists!")
                        continue
                    cursor.execute("""INSERT INTO trains (number) VALUES (?)""", new_number)
                    cursor.commit()
                    ok = True
                except pyodbc.Error as exc:
                    cursor.rollback()
                    return
                self.__main_app.trains_manager.update_trains_table()
            else:
                print("...Ничего не делаем")    # TODO
                return

    def fill_trainsManagment_table(self, trains):
        self.trains_table.setRowCount(0)
        self.trains_table.setColumnCount(3)
        self.trains_table.setHorizontalHeaderLabels([
            "Номер", "",""])
        header = self.trains_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setCascadingSectionResizes(True)
        header.setDefaultSectionSize(140)
        header.setHighlightSections(False)
        header.setMinimumSectionSize(100)
        header.setSortIndicatorShown(False)
        header.setStretchLastSection(False)
        # self.trains_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.trains_table.resizeColumnsToContents()
        i = 0
        for train_id, number in trains:
            self.trains_table.insertRow(i)
            self.trains_table.setItem(i, 0, QTableWidgetItem(number))
            # self.trains_table.setItem(i, 1, QTableWidgetItem(str(num)))
            edit_train_button = QPushButton(text="Ред.", parent=self)
            edit_train_button.clicked.connect(
                lambda state, train_id=train_id: self.__main_app.trains_manager.open_edit_train_Dialog(train_id))

            remove_train_button = QPushButton(text="Удалить", parent=self)
            remove_train_button.clicked.connect(
                lambda state, train_id=train_id: self.__main_app.trains_manager.delete_train(train_id))

            # edit_route_passages_button = QPushButton(text="Рейсы", parent=self)
            # edit_route_passages_button.clicked.connect(
            #     lambda state, r_id=route_id: self.__main_app.route_manager.start_timetable_manager(r_id))

            self.trains_table.setCellWidget(i, 1, edit_train_button)
            self.trains_table.setCellWidget(i, 2, remove_train_button)
            # self.trains_table.setCellWidget(i, 4, edit_route_passages_button)
            i += 1

    #########################################
    ######################################
    # TODO СТРАНИЦА РЕДАКТИРОВАНИЯ РАСПИСАНИЯ
    ###################################\


    @QtCore.pyqtSlot()
    def __add_passage(self):  # TODO: Перенести в BackEnd
        add_train_dialog = self.AddTrainDialog(self)
        ok = False
        while not ok:
            if add_train_dialog.exec_():
                new_number: str = add_train_dialog.new_train_number
                try:
                    amount = cursor.execute("""SELECT COUNT(*) cnt FROM trains
                                    WHERE number = ?""",new_number).fetchone()[0]
                    if amount > 0:
                        QMessageBox.warning(self, "You can't add that Train!",
                                         "Train already exists!")
                        continue
                    cursor.execute("""INSERT INTO trains (number) VALUES (?)""", new_number)
                    cursor.commit()
                    ok = True
                except pyodbc.Error as exc:
                    cursor.rollback()
                    return
                self.__main_app.trains_manager.update_admin_timetable()
            else:
                print("...Ничего не делаем")    # TODO
                return

    def fill_TimetableManagment_table(self, passages):
        self.admin_timetable.setRowCount(0)
        self.admin_timetable.setColumnCount(4)
        self.admin_timetable.setHorizontalHeaderLabels([
            "Поезд", "Маршрут","",""])
        header = self.admin_timetable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setCascadingSectionResizes(True)
        header.setDefaultSectionSize(140)
        header.setHighlightSections(False)
        header.setMinimumSectionSize(100)
        header.setSortIndicatorShown(False)
        header.setStretchLastSection(False)

        i = 0
        for train_id, route_id, train_name, route_name in passages:
            self.admin_timetable.insertRow(i)
            self.admin_timetable.setItem(i, 0, QTableWidgetItem(train_name))
            edit_passage_button = QPushButton(text="Ред.", parent=self)
            edit_passage_button.clicked.connect(
                lambda state, t_id=train_id, r_id=route_id:
                    self.__main_app.timetable_manager.open_edit_passage_Dialog(t_id,r_id))

            remove_passage_button = QPushButton(text="Удалить", parent=self)
            remove_passage_button.clicked.connect(
                lambda state, t_id=train_id, r_id=route_id:
                self.__main_app.timetable_manager.delete_passage(t_id, r_id))

            self.admin_timetable.setCellWidget(i, 1, edit_passage_button)
            self.admin_timetable.setCellWidget(i, 2, remove_passage_button)
            # self.admin_timetable.setCellWidget(i, 4, edit_route_passages_button)
            i += 1



class ApplicationBack():
    def __init__(self, user_interface: MainWindowUI):
        self._ui = user_interface  # MAIN APPLICATION INTERFACE
        self._ui.__main_app = self
        self.route_manager = Routes_Manager(self._ui, cursor, self)
        self.trains_manager = Trains_Manager(self._ui, cursor, self)
        self.timetable_manager = TimetableManager(self._ui, cursor, self)
        self._ui.init2(self)

    def start_route_managment(self):
        self.route_manager.update_routes()

    def start_trains_managment(self):
        self.trains_manager.update_trains_table()

    def start_timetable_managment(self):
        self.timetable_manager.update_timetable_table()

if __name__ == "__main__":
    # os.system('python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py')
    ########################################
    # Initialize connection to DB
    ##########################################
    # driver = "ODBC Driver 17 for SQL Server"
    driver = "MySQL ODBC 8.0 Unicode Driver"
    server_name = "localhost"
    database = "kursach"
    username = "root"
    passwd = "Qwerty123!"

    new_conn = connectToDB(driver, server_name, database, username, passwd)
    cursor = new_conn.cursor()

    # q = """SELECT day_of_week FROM timetable LIMIT 1"""
    # data = cursor.execute(q).fetchone()[0]
    # print(data)

    # query = """INSERT INTO timetable (route_id,sort_order, station_id, arrival_time, delay)
    #             VALUES (?,?, TIME(?), ?)"""
    # cursor.execute(query,15,11,10,'10:22',23)
    # cursor.commit()
    ############################################
    # Start QT Applocation
    #############################################
    app = QApplication(sys.argv)
    main_window = MainWindowUI()
    mainApp = ApplicationBack(main_window)
    main_window.show()
    sys.exit(app.exec())
