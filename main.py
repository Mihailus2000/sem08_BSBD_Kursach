# import pyodbc
# import pandas as pd
# from sqlalchemy import create_engine
# import pymysql
from turtledemo import paint

import pyodbc
import sys

# from console_commands import *

from PyQt5.QtWidgets import QWidget, QApplication, QStackedWidget, QPushButton, QTableWidget, QTableWidgetItem, \
    QStyledItemDelegate, QDialog, QLabel, QMainWindow, QInputDialog
# import PyQt5.QtGui
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui


def connectToDB(driver, ser_name, db_name, username, passwd):
    return pyodbc.connect("""DRIVER={};
                        SERVER={};
                        DATABASE={};
                        UID={};
                        PWD={}""".format(driver, ser_name, db_name, username, passwd))


AUTHORIZED = False
USR_LOGIN = None


# if __name__ == '__main__':
#     # driver = "ODBC Driver 17 for SQL Server"
#     driver = "MySQL ODBC 8.0 Unicode Driver"
#     server_name = "localhost"
#     database = "tickets_on_train"
#     username = "root"
#     passwd = "Qwerty123!"
#     # %%
#     new_conn = connectToDB(driver, server_name, database, username, passwd)
#     cursor = new_conn.cursor()
#     db_connection_str = 'mysql+pymysql://root:Qwerty123!@localhost/tickets_on_train'
#     db_connection = create_engine(db_connection_str)
#     pd.set_option('display.max_rows',100)
#     pd.set_option('display.max_columns',None)
#     pd.options.display.width = None
#     pd.set_option('display.max_colwidth', None)
#
#     tables_list = cursor.execute("SHOW TABLES;").fetchall()
#     cursor.commit()
#     all_tables_list = []
#     for tbl in tables_list:
#         all_tables_list.append(tbl[0])
#
#     display_all_tables(db_connection, all_tables_list, cursor)
#     simple_parser(all_tables_list, db_connection, cursor)
class dialogWinNewRoute(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setParent(parent)
        self.push = QLabel("TEST")
        loadUi("dialogAddNewRoute.ui", self)
        self.show()
        # self.setupUi(self)



class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("menu.ui", self)
        self.stackedWidget.setCurrentIndex(1)
        self.authorization_menu_btn.clicked.connect(self.start_authorization)
        self.registration_menu_btn.clicked.connect(self.start_registration)
        self.buy_tickets_menu_btn.clicked.connect(self.start_buying)
        self.apply_rt_changes_btn.clicked.connect(self.apply_routesDB_changes)
        self.add_routes_btn.clicked.connect(self.add_new_route)
        self.start_value = None
        self.changedValue = None
        self.is_doubleClicked = False
        self.is_changedItem = False
        self.items_to_update = []

    def start_authorization(self):
        index = self.stackedWidget.indexOf(self.authorization_page)
        self.stackedWidget.setCurrentIndex(index)
        pass

    def start_registration(self):
        index = self.stackedWidget.indexOf(self.registration_page)
        self.stackedWidget.setCurrentIndex(index)
        pass

    def start_buying(self):
        index = self.stackedWidget.indexOf(self.buy_tickets_page)
        self.stackedWidget.setCurrentIndex(index)
        pass

    def apply_routesDB_changes(self):
        for rt_id, changed_field in self.items_to_update:
            rtDB_update_query = """UPDATE routes SET train_name = ? WHERE route_id = ?"""
            cursor.execute(rtDB_update_query,changed_field,int(rt_id))
        self.items_to_update.clear()
        cursor.commit()
        self.routes_DB.blockSignals(True)
        self.route_managment()
        self.routes_DB.blockSignals(False)

    def add_new_route(self):
        # self.dialog_window_addnewRoute = QDialog()
        self.ui = dialogWinNewRoute(self)
        x, y = QInputDialog.getText(self, 'input','entername')
        self.ui.setModal(True)
        self.ui.show()
        self.ui.open()
        self.ui.exec()


        # TODO

    def route_managment(self):
        index = self.stackedWidget.indexOf(self.page)
        self.stackedWidget.setCurrentIndex(index)
        self.routes_DB.setHorizontalHeaderLabels(["ID","№ мар-та","Название","Отправляется из","Время отправления","Прибывает на","Время прибытия"])

        #####################################
        # load all routes from DB
        #####################################
        query1 = """SELECT routes.route_id, train_name, routes.number
                    FROM routes
                    JOIN timetable on routes.route_id = timetable.route_id
                    JOIN stations s on timetable.station_id = s.station_id
                    GROUP BY routes.route_id;"""
        all_routes = cursor.execute(query1).fetchall()
        routes_dict = {}

        print("Finded routes:")  # TODO: DEBUG
        for (r_id, name, number) in all_routes:
            routes_dict[r_id] = [name, number]
            print("\t[{}] : {{{},{}}}".format(r_id, name, number))  # TODO: DEBUG

        routes_stations = {}
        query2 = """SELECT timetable.day_of_week, timetable.sort_order, stations.station_name, 
                    TIME_FORMAT(timetable.arrival_time, '%H:%i'), timetable.delay
                    FROM timetable JOIN stations
                    ON timetable.station_id = stations.station_id
                    WHERE route_id = ? ORDER BY sort_order;"""

        print("Station in routes:")  # TODO: DEBUG
        for r_id in routes_dict.keys():
            route_stations = cursor.execute(query2, r_id).fetchall()
            stations = []
            for (d_o_w, sort_order, st_name, ar_time, delay) in route_stations:
                stations.append([st_name, d_o_w, sort_order, ar_time, delay])
                print("\t[{}] : {{num:{}, dow:{}, {}, {} min}}".format(sort_order, st_name, d_o_w, ar_time, delay))  # TODO: DEBUG
            routes_stations[r_id] = stations
            print("\t-------------")

        self.routes_DB.setRowCount(len(routes_dict))
        for num, route_id in enumerate(routes_dict.keys()):
            ######
            rt_id = QTableWidgetItem(str(route_id))
            rt_id.setFlags((rt_id.flags() | QtCore.Qt.CustomizeWindowHint) & ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
            self.routes_DB.setItem(num, 0, rt_id)
            ######
            rt_number = QTableWidgetItem(routes_dict[route_id][1])
            rt_number.setFlags((rt_number.flags() | QtCore.Qt.CustomizeWindowHint) & ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
            self.routes_DB.setItem(num, 1, rt_number)
            ######
            rt_name = QTableWidgetItem(routes_dict[route_id][0])
            # print(rt_name.flags().__bool__())
            rt_name.setFlags((rt_name.flags() | QtCore.Qt.CustomizeWindowHint) | QtCore.Qt.ItemIsEditable)
            self.routes_DB.setItem(num, 2, rt_name)
            ######
            start_station = QTableWidgetItem(routes_stations[route_id][0][0])
            start_station.setFlags((start_station.flags() | QtCore.Qt.CustomizeWindowHint) & ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
            self.routes_DB.setItem(num, 3, start_station)
            ######
            start_time = QTableWidgetItem(routes_stations[route_id][0][3])
            start_time.setFlags((start_time.flags() | QtCore.Qt.CustomizeWindowHint) & ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
            self.routes_DB.setItem(num, 4, start_time)
            ######
            end_station = QTableWidgetItem(routes_stations[route_id][-1][0])
            end_station.setFlags((end_station.flags() | QtCore.Qt.CustomizeWindowHint) & ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
            self.routes_DB.setItem(num, 5, end_station)
            ######
            end_time = QTableWidgetItem(routes_stations[route_id][-1][3])
            end_time.setFlags((end_time.flags() | QtCore.Qt.CustomizeWindowHint) & ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
            self.routes_DB.setItem(num, 6, end_time)
            ######
        self.routes_DB.itemChanged.connect(self.changedTableItem)
        self.routes_DB.itemDoubleClicked.connect(self.doubleClicked)
        self.routes_DB.itemSelectionChanged.connect(self.changedTableSelectedItem)
        self.is_doubleClicked = False
        self.is_changedItem = False


        # TODO : ADD MOOOOORRRREEE

    def doubleClicked(self, item):
        self.start_value = item.text()
        self.is_doubleClicked = True
        row = item.row()
        col = item.column()
        print(item)

    def changedTableItem(self, item):
        row = item.row()
        col = item.column()
        item.tableWidget().blockSignals(True)
        el = item.setBackground (QtGui.QBrush(QtGui.QColor("#f00")))
        item.tableWidget().blockSignals(False)
        self.items_to_update.append([self.routes_DB.item(row,0).text(),item.text()])
        # print(self.changedValue)
        self.is_changedItem = True

        # route_num = item.tableWidget().item(row,1).text()
        # query = """SELECT * FROM routes WHERE number = ?"""
        # res = cursor.execute(query,route_num).fetchall()
        # # for r in res:
        # #     print(res)

    def changedTableSelectedItem(self):
        if self.is_doubleClicked and self.is_changedItem:
            print("was: {}\nnow: {}".format(self.start_value,self.changedValue))
            # self.items_to_update.insert([])
            # upd_query = """UPDATE """
        self.is_changedItem = False
        self.is_doubleClicked = False

if __name__ == "__main__":
    ########################################
    # Initialize connection to DB
    ##########################################
    # driver = "ODBC Driver 17 for SQL Server"
    driver = "MySQL ODBC 8.0 Unicode Driver"
    server_name = "localhost"
    database = "tickets_on_train"
    username = "root"
    passwd = "Qwerty123!"
    # %%
    new_conn = connectToDB(driver, server_name, database, username, passwd)
    cursor = new_conn.cursor()

    ############################################
    # Start QT Applocation
    #############################################
    app = QApplication(sys.argv)
    mainwindow = Window()
    mainwindow.show()
    mainwindow.route_managment()
    sys.exit(app.exec())
