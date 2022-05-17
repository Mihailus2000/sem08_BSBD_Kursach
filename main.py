# import pyodbc
# import pandas as pd
# from sqlalchemy import create_engine
# import pymysql
# from turtledemo import paint
from copy import copy

import pyodbc
import sys
import os

from PyQt5.QtCore import Qt, QTime, QSize
from bitarray import bitarray

from dialogAddNewRoute import Ui_Dialog

# from console_commands import *

from PyQt5.QtWidgets import QWidget, QApplication, QStackedWidget, QPushButton, QTableWidget, QTableWidgetItem, \
    QStyledItemDelegate, QDialog, QLabel, QMainWindow, QInputDialog, QMessageBox, QComboBox, QCheckBox, \
    QAbstractScrollArea, QDialogButtonBox, QVBoxLayout
# import PyQt5.QtGui
from PyQt5.uic import loadUi, pyuic
from PyQt5 import QtCore, QtGui
# from CheckableCombobox import CheckableComboBox

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



class MyCheckBox(QCheckBox):
    def __init__( self, *args ):
        super(MyCheckBox, self).__init__(*args) # will fail if passing **kwargs
        self._readOnly = False

    def isReadOnly( self ):
        return self._readOnly

    def mousePressEvent( self, event ):
        if (self.isReadOnly() ):
            event.accept()
        else:
            super(MyCheckBox, self).mousePressEvent(event)

    def mouseMoveEvent( self, event ):
        if ( self.isReadOnly() ):
            event.accept()
        else:
            super(MyCheckBox, self).mouseMoveEvent(event)

    def mouseReleaseEvent( self, event ):
        if ( self.isReadOnly() ):
            event.accept()
        else:
            super(MyCheckBox, self).mouseReleaseEvent(event)


    # Handle event in which the widget has focus and the spacebar is pressed.
    def keyPressEvent( self, event ):
        if ( self.isReadOnly() ):
            event.accept()
        else:
            super(MyCheckBox, self).keyPressEvent(event)

    @QtCore.pyqtSlot(bool)
    def setReadOnly( self, state ):
        self._readOnly = state
    readOnly = QtCore.pyqtProperty(bool, isReadOnly, setReadOnly)


