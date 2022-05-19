# from PyQt5.uic import loadUi
from functools import partial

# from main import MainWindowUI
# import PyQt5
# from PyQt5.uic import loadUi

import pyodbc
from pyodbc import Cursor
from PyQt5.QtWidgets import QWidget, QApplication, QStackedWidget, QPushButton, QTableWidget, QTableWidgetItem, \
    QStyledItemDelegate, QDialog, QLabel, QMainWindow, QInputDialog, QMessageBox, QComboBox, QCheckBox, \
    QAbstractScrollArea, QDialogButtonBox, QVBoxLayout
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QTime, QSize
# from main import MainWindowUI, ApplicationBack, EditRouteDialog
import main

#
# class MyCheckBox(QCheckBox):
#     def __init__(self, *args):
#         super(MyCheckBox, self).__init__(*args)  # will fail if passing **kwargs
#         self._readOnly = False
#
#     def isReadOnly(self):
#         return self._readOnly
#
#     def mousePressEvent(self, event):
#         if (self.isReadOnly()):
#             event.accept()
#         else:
#             super(MyCheckBox, self).mousePressEvent(event)
#
#     def mouseMoveEvent(self, event):
#         if (self.isReadOnly()):
#             event.accept()
#         else:
#             super(MyCheckBox, self).mouseMoveEvent(event)
#
#     def mouseReleaseEvent(self, event):
#         if (self.isReadOnly()):
#             event.accept()
#         else:
#             super(MyCheckBox, self).mouseReleaseEvent(event)
#
#     # Handle event in which the widget has focus and the spacebar is pressed.
#     def keyPressEvent(self, event):
#         if (self.isReadOnly()):
#             event.accept()
#         else:
#             super(MyCheckBox, self).keyPressEvent(event)
#
#     @QtCore.pyqtSlot(bool)
#     def setReadOnly(self, state):
#         self._readOnly = state
#
#     readOnly = QtCore.pyqtProperty(bool, isReadOnly, setReadOnly)
#
#
# class DialogCreateNewRouteUI(QDialog):
#     def __init__(self, parent_ui=None):
#         super().__init__(parent_ui)
#         loadUi("dialogAddNewRoute.ui", self)
#         self.show()
#
#
# class NewRouteCreator():
#     def __init__(self, db_cursor:Cursor, user_interface:DialogCreateNewRouteUI, mainApp : ApplicationBack):
#         self.ui = user_interface
#         self.mainApp = mainApp
#         self.mainApp_ui = mainApp.ui
#         self.db_cursor = db_cursor
#
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
#
#         self.all_stations = []
#         self.route_is_added = False
#         self.days = None
#         self.new_tt_id = None
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
#         self.start_value = None
#         self.changedValue = None
#         self.is_doubleClicked = False
#         self.is_changedItem = False
#         self.items_to_update = []
#         self.ui.apply_rt_changes_btn.setEnabled(False)
#         self.all_stations_id_to_name = {}
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
#                 self.db_cursor.execute(query1, route_id)
#                 query2 = """DELETE FROM timetable WHERE route_id = ?"""
#                 self.db_cursor.execute(query2, route_id)
#                 query3 = """DELETE FROM routes
#                                             WHERE route_id = ?"""
#                 self.db_cursor.execute(query3, route_id)
#             except pyodbc.Error as exc:
#                 self.db_cursor.rollback()
#                 QMessageBox.critical(self, "Cancelling failed!",
#                                      "Can't delete route because of:\n{}".format(exc.args))
#                 return
#             self.db_cursor.commit()
#             QMessageBox.information(self, "Route insertion procedure", "All changes were successfully Cancelled!")
#             self.mainApp_ui.update_routes_form()
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
#         self.mainApp_ui.update_routes_form()
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
#         stations = self.db_cursor.execute(query).fetchall()
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

class Timetable_Manager():
    def __init__(self,user_interface: main.MainWindowUI, db_cursor: Cursor, mainApp : main.ApplicationBack, route_id):
        self._mainApp = mainApp
        self._ui = user_interface
        self._db_cursor = db_cursor
        self._route_id = route_id   # Рейсы связаны с одним маршрутом

    def get_all_passages_from_route(self):
        get_passages = """SELECT passage_number, t.name FROM stations_to_routes
            LEFT JOIN timetable
            ON stations_to_routes.id = timetable.routes_to_stations
            LEFT JOIN trains t on timetable.train_id = t.id
            WHERE stations_to_routes.route_id = ?
            GROUP BY passage_number, sort_order
            ORDER BY passage_number, sort_order"""
        passages = self._db_cursor.execute(get_passages,self._route_id,self._route_id).fetchall()
        return passages

    def update_timetable(self):
        passages = self.get_all_passages_from_route()
        self._ui.fill_admin_timetable(passages)

    def add_new_passage(self):
        pass


