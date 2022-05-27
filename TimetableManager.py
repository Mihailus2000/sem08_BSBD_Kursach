# from copy import copy
# from functools import partial
#
# import pyodbc
# from pyodbc import Cursor
#
# from PyQt5.QtWidgets import *
# from PyQt5.uic import loadUi, pyuic
from PyQt5 import QtCore, QtGui
import main_app



class Timetable_Manager:

    def __init__(self, user_interface, db_cursor, mainApp):
        self.edit_passage_dialog = None
        self._mainApp = mainApp
        self._ui = user_interface
        self._db_cursor = db_cursor

    def update_timetable_table(self):
        passages = self.get_all_passages()
        self._ui.fill_TimetableManagment_table(passages)

    def get_all_passages(self):
        #####################################
        # load all passages from DB
        #####################################
        query = """SELECT DISTINCT t.id, t.number, r.route_id, r.name FROM trains t 
        INNER JOIN passages p ON p.train_id = t.id 
        INNER JOIN stations_to_routes str ON p.passage_first_station_to_route_id = str.id
        INNER JOIN routes r on str.route_id = r.route_id"""
        passages = self._db_cursor.execute(query).fetchall()
        return passages

    @QtCore.pyqtSlot(int)
    def delete_passage(self, train_id, route_id):
        pass
        # self._db_cursor.execute("""DELETE FROM trains WHERE trains.id = ?""", train_id)
        # now_trains = self.get_all_passages()
        # self._ui.fill_TimetableManagment_table(now_trains)


    #########################
    #######################
    ######################

    @QtCore.pyqtSlot(int)
    def open_edit_passage_Dialog(self, train_id, route_id):
        self.edit_passage_dialog = main_app.EditTimetableDialog(self._db_cursor,self._ui)
        self.edit_passage_dialog.set_route_and_train_manual(route_id,train_id)
        self.edit_passage_dialog.exec_()
        print("HERE OPENS Dialog PASSAGE TIMETABLE EDITOR") # TODO Добавить создание диалогового окна
        pass


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