# class dialogWinEditRoute(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.route_is_added = False
#         self.days = None
#         self.new_tt_id = None
#         # self.setParent(parent)
#         # self.ui = Ui_Dialog()
#         # self.ui.setupUi(self)
#         self.parentWindow = parent
#         # self.push = QLabel("TEST")
#         loadUi("dialogAddNewRoute.ui", self)
#         self.show()
#         self.all_stations = []
#         self.add_station_btn.clicked.connect(self.addStationToRoute)
#         self.del_station_btn.clicked.connect(self.delStationFromRoute)
#         self.all_stationsBox.activated.connect(self.chooseStation)
#         self.time_setter.timeChanged.connect(self.chooseT0)
#         self.delay_setter.valueChanged.connect(self.delayChanged)
#         self.save_changes_btn.clicked.connect(self.save_changes)
#         self.cancel_changes_btn.clicked.connect(self.reject_all_changes)
#
#         self.monday_checkBox.stateChanged.connect(self.checkboxes_changed)
#         self.tuesday_checkBox.stateChanged.connect(self.checkboxes_changed)
#         self.wednesday_checkBox.stateChanged.connect(self.checkboxes_changed)
#         self.thirsday_checkBox.stateChanged.connect(self.checkboxes_changed)
#         self.friday_checkBox.stateChanged.connect(self.checkboxes_changed)
#         self.saturday_checkBox.stateChanged.connect(self.checkboxes_changed)
#         self.sunday_checkBox.stateChanged.connect(self.checkboxes_changed)
#
#
#         # self.day_of_weeks_choose.activated.connect(self.choose_dow)
#
#         self.add_route_btn.clicked.connect(self.insert_route_toDB)
#         self.route_num_input.editingFinished.connect(self.update_route_num)
#         self.train_name_input.editingFinished.connect(self.update_train_name)
#         self.sum_of_route_tbl.setColumnCount(11)
#         self.sum_of_route_tbl.setHorizontalHeaderLabels(["id","Станция", "Отправление", "Стоянка", "П","Вт","Ср","Чт","Пт","Сб","Вс"])
#         self.sum_of_route_tbl.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
#         self.sum_of_route_tbl.resizeColumnsToContents()
#         self.routeData = {"route_num": None, "train_name": None,
#                           "stations": list()}
#         self.available_stations_id = {}
#         self.getDBInfo()
#         self.new_station = [self.all_stationsBox.currentText(),
#                             self.all_stationsBox.currentData()]
#         self.new_start_time = [int(self.time_setter.time().toString("HH")), int(self.time_setter.time().toString("mm"))]
#         self.new_st_delay = self.delay_setter.value()
#         self.route_is_added = False
#         self.stations_menu.setEnabled(False)
#         self.add_station_btn.setEnabled(False)
#         self.del_station_btn.setEnabled(False)
#         self.route_id = None
#
#         # day_of_weeks = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]
#         # for i, dow in enumerate(day_of_weeks):
#         #     self.day_of_weeks_choose.addItem(dow)
#         #     self.day_of_weeks_choose.setItemChecked(i,False)
#         self.reset_station_menu()
#         # self.new_dow_arr = self.day_of_weeks_choose.getBooleanArray()
#         self.station_cnt = 1
#         self.just_close = False
#
#     def closeEvent(self, event: QtGui.QCloseEvent) -> None:
#         if self.just_close:
#             event.accept()
#         else:
#             if self.route_is_added:
#                 self.reject_all_changes()
#             else:
#                 event.accept()
#
#     def checkboxes_changed(self):
#         self.days = [
#             self.monday_checkBox.isChecked(),
#             self.tuesday_checkBox.isChecked(),
#             self.wednesday_checkBox.isChecked(),
#             self.thirsday_checkBox.isChecked(),
#             self.friday_checkBox.isChecked(),
#             self.saturday_checkBox.isChecked(),
#             self.sunday_checkBox.isChecked()
#         ]
#         if True not in self.days:
#             self.add_station_btn.setEnabled(False)
#         else:
#             self.add_station_btn.setEnabled(True)
#
#
#     def reject_all_changes(self):
#         if not self.route_is_added:
#             self.just_close = True
#             self.close()
#             return
#         q_mess_box = QMessageBox.question(self, "Route insertion procedure", "Are you sure to cancel all changes?")
#         if q_mess_box:
#             try:
#                 route_id = self.route_id
#                 query1 = """DELETE timetable_of_days
#                                             FROM timetable_of_days
#                                             JOIN timetable ON timetable_of_days.timetable_id = timetable.id
#                                             WHERE route_id = ?"""
#                 cursor.execute(query1, route_id)
#                 query2 = """DELETE FROM timetable WHERE route_id = ?"""
#                 cursor.execute(query2, route_id)
#                 query3 = """DELETE FROM routes
#                                             WHERE route_id = ?"""
#                 cursor.execute(query3, route_id)
#             except pyodbc.Error as exc:
#                 QMessageBox.critical(self, "Cancelling failed!",
#                                      "Can't delete route because of:\n{}".format(exc.args))
#             cursor.commit()
#             QMessageBox.information(self, "Route insertion procedure", "All changes were successfully Cancelled!")
#             self.parentWindow.update_routes_form()
#             self.just_close = True
#             self.close()
#             return
#         else:
#             self.save_changes()
#
#
#     def save_changes(self):
#         self.just_close = True
#         if not self.route_is_added:
#             self.close()
#             return
#         QMessageBox.information(self, "Route insertion procedure", "All changes were Saved!")
#         self.parentWindow.update_routes_form()
#         self.close()
#
#     def reset_station_menu(self):
#         self.all_stationsBox.clearEditText()
#         self.time_setter.setTime(QTime(0,0))
#         self.delay_setter.setValue(0)
#         self.monday_checkBox.setChecked(False),
#         self.tuesday_checkBox.setChecked(False),
#         self.wednesday_checkBox.setChecked(False),
#         self.thirsday_checkBox.setChecked(False),
#         self.friday_checkBox.setChecked(False),
#         self.saturday_checkBox.setChecked(False),
#         self.sunday_checkBox.setChecked(False)
#         self.add_station_btn.setEnabled(False)
#
#     def update_route_num(self):
#         print("WAS: {}".format(self.routeData["route_num"]))
#         self.routeData["route_num"] = self.route_num_input.text()
#         print("NOW: {}".format(self.routeData["route_num"]))
#
#     def update_train_name(self):
#         print("WAS: {}".format(self.routeData["train_name"]))
#         self.routeData["train_name"] = self.train_name_input.text()
#         print("WAS: {}".format(self.routeData["train_name"]))
#
#     def getDBInfo(self):
#         query = """SELECT stations.station_id, stations.station_name FROM
#                 stations ORDER BY station_name"""
#         stations = cursor.execute(query).fetchall()
#         # all_stations = []
#         print(stations)
#         for st_id, st_name in stations:
#             self.available_stations_id[st_name] = st_id
#             self.all_stationsBox.addItem(st_name, userData=st_id)
#             # all_stations.append(st_name)
#         ########
#
#     # def choose_dow(self, index):
#     #     self.new_dow = index
#     #     print("Day Of week : {}".format(index))
#
#     def delayChanged(self, value):
#         self.new_st_delay = value
#         print("value : {}".format(value))
#
#     def chooseT0(self, cur_time):
#         self.new_start_time = [int(cur_time.toString("HH")), int(cur_time.toString("mm"))]
#         print("time : {}".format(self.new_start_time))
#
#     def chooseStation(self, index):
#         name = self.all_stationsBox.currentText()
#         id = self.all_stationsBox.currentData()
#         self.new_station = [name, id]
#         print("[{}] : {}, {}".format(index, self.all_stationsBox.currentText(), self.all_stationsBox.currentData()))
#
#     def insert_route_toDB(self):
#         if self.routeData["route_num"] is not None and self.routeData["route_num"] is not None:
#             query0 = """SELECT COUNT(route_id) FROM routes WHERE number = ? """
#             cnt = cursor.execute(query0, self.routeData["route_num"]).fetchall()[0][0]
#             if cnt != 0:
#                 msg = QMessageBox.warning(self, "Can't add that route!", "The same route already exists!\n"
#                                                                          "Change the information.")
#                 return
#             try:
#                 query = """INSERT INTO routes (train_name,number) VALUES (?,?)"""
#                 cursor.execute(query, self.routeData["train_name"], self.routeData["route_num"])
#             except pyodbc.Error as exc:
#                 cursor.rollback()
#                 QMessageBox.critical(self, "Insertion failed!",
#                                      "Can't insert route because of:\n{}".format(exc.args))
#                 return
#             query2 = """SELECT route_id FROM routes WHERE train_name = ? AND number = ?"""
#             self.route_id = int(
#                 cursor.execute(query2, self.routeData["train_name"], self.routeData["route_num"]).fetchone()[0])
#             self.route_is_added = True
#             self.add_route_btn.setEnabled(False)
#             self.stations_menu.setEnabled(True)
#             self.add_station_btn.setEnabled(False)
#             self.del_station_btn.setEnabled(True)
#
#     def addStationToRoute(self):
#         ##########
#         # self.new_dow_arr = self.day_of_weeks_choose.getBooleanArray()
#         self.all_stations.append([self.new_station, self.new_start_time, self.new_st_delay, self.days])
#         print("After INSERTION: {}".format(self.all_stations))
#         self.sum_of_route_tbl.insertRow(self.sum_of_route_tbl.rowCount())
#         station = QTableWidgetItem(self.new_station[0])
#         time0 = QTableWidgetItem("{}:{}".format(self.new_start_time[0], self.new_start_time[1]))
#         delay = QTableWidgetItem(str(self.new_st_delay))
#         # days = [
#         #     self.monday_checkBox.isChecked(),
#         #     self.tuesday_checkBox.isChecked(),
#         #     self.wednesday_checkBox.isChecked(),
#         #     self.thirsday_checkBox.isChecked(),
#         #     self.friday_checkBox.isChecked(),
#         #     self.saturday_checkBox.isChecked(),
#         #     self.sunday_checkBox.isChecked()
#         # ]
#         # if True not in days:
#         #     QMessageBox.warning(self, "Station insertion", "Can't delete ROW from empty table!")
#
#
#         # days_of_week_where_add = self.new_dow_arr
#         # days_of_week_where_add_tbl = ""
#         # aa = ["22","21"]
#
#         # for day in days_of_week_where_add:
#         #     if day:
#         #         days_of_week_where_add_tbl += '1'
#         #     else:
#         #         days_of_week_where_add_tbl += '0'
#         # days_of_week_where_add_tbl =  QTableWidgetItem("{}".format(days_of_week_where_add))
#
#
#         # unreacheable_checkbox = QCheckBox()
#         # self.sum_of_route_tbl.setEditTriggers(QTableWidget.NoEditTriggers)
#
#         days_cbs = []
#         for day in self.days:
#             cb = MyCheckBox()
#             cb.setReadOnly(True)
#             if day:
#                 cb.setChecked(True)
#             else:
#                 cb.setChecked(False)
#             # cb.setStyleSheet("pointer-events: none")
#             days_cbs.append(cb)
#
#
#         # for i in range(7):
#         #     item = self.sum_of_route_tbl.item(self.sum_of_route_tbl.rowCount() - 1,3+i)
#         #     item.setFlags((item.flags() | QtCore.Qt.CustomizeWindowHint) &
#         #                ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
#
#         # chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
#         # days_of_week_where_add_tbl.setFlags((days_of_week_where_add_tbl.flags() | QtCore.Qt.CustomizeWindowHint) &
#         #              ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
#         # self.sum_of_route_tbl.setItem(self.sum_of_route_tbl.rowCount() - 1, 3, days_of_week_where_add_tbl)
#         ##########
#         ##########
#         # Update DB7
#         try:
#             query1 = """INSERT INTO timetable (route_id, sort_order, station_id, arrival_time, delay)
#                                 VALUES (?,?,?,TIME(?),?)"""  # TODO ДОДЕЛАТЬ! При удалении нужно менять sort_order!!
#             cursor.execute(query1, self.route_id, self.station_cnt, self.new_station[1], "{}".format(time0.text()),
#                            self.new_st_delay)
#             cursor.commit()
#             query2 = """SELECT id FROM timetable WHERE route_id = ? AND sort_order = ? AND station_id = ?
#                         AND arrival_time = ? AND delay = ?"""
#             self.new_tt_id = cursor.execute(query2, self.route_id, self.station_cnt, self.new_station[1],
#                                             "{}".format(time0.text()), self.new_st_delay).fetchall()[-1][0]
#
#             query3 = """INSERT INTO timetable_of_days (timetable_id, day_of_week)
#                                 VALUES (?,?)"""
#             for index, is_day_inserted in enumerate(self.days):
#                 if is_day_inserted:
#                     cursor.execute(query3, self.new_tt_id, index)
#
#         except pyodbc.Error as exc:
#             cursor.rollback()
#             QMessageBox.critical(self, "Insertion failed!",
#                                  "Exception raised because of:\n{}".format(exc.args))
#             return
#         cursor.commit()
#
#         id_in_tbl = QTableWidgetItem(str(self.new_tt_id))
#         id_in_tbl.setFlags((id_in_tbl.flags() | QtCore.Qt.CustomizeWindowHint) &
#                          ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
#         self.sum_of_route_tbl.setItem(self.sum_of_route_tbl.rowCount() - 1, 0, id_in_tbl)
#         ##########
#         station.setFlags((station.flags() | QtCore.Qt.CustomizeWindowHint) &
#                          ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
#         self.sum_of_route_tbl.setItem(self.sum_of_route_tbl.rowCount() - 1, 1, station)
#         ##########
#         station.setFlags((station.flags() | QtCore.Qt.CustomizeWindowHint) &
#                          ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
#         self.sum_of_route_tbl.setItem(self.sum_of_route_tbl.rowCount() - 1, 1, station)
#         ##########
#         time0.setFlags((time0.flags() | QtCore.Qt.CustomizeWindowHint) &
#                        ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
#         self.sum_of_route_tbl.setItem(self.sum_of_route_tbl.rowCount() - 1, 2, time0)
#         ##########
#         delay.setFlags((delay.flags() | QtCore.Qt.CustomizeWindowHint) &
#                        ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
#         self.sum_of_route_tbl.setItem(self.sum_of_route_tbl.rowCount() - 1, 3, delay)
#         ##########
#         self.sum_of_route_tbl.setCellWidget(self.sum_of_route_tbl.rowCount() - 1, 4, days_cbs[0])
#         self.sum_of_route_tbl.setCellWidget(self.sum_of_route_tbl.rowCount() - 1, 5, days_cbs[1])
#         self.sum_of_route_tbl.setCellWidget(self.sum_of_route_tbl.rowCount() - 1, 6, days_cbs[2])
#         self.sum_of_route_tbl.setCellWidget(self.sum_of_route_tbl.rowCount() - 1, 7, days_cbs[3])
#         self.sum_of_route_tbl.setCellWidget(self.sum_of_route_tbl.rowCount() - 1, 8, days_cbs[4])
#         self.sum_of_route_tbl.setCellWidget(self.sum_of_route_tbl.rowCount() - 1, 9, days_cbs[5])
#         self.sum_of_route_tbl.setCellWidget(self.sum_of_route_tbl.rowCount() - 1, 10, days_cbs[6])
#         self.sum_of_route_tbl.resizeColumnsToContents()
#
#         self.reset_station_menu()
#
#     def delStationFromRoute(self):
#         if self.sum_of_route_tbl.rowCount() == 0:
#             msg = QMessageBox.warning(self, "Deletion", "Can't delete ROW from empty table!")
#             return
#         row = self.sum_of_route_tbl.currentRow()
#         id = int(self.sum_of_route_tbl.item(row,0).text())
#         print("Will be deleted {} row. Id = {}\n".format(row, id))
#
#         # TODO: Change counts in DB:
#         try:
#             query1 = """DELETE timetable_of_days
#                         FROM timetable_of_days
#                         WHERE timetable_id = ?"""
#             cursor.execute(query1, id)
#             query2 = """DELETE FROM timetable WHERE id = ?"""
#             cursor.execute(query2, id)
#         except pyodbc.Error as exc:
#             cursor.rollback()
#             QMessageBox.critical(self, "Cancelling failed!",
#                                  "Can't delete route because of:\n{}\n"
#                                  "All actions were canceled!".format(exc.args))
#         cursor.commit()
#         self.sum_of_route_tbl.removeRow(row)
#         self.all_stations.pop(row)
#         print("After delition: {}".format(self.all_stations))

