
# from copy import copy
# from functools import partial
#
import pyodbc
# from pyodbc import Cursor
#
# from PyQt5.QtWidgets import *
# from PyQt5.uic import loadUi, pyuic
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMessageBox

import main_app



class Purchase_Manager():

    def __init__(self, user_interface, db_cursor, mainApp):
        # self.editTrain_dialog = None
        self._mainApp = mainApp
        self._ui = user_interface
        self._db_cursor = db_cursor
        self._station_from_id = None
        self._station_to_id = None
        self._travel_date = None
        self.__fill_stations_cbox()
        self._ui.find_availiable_passages_btn.clicked.connect(self.__find_passages)
        self._ui.find_availiable_passages_btn.setEnabled(False)
        self._ui.choose_from_station_cBox.currentIndexChanged.connect(self.__changed_station_from)
        self._ui.choose_to_station_cBox.currentIndexChanged.connect(self.__changed_station_to)
        self._ui.choose_date_travel.dateChanged.connect(self.__changed_travel_date)


    def __changed_station_from(self, new_index):
        self._station_from_id = self._ui.choose_from_station_cBox.currentData()
        station_from_name = self._ui.choose_from_station_cBox.currentText()
        print("Choose FROM station: id={}|Name={}".format(self._station_from_id, station_from_name))

    def __changed_station_to(self, new_index):
        self._station_to_id = self._ui.choose_to_station_cBox.currentData()
        station_to_name = self._ui.choose_to_station_cBox.currentText()
        print("Choose TO station: id={}|Name={}".format(self._station_to_id, station_to_name))

    def __changed_travel_date(self, new_date):
        self._travel_date = new_date
        print("Choose TRAVEL DATE: {}".format(self._travel_date.toString("dd.MM.yyyy")))



    def __fill_stations_cbox(self):     # TODO Учесть, что при добавлени станции в 1/2 список, из другого надо убрать
        self._ui.choose_from_station_cBox.clear()
        self._ui.choose_from_station_cBox.addItem("Не выбрано", -1)
        query_all_stations = """SELECT s.station_id, s.station_name FROM stations s"""
        stations = self._db_cursor.execute(query_all_stations).fetchall()
        for st_id, st_name in stations:
            self._ui.choose_from_station_cBox.addItem(st_name, int(st_id))
        self._ui.choose_from_station_cBox.setCurrentIndex(0)

        # self.statusBar.showMessage("Выпадающий список обновился", 3000)

        self._ui.choose_to_station_cBox.clear()
        query_all_stations = """SELECT s.station_id, s.station_name FROM stations s"""
        self._ui.choose_to_station_cBox.addItem("Не выбрано", -1)
        stations = self._db_cursor.execute(query_all_stations).fetchall()
        for st_id, st_name in stations:
            self._ui.choose_to_station_cBox.addItem(st_name, int(st_id))
        self._ui.choose_to_station_cBox.setCurrentIndex(0)
        self._ui.choose_date_travel.setDateRange(QDate.currentDate(),QDate.currentDate().addDays(30))

    def __find_passages(self):

        pass
    # def update_trains_table(self):
    #     trains = self.get_all_trains()
    #     self._ui.fill_trainsManagment_table(trains)

    # def get_all_trains(self):
    #     #####################################
    #     # load all trains from DB
    #     #####################################
    #     query = """SELECT * FROM trains order by number"""
    #     trains = self._db_cursor.execute(query).fetchall()
    #     return trains

    # @QtCore.pyqtSlot(int)
    # def delete_train(self, train_id):
    #     try:
    #         self._db_cursor.execute("""DELETE FROM trains WHERE trains.id = ?""", train_id)
    #         now_trains = self.get_all_trains()
    #         self._ui.fill_trainsManagment_table(now_trains)
    #     except pyodbc.Error as err:
    #         self._db_cursor.rollback()
    #         QMessageBox.critical(self.editTrain_dialog, "Error!",
    #              "Can't delete train because of:\n{}".format(err.args))

    #########################
    #######################
    ######################


    # @QtCore.pyqtSlot(int)
    # def open_edit_train_Dialog(self, train_id):
    #     train_name = self._db_cursor.execute("""SELECT number FROM trains WHERE id = ?""", train_id).fetchone()[0]
    #     self.editTrain_dialog = main_app.EditTrainDialog(self._db_cursor, train_id, train_name, self._ui)
    #     self.editTrain_dialog.exec_()


    # @QtCore.pyqtSlot(int)
    # def delete_station_from_route(self, rt_to_st_id):  # rt_to_st_id = (id,route_id)
    #     # TODO: Change counts in DB:
    #     rts_id, route_id = rt_to_st_id
    #     try:
    #         query0 = """SELECT sort_order FROM stations_to_routes
    #                            WHERE id = ?"""
    #         order = int(self._db_cursor.execute(query0, rts_id).fetchone()[0])
    #         query1 = """DELETE FROM stations_to_routes
    #                            WHERE id = ?"""
    #         self._db_cursor.execute(query1, rts_id)
    #
    #         query3 = """UPDATE kursach.stations_to_routes t3 SET t3.sort_order=(
    #            SELECT (@row_number:=@row_number + 1) AS num FROM (SELECT @row_number:=0 as tmp ) as rn)
    #            where t3.route_id=?;"""
    #         self._db_cursor.execute(query3, route_id, route_id)
    #     except pyodbc.Error as exc:
    #         self._db_cursor.rollback()
    #         QMessageBox.critical(self.editRoute_dialog, "Error!",
    #                              "Can't delete station because of:\n{}".format(exc.args))
    #     self._db_cursor.commit()
    #     self.editRoute_dialog.fill_stations_table(self.get_stations_of_route(route_id))

    #########################
    #######################
    ######################


    # def start_timetable_manager(self, route_id):
    #     index = self._ui.stackedWidget.indexOf(self._ui.timetable_form)
    #     self._ui.stackedWidget.setCurrentIndex(index)
    #     self._timetable_manager = Timetable_Manager(self._ui, self._db_cursor, self._mainApp, route_id)
    #     self._ui.update_passages_btn.clicked.connect(self._timetable_manager.update_passages())
    #     self._ui.add_passage_btn.clicked.connect(self._timetable_manager.add_new_passage())