class Routes_Manager():

    @property
    def timetable_manager(self):
        return self._timetable_manager

    def __init__(self, user_interface, db_cursor: Cursor, mainApp):
        self.editRoute_dialog = None
        self._mainApp = mainApp
        self._ui = user_interface
        self._db_cursor = db_cursor
        self._timetable_manager : Timetable_Manager = None

    def update_routes(self):
        routes = self.get_all_routes()
        self._ui.fill_routeManagment_table(routes=routes)

    def get_all_routes(self):
        #####################################
        # load all routes from DB
        #####################################
        query = """SELECT * FROM routes order by route_id"""
        routes = self._db_cursor.execute(query).fetchall()
        return routes

    @QtCore.pyqtSlot(int)
    def delete_route(self, route_id):
        self._db_cursor.execute("""DELETE FROM routes WHERE route_id = ?""",route_id)
        routes = self.get_all_routes()
        self._ui.fill_routeManagment_table(routes=routes)


    #########################
    #######################
    ######################

    def get_stations_of_route(self, route_id):
        curr_stations = self._db_cursor.execute("""SELECT str.id, station_name, sort_order FROM stations_to_routes str 
                                        INNER JOIN stations s ON str.station_id = s.station_id  WHERE route_id = ?""",
                                                route_id).fetchall()
        return curr_stations

    @QtCore.pyqtSlot(int)
    def open_edit_route_Dialog(self, route_id):
        self.editRoute_dialog = main.EditRouteDialog(route_id,self,self._db_cursor,self._ui)
        self.editRoute_dialog.fillStatinosBox()
        self.editRoute_dialog.fill_stations_table(self.get_stations_of_route(route_id))
        self.editRoute_dialog.exec_()

    def add_station_to_route(self, route_id):
        i = self._db_cursor.execute("""SELECT COUNT(*) FROM stations_to_routes WHERE route_id = ?"""
                                    , route_id).fetchone()[0]
        # i = self.stationsToRoute_table.rowCount()
        new_station_id = self.editRoute_dialog.all_stationsBox.itemData(
            self.editRoute_dialog.all_stationsBox.currentIndex())
        try:
            self._db_cursor.execute("""INSERT INTO stations_to_routes (route_id, station_id, sort_order)
                                    VALUES (?,?,?)""",route_id, new_station_id, i+1)
            self._db_cursor.commit()
        except pyodbc.Error as exc:
            self._db_cursor.rollback()
            QMessageBox.critical(self.editRoute_dialog, "Station additing failed!",
                                 "Can't add station because of:\n{}".format(exc.args))
            return
        self.editRoute_dialog.fill_stations_table(self.get_stations_of_route(route_id))

    @QtCore.pyqtSlot(int)
    def delete_station_from_route(self, rt_to_st_id):  # rt_to_st_id = (id,route_id)
        # TODO: Change counts in DB:
        rts_id, route_id = rt_to_st_id
        try:
            query0 = """SELECT sort_order FROM stations_to_routes
                               WHERE id = ?"""
            order = int(self._db_cursor.execute(query0, rts_id).fetchone()[0])
            query1 = """DELETE FROM stations_to_routes
                               WHERE id = ?"""
            self._db_cursor.execute(query1, rts_id)

            query3 = """UPDATE kursach.stations_to_routes t3 SET t3.sort_order=(
               SELECT (@row_number:=@row_number + 1) AS num FROM (SELECT @row_number:=0 as tmp ) as rn)
               where t3.route_id=?;"""
            self._db_cursor.execute(query3, route_id)
        except pyodbc.Error as exc:
            self._db_cursor.rollback()
            QMessageBox.critical(self.editRoute_dialog, "Error!",
                                 "Can't delete station because of:\n{}".format(exc.args))
        self._db_cursor.commit()
        self.editRoute_dialog.fill_stations_table(self.get_stations_of_route(route_id))

    #########################
    #######################
    ######################


    def start_timetable_manager(self, route_id):
        index = self._ui.stackedWidget.indexOf(self._ui.timetable_form)
        self._ui.stackedWidget.setCurrentIndex(index)
        self._timetable_manager = Timetable_Manager(self._ui, self._db_cursor, self._mainApp, route_id)
        self._ui.update_passages_btn.clicked.connect(self._timetable_manager.update_passages())
        self._ui.add_passage_btn.clicked.connect(self._timetable_manager.add_new_passage())