class dialogWinNewRoute(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.route_is_added = False
        self.days = None
        self.new_tt_id = None
        # self.setParent(parent)
        # self.ui = Ui_Dialog()
        # self.ui.setupUi(self)
        self.parentWindow = parent
        # self.push = QLabel("TEST")
        loadUi("dialogAddNewRoute.ui", self)
        self.show()
        self.all_stations = []
        self.add_station_btn.clicked.connect(self.addStationToRoute)
        self.del_station_btn.clicked.connect(self.delStationFromRoute)
        self.all_stationsBox.activated.connect(self.chooseStation)
        self.time_setter.timeChanged.connect(self.chooseT0)
        self.delay_setter.valueChanged.connect(self.delayChanged)
        self.save_changes_btn.clicked.connect(self.save_changes)
        self.cancel_changes_btn.clicked.connect(self.reject_all_changes)

        self.monday_checkBox.stateChanged.connect(self.checkboxes_changed)
        self.tuesday_checkBox.stateChanged.connect(self.checkboxes_changed)
        self.wednesday_checkBox.stateChanged.connect(self.checkboxes_changed)
        self.thirsday_checkBox.stateChanged.connect(self.checkboxes_changed)
        self.friday_checkBox.stateChanged.connect(self.checkboxes_changed)
        self.saturday_checkBox.stateChanged.connect(self.checkboxes_changed)
        self.sunday_checkBox.stateChanged.connect(self.checkboxes_changed)


        # self.day_of_weeks_choose.activated.connect(self.choose_dow)

        self.add_route_btn.clicked.connect(self.insert_route_toDB)
        self.route_num_input.editingFinished.connect(self.update_route_num)
        self.train_name_input.editingFinished.connect(self.update_train_name)
        self.sum_of_route_tbl.setColumnCount(11)
        self.sum_of_route_tbl.setHorizontalHeaderLabels(["id","Станция", "Отправление", "Стоянка", "П","Вт","Ср","Чт","Пт","Сб","Вс"])
        self.sum_of_route_tbl.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.sum_of_route_tbl.resizeColumnsToContents()
        self.routeData = {"route_num": None, "train_name": None,
                          "stations": list()}
        self.available_stations_id = {}
        self.getDBInfo()
        self.new_station = [self.all_stationsBox.currentText(),
                            self.all_stationsBox.currentData()]
        self.new_start_time = [int(self.time_setter.time().toString("HH")), int(self.time_setter.time().toString("mm"))]
        self.new_st_delay = self.delay_setter.value()
        self.route_is_added = False
        self.stations_menu.setEnabled(False)
        self.add_station_btn.setEnabled(False)
        self.del_station_btn.setEnabled(False)
        self.route_id = None

        # day_of_weeks = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]
        # for i, dow in enumerate(day_of_weeks):
        #     self.day_of_weeks_choose.addItem(dow)
        #     self.day_of_weeks_choose.setItemChecked(i,False)
        self.reset_station_menu()
        # self.new_dow_arr = self.day_of_weeks_choose.getBooleanArray()
        self.station_cnt = 1
        self.just_close = False

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.just_close:
            event.accept()
        else:
            if self.route_is_added:
                self.reject_all_changes()
            else:
                event.accept()

    def checkboxes_changed(self):
        self.days = [
            self.monday_checkBox.isChecked(),
            self.tuesday_checkBox.isChecked(),
            self.wednesday_checkBox.isChecked(),
            self.thirsday_checkBox.isChecked(),
            self.friday_checkBox.isChecked(),
            self.saturday_checkBox.isChecked(),
            self.sunday_checkBox.isChecked()
        ]
        if True not in self.days:
            self.add_station_btn.setEnabled(False)
        else:
            self.add_station_btn.setEnabled(True)


    def reject_all_changes(self):
        if not self.route_is_added:
            self.just_close = True
            self.close()
            return
        q_mess_box = QMessageBox.question(self, "Route insertion procedure", "Are you sure to cancel all changes?")
        if q_mess_box:
            try:
                route_id = self.route_id
                query1 = """DELETE timetable_of_days
                                            FROM timetable_of_days
                                            JOIN timetable ON timetable_of_days.timetable_id = timetable.id
                                            WHERE route_id = ?"""
                cursor.execute(query1, route_id)
                query2 = """DELETE FROM timetable WHERE route_id = ?"""
                cursor.execute(query2, route_id)
                query3 = """DELETE FROM routes
                                            WHERE route_id = ?"""
                cursor.execute(query3, route_id)
            except pyodbc.Error as exc:
                cursor.rollback()
                QMessageBox.critical(self, "Cancelling failed!",
                                     "Can't delete route because of:\n{}".format(exc.args))
                return
            cursor.commit()
            QMessageBox.information(self, "Route insertion procedure", "All changes were successfully Cancelled!")
            self.parentWindow.update_routes_form()
            self.just_close = True
            self.close()
            return
        else:
            self.save_changes()


    def save_changes(self):
        self.just_close = True
        if not self.route_is_added:
            self.close()
            return
        QMessageBox.information(self, "Route insertion procedure", "All changes were Saved!")
        self.parentWindow.update_routes_form()
        self.close()

    def reset_station_menu(self):
        self.all_stationsBox.clearEditText()
        self.time_setter.setTime(QTime(0,0))
        self.delay_setter.setValue(0)
        self.monday_checkBox.setChecked(False),
        self.tuesday_checkBox.setChecked(False),
        self.wednesday_checkBox.setChecked(False),
        self.thirsday_checkBox.setChecked(False),
        self.friday_checkBox.setChecked(False),
        self.saturday_checkBox.setChecked(False),
        self.sunday_checkBox.setChecked(False)
        self.add_station_btn.setEnabled(False)

    def update_route_num(self):
        print("WAS: {}".format(self.routeData["route_num"]))
        self.routeData["route_num"] = self.route_num_input.text()
        print("NOW: {}".format(self.routeData["route_num"]))

    def update_train_name(self):
        print("WAS: {}".format(self.routeData["train_name"]))
        self.routeData["train_name"] = self.train_name_input.text()
        print("WAS: {}".format(self.routeData["train_name"]))

    def getDBInfo(self):
        query = """SELECT stations.station_id, stations.station_name FROM
                stations ORDER BY station_name"""
        stations = cursor.execute(query).fetchall()
        # all_stations = []
        print(stations)
        for st_id, st_name in stations:
            self.available_stations_id[st_name] = st_id
            self.all_stationsBox.addItem(st_name, userData=st_id)
            # all_stations.append(st_name)
        ########

    # def choose_dow(self, index):
    #     self.new_dow = index
    #     print("Day Of week : {}".format(index))

    def delayChanged(self, value):
        self.new_st_delay = value
        print("value : {}".format(value))

    def chooseT0(self, cur_time):
        self.new_start_time = [int(cur_time.toString("HH")), int(cur_time.toString("mm"))]
        print("time : {}".format(self.new_start_time))

    def chooseStation(self, index):
        name = self.all_stationsBox.currentText()
        id = self.all_stationsBox.currentData()
        self.new_station = [name, id]
        print("[{}] : {}, {}".format(index, self.all_stationsBox.currentText(), self.all_stationsBox.currentData()))

    def insert_route_toDB(self):
        if self.routeData["route_num"] is not None and self.routeData["route_num"] is not None:
            query0 = """SELECT COUNT(route_id) FROM routes WHERE number = ? """
            cnt = cursor.execute(query0, self.routeData["route_num"]).fetchall()[0][0]
            if cnt != 0:
                msg = QMessageBox.warning(self, "Can't add that route!", "The same route already exists!\n"
                                                                         "Change the information.")
                return
            try:
                query = """INSERT INTO routes (train_name,number) VALUES (?,?)"""
                cursor.execute(query, self.routeData["train_name"], self.routeData["route_num"])
            except pyodbc.Error as exc:
                cursor.rollback()
                QMessageBox.critical(self, "Insertion failed!",
                                     "Can't insert route because of:\n{}".format(exc.args))
                return
            query2 = """SELECT route_id FROM routes WHERE train_name = ? AND number = ?"""
            self.route_id = int(
                cursor.execute(query2, self.routeData["train_name"], self.routeData["route_num"]).fetchone()[0])
            self.route_is_added = True
            self.add_route_btn.setEnabled(False)
            self.stations_menu.setEnabled(True)
            self.add_station_btn.setEnabled(False)
            self.del_station_btn.setEnabled(True)

    def addStationToRoute(self):
        ##########
        # self.new_dow_arr = self.day_of_weeks_choose.getBooleanArray()
        self.all_stations.append([self.new_station, self.new_start_time, self.new_st_delay, self.days])
        print("After INSERTION: {}".format(self.all_stations))
        self.sum_of_route_tbl.insertRow(self.sum_of_route_tbl.rowCount())
        station = QTableWidgetItem(self.new_station[0])
        time0 = QTableWidgetItem("{}:{}".format(self.new_start_time[0], self.new_start_time[1]))
        delay = QTableWidgetItem(str(self.new_st_delay))
        # days = [
        #     self.monday_checkBox.isChecked(),
        #     self.tuesday_checkBox.isChecked(),
        #     self.wednesday_checkBox.isChecked(),
        #     self.thirsday_checkBox.isChecked(),
        #     self.friday_checkBox.isChecked(),
        #     self.saturday_checkBox.isChecked(),
        #     self.sunday_checkBox.isChecked()
        # ]
        # if True not in days:
        #     QMessageBox.warning(self, "Station insertion", "Can't delete ROW from empty table!")


        # days_of_week_where_add = self.new_dow_arr
        # days_of_week_where_add_tbl = ""
        # aa = ["22","21"]

        # for day in days_of_week_where_add:
        #     if day:
        #         days_of_week_where_add_tbl += '1'
        #     else:
        #         days_of_week_where_add_tbl += '0'
        # days_of_week_where_add_tbl =  QTableWidgetItem("{}".format(days_of_week_where_add))


        # unreacheable_checkbox = QCheckBox()
        # self.sum_of_route_tbl.setEditTriggers(QTableWidget.NoEditTriggers)

        days_cbs = []
        for day in self.days:
            cb = MyCheckBox()
            cb.setReadOnly(True)
            if day:
                cb.setChecked(True)
            else:
                cb.setChecked(False)
            # cb.setStyleSheet("pointer-events: none")
            days_cbs.append(cb)


        # for i in range(7):
        #     item = self.sum_of_route_tbl.item(self.sum_of_route_tbl.rowCount() - 1,3+i)
        #     item.setFlags((item.flags() | QtCore.Qt.CustomizeWindowHint) &
        #                ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)

        # chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        # days_of_week_where_add_tbl.setFlags((days_of_week_where_add_tbl.flags() | QtCore.Qt.CustomizeWindowHint) &
        #              ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
        # self.sum_of_route_tbl.setItem(self.sum_of_route_tbl.rowCount() - 1, 3, days_of_week_where_add_tbl)
        ##########
        ##########
        # Update DB7
        try:
            query1 = """INSERT INTO timetable (route_id, sort_order, station_id, arrival_time, delay)
                                VALUES (?,?,?,TIME(?),?)"""  # TODO ДОДЕЛАТЬ! При удалении нужно менять sort_order!!
            cursor.execute(query1, self.route_id, self.station_cnt, self.new_station[1], "{}".format(time0.text()),
                           self.new_st_delay)
            cursor.commit()
            query2 = """SELECT id FROM timetable WHERE route_id = ? AND sort_order = ? AND station_id = ?
                        AND arrival_time = ? AND delay = ?"""
            self.new_tt_id = cursor.execute(query2, self.route_id, self.station_cnt, self.new_station[1],
                                            "{}".format(time0.text()), self.new_st_delay).fetchall()[-1][0]

            query3 = """INSERT INTO timetable_of_days (timetable_id, day_of_week) 
                                VALUES (?,?)"""
            for index, is_day_inserted in enumerate(self.days):
                if is_day_inserted:
                    cursor.execute(query3, self.new_tt_id, index)

        except pyodbc.Error as exc:
            cursor.rollback()
            QMessageBox.critical(self, "Insertion failed!",
                                 "Exception raised because of:\n{}".format(exc.args))
            return
        cursor.commit()
        self.station_cnt += 1
        id_in_tbl = QTableWidgetItem(str(self.new_tt_id))
        id_in_tbl.setFlags((id_in_tbl.flags() | QtCore.Qt.CustomizeWindowHint) &
                         ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
        self.sum_of_route_tbl.setItem(self.sum_of_route_tbl.rowCount() - 1, 0, id_in_tbl)
        ##########
        station.setFlags((station.flags() | QtCore.Qt.CustomizeWindowHint) &
                         ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
        self.sum_of_route_tbl.setItem(self.sum_of_route_tbl.rowCount() - 1, 1, station)
        ##########
        station.setFlags((station.flags() | QtCore.Qt.CustomizeWindowHint) &
                         ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
        self.sum_of_route_tbl.setItem(self.sum_of_route_tbl.rowCount() - 1, 1, station)
        ##########
        time0.setFlags((time0.flags() | QtCore.Qt.CustomizeWindowHint) &
                       ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
        self.sum_of_route_tbl.setItem(self.sum_of_route_tbl.rowCount() - 1, 2, time0)
        ##########
        delay.setFlags((delay.flags() | QtCore.Qt.CustomizeWindowHint) &
                       ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
        self.sum_of_route_tbl.setItem(self.sum_of_route_tbl.rowCount() - 1, 3, delay)
        ##########
        self.sum_of_route_tbl.setCellWidget(self.sum_of_route_tbl.rowCount() - 1, 4, days_cbs[0])
        self.sum_of_route_tbl.setCellWidget(self.sum_of_route_tbl.rowCount() - 1, 5, days_cbs[1])
        self.sum_of_route_tbl.setCellWidget(self.sum_of_route_tbl.rowCount() - 1, 6, days_cbs[2])
        self.sum_of_route_tbl.setCellWidget(self.sum_of_route_tbl.rowCount() - 1, 7, days_cbs[3])
        self.sum_of_route_tbl.setCellWidget(self.sum_of_route_tbl.rowCount() - 1, 8, days_cbs[4])
        self.sum_of_route_tbl.setCellWidget(self.sum_of_route_tbl.rowCount() - 1, 9, days_cbs[5])
        self.sum_of_route_tbl.setCellWidget(self.sum_of_route_tbl.rowCount() - 1, 10, days_cbs[6])
        self.sum_of_route_tbl.resizeColumnsToContents()

        self.reset_station_menu()

    def delStationFromRoute(self):
        if self.sum_of_route_tbl.rowCount() == 0:
            msg = QMessageBox.warning(self, "Deletion", "Can't delete ROW from empty table!")
            return
        row = self.sum_of_route_tbl.currentRow()
        id = int(self.sum_of_route_tbl.item(row,0).text())
        print("Will be deleted {} row. Id = {}\n".format(row, id))

        # TODO: Change counts in DB:
        try:
            query0 = """SELECT sort_order FROM timetable
                        WHERE id = ?"""
            order = int(cursor.execute(query0, id).fetchone()[0])
            query1 = """DELETE timetable_of_days
                        FROM timetable_of_days
                        WHERE timetable_id = ?"""
            cursor.execute(query1, id)
            query2 = """DELETE FROM timetable WHERE id = ?"""
            cursor.execute(query2, id)

            query3 = """UPDATE timetable SET sort_order = sort_order - 1
                        WHERE route_id = ? AND sort_order > ?"""
            cursor.execute(query3, self.route_id, order)
        except pyodbc.Error as exc:
            cursor.rollback()
            QMessageBox.critical(self, "Cancelling failed!",
                                 "Can't delete station because of:\n{}\n"
                                 "All actions were canceled!".format(exc.args))
            return
        cursor.commit()
        self.station_cnt -= 1
        self.sum_of_route_tbl.removeRow(row)
        self.all_stations.pop(row)
        print("After delition: {}".format(self.all_stations))

class CustomDialog(QDialog):
    def __init__(self, parent=None, records=0):
        super().__init__(parent)
        self.setWindowTitle("Удаление маршрута(ов)")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        self.message = QLabel("Вы уверены, что хотите удалить {} записей из Расписания?".format(records))
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    # def reject(self) -> None:
    #     self.hide()

    def changeTo(self,new_text):
        self.message.setText(new_text)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.exec_()








class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("menu.ui", self)
        self.stackedWidget.setCurrentIndex(0)
        # btn = QPushButton()
        self.icon_btns.setIconSize(QSize(16, 16))
        # self.choose
        self.authorization_menu_btn.clicked.connect(self.start_authorization)
        self.delRoutebtn.clicked.connect(self.del_selected_route)
        self.registration_menu_btn.clicked.connect(self.start_registration)
        self.buy_tickets_menu_btn.clicked.connect(self.start_buying)
        self.apply_rt_changes_btn.clicked.connect(self.apply_routesDB_changes)
        self.edit_routes_menu_btn.clicked.connect(self.open_routes_editing)
        self.add_routes_btn.clicked.connect(self.add_new_route)
        self.update_routesForm.clicked.connect(self.update_routes_form)
        self.start_value = None
        self.changedValue = None
        self.is_doubleClicked = False
        self.is_changedItem = False
        self.items_to_update = []
        self.apply_rt_changes_btn.setEnabled(False)
        self.all_stations_id_to_name = {}

    def open_routes_editing(self):
        self.stackedWidget.setCurrentIndex(1)
        self.route_managment()

    def del_selected_route(self):
        selected_items = self.routes_DB.selectedItems()
        if len(selected_items) == 0:
            QMessageBox.warning(self, "Deletion", "You don't select anything to delete!")
            return
        selected_rows = set()
        for item in selected_items:
            selected_rows.add(item.row())
        all_records = 0
        all_route_ids = []
        for row in selected_rows:
            route_id = int(self.routes_DB.item(row,0).text())
            query0 = """SELECT COUNT(timetable_of_days.id) FROM timetable_of_days
                        JOIN timetable ON timetable_of_days.timetable_id = timetable.id
                        WHERE route_id = ?"""
            all_records += cursor.execute(query0,route_id).fetchone()[0]
            all_route_ids.append(route_id)
        msg = CustomDialog(self,all_records)
        if msg.exec_():
            try:
                for route_id in all_route_ids:
                    query1 = """DELETE timetable_of_days
                                FROM timetable_of_days
                                JOIN timetable ON timetable_of_days.timetable_id = timetable.id
                                WHERE route_id = ?"""
                    cursor.execute(query1, route_id)
                    query2 = """DELETE FROM timetable WHERE route_id = ?"""
                    cursor.execute(query2, route_id)
                    query3 = """DELETE FROM routes
                                WHERE route_id = ?"""
                    cursor.execute(query3, route_id)
            except pyodbc.Error as exc:
                QMessageBox.critical(self,"Deletion failed!","Can't delete route because of:\n{}".format(exc.args))
                return
            msg.changeTo("Всё OK! Записи успешно были удалены.")
            cursor.commit()
            self.update_routes_form()
        else:
            msg.changeTo("OK! Записи не были удалены.")

    def update_routes_form(self):
        self.routes_DB.blockSignals(True)
        self.route_managment()
        self.routes_DB.blockSignals(False)


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
        print("Items will be changed: {}".format(self.items_to_update))
        if len(self.items_to_update) == 0:
            msg = QMessageBox.warning(self, "Nothing to update!", "Nothing to update!")
            return
        for rt_id, changed_field in self.items_to_update:
            rtDB_update_query = """UPDATE routes SET train_name = ? WHERE route_id = ?"""
            cursor.execute(rtDB_update_query, changed_field, int(rt_id))
        self.items_to_update.clear()
        cursor.commit()
        self.routes_DB.blockSignals(True)
        self.route_managment()
        self.routes_DB.blockSignals(False)
        self.apply_rt_changes_btn.setEnabled(False)


    def add_new_route(self):
        # self.dialog_window_addnewRoute = QDialog()
        self.ui = dialogWinNewRoute(self)
        self.ui.setModal(True)
        # self.ui.show()
        self.ui.exec()

        # TODO

    def route_managment(self):
        self.routes_DB.clearContents()
        index = self.stackedWidget.indexOf(self.page)
        self.stackedWidget.setCurrentIndex(index)
        self.routes_DB.setColumnCount(7)
        self.routes_DB.setHorizontalHeaderLabels(
            ["ID", "№ мар-та", "Название", "Отправляется из", "Время отправления", "Прибывает на", "Время прибытия"])

        #####################################
        # load all routes from DB
        #####################################
        query1 = """SELECT routes.route_id, train_name, routes.number
                    FROM routes
                    LEFT JOIN timetable on routes.route_id = timetable.route_id
                    LEFT JOIN stations s on timetable.station_id = s.station_id
                    GROUP BY routes.route_id;"""
        all_routes = cursor.execute(query1).fetchall()
        routes_dict = {}

        print("Finded routes:")  # TODO: DEBUG
        for (r_id, name, number) in all_routes:
            routes_dict[r_id] = [name, number]
            print("\t[{}] : {{{},{}}}".format(r_id, name, number))  # TODO: DEBUG

        routes_stations = {}
        query2 = """SELECT timetable.sort_order, stations.station_name, 
                    TIME_FORMAT(timetable.arrival_time, '%H:%i'), timetable.delay
                    FROM timetable JOIN stations
                    ON timetable.station_id = stations.station_id
                    WHERE route_id = ? ORDER BY sort_order;"""

        print("Station in routes:")  # TODO: DEBUG
        for r_id in routes_dict.keys():
            route_stations = cursor.execute(query2, r_id).fetchall()
            stations = []
            if len(route_stations) == 0:
                stations.append([None, None, None, None])
                print("\tNO STATION in {}!".format(r_id))
            for (sort_order, st_name, ar_time, delay) in route_stations:
                stations.append([st_name, sort_order, ar_time, delay])
                print("\t[{}] : {{num:{}, {}, {} min}}".format(sort_order, st_name, ar_time,
                                                                       delay))  # TODO: DEBUG
            routes_stations[r_id] = stations
            print("\t-------------")

        self.routes_DB.setRowCount(len(routes_dict))
        for num, route_id in enumerate(routes_dict.keys()):
            ######
            rt_id = QTableWidgetItem(str(route_id))
            rt_id.setFlags((rt_id.flags() | QtCore.Qt.CustomizeWindowHint) &
                           ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
            self.routes_DB.setItem(num, 0, rt_id)
            ######
            rt_number = QTableWidgetItem(routes_dict[route_id][1])
            rt_number.setFlags((rt_number.flags() | QtCore.Qt.CustomizeWindowHint) &
                               ~QtCore.Qt.ItemIsEditable)
            self.routes_DB.setItem(num, 1, rt_number)
            ######
            rt_name = QTableWidgetItem(routes_dict[route_id][0])
            # print(rt_name.flags().__bool__())
            rt_name.setFlags((rt_name.flags() | QtCore.Qt.CustomizeWindowHint) | QtCore.Qt.ItemIsEditable)
            self.routes_DB.setItem(num, 2, rt_name)
            ######
            start_station = QTableWidgetItem(routes_stations[route_id][0][0])
            start_station.setFlags((start_station.flags() | QtCore.Qt.CustomizeWindowHint) &
                                   ~QtCore.Qt.ItemIsEditable)
            self.routes_DB.setItem(num, 3, start_station)
            ######
            start_time = QTableWidgetItem(routes_stations[route_id][0][2])
            start_time.setFlags((start_time.flags() | QtCore.Qt.CustomizeWindowHint) &
                                ~QtCore.Qt.ItemIsEditable)
            self.routes_DB.setItem(num, 4, start_time)
            ######
            end_station = QTableWidgetItem(routes_stations[route_id][-1][0])
            end_station.setFlags((end_station.flags() | QtCore.Qt.CustomizeWindowHint) &
                                 ~QtCore.Qt.ItemIsEditable)
            self.routes_DB.setItem(num, 5, end_station)
            ######
            end_time = QTableWidgetItem(routes_stations[route_id][-1][2])
            end_time.setFlags((end_time.flags() | QtCore.Qt.CustomizeWindowHint) &
                              ~QtCore.Qt.ItemIsEditable)
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

        row = item.row()
        col = item.column()
        if col == 2:
            self.is_doubleClicked = True
            print("Doubled: {}".format(item))

    def changedTableItem(self, item):
        row = item.row()
        col = item.column()
        item.tableWidget().blockSignals(True)
        item.setBackground(QtGui.QBrush(QtGui.QColor("#f00")))
        item.tableWidget().blockSignals(False)
        self.items_to_update.append([self.routes_DB.item(row, 0).text(), item.text()])
        self.apply_rt_changes_btn.setEnabled(True)

        # print(self.changedValue)
        self.is_changedItem = True

        # route_num = item.tableWidget().item(row,1).text()
        # query = """SELECT * FROM routes WHERE number = ?"""
        # res = cursor.execute(query,route_num).fetchall()
        # # for r in res:
        # #     print(res)

    def changedTableSelectedItem(self):
        if self.is_doubleClicked and self.is_changedItem:
            print("was: {}\nnow: {}".format(self.start_value, self.changedValue))
            # self.items_to_update.insert([])
            # upd_query = """UPDATE """
        self.is_changedItem = False
        self.is_doubleClicked = False

    def __get_stations(self):
        try:
            query = """SELECT stations.station_id, stations.station_name FROM
                           stations ORDER BY station_name"""
            stations = cursor.execute(query).fetchall()
        except pyodbc.Error as exc:
            QMessageBox.critical(self, "Station updation failed!","Can't get stations because of:\n{}".format(exc.args))
            return
        for st_id, st_name in stations:
            self.all_stations_id_to_name[st_id] = st_name

    # def displayRoutesForBuy(self, st_from_id, st_to_id, day_of_week):
    #     self.AllRoutesForBuy_tbl.setColumnCount()
    #     self.AllRoutesForBuy_tbl.setHorizontalHeaderLabels(
    #         ["Номер маршрута", "Поезд(название)", "Время отправления", "Время прибытия"])
    #     self.AllRoutesForBuy_tbl.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
    #     self.AllRoutesForBuy_tbl.resizeColumnsToContents()
    #     try:
    #         query = """SELECT route_id, timetable.id as timetable_id, station_id,sort_order,
    #                     arrival_time, delay FROM
    #                    timetable
    #                    right join
    #                     (SELECT f_st_routes, first_st_id, f_ord, second_st_id, sec_ord FROM(
    #                         (SELECT route_id f_st_routes, id first_st_id, sort_order f_ord FROM timetable
    #                         WHERE station_id = ?) first
    #                       inner join
    #                     (SELECT route_id s_st_routes,id second_st_id, sort_order sec_ord FROM timetable
    #                     WHERE station_id=?)second
    #                     on f_st_routes = s_st_routes
    #                     ) WHERE f_ord < sec_ord) firstLastRoutes
    #                     on route_id = f_st_routes
    #                      join timetable_of_days
    #                     on timetable.id = timetable_of_days.timetable_id
    #                     WHERE sort_order BETWEEN f_ord AND sec_ord AND day_of_week = ?"""
    #         available_routes = cursor.execute(query,st_from_id, st_to_id, day_of_week).fetchall()
    #     except pyodbc.Error as exc:
    #         # TODO
    #         return
    #         pass
    #     routes_amount = len(available_routes)
    #     self.AllRoutesForBuy_tbl.setRowCount(routes_amount)
    #     for route_id, tt_id, st_id, order, arr_time, delay in available_routes:
    #         # self.routes_for_tickets[] =



if __name__ == "__main__":
    # os.system('python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py')
    ########################################
    # Initialize connection to DB
    ##########################################
    # driver = "ODBC Driver 17 for SQL Server"
    driver = "MySQL ODBC 8.0 Unicode Driver"
    server_name = "localhost"
    database = "tickets_on_train"
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
    mainwindow = Window()
    mainwindow.show()
    sys.exit(app.exec())
