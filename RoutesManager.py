from functools import partial

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QLineEdit

import main_app
import pyodbc



class Routes_Manager():

    def __init__(self, user_interface, db_cursor, mainApp):
        self.editRoute_dialog = None
        self._mainApp = mainApp
        self._ui = user_interface
        self._db_cursor = db_cursor

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
    def delete_route(self, route_id):   #TODO Проверка что нет использованных данных в построении расписания!
        try:
            self._db_cursor.execute("""DELETE FROM routes WHERE route_id = ?""",route_id)
            self._db_cursor.commit()
        except pyodbc.Error as exc:
            self._db_cursor.rollback()
            QMessageBox.critical(self._ui, "Route deletion failed!",
                                 "Can't delete route because of:\n{}".format(exc.args))
            return
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
    def open_edit_route_Dialog(self, route_id, route_name):
        self.editRoute_dialog = main_app.EditRouteDialog(route_id, route_name, self, self._db_cursor, self._ui)
        self.editRoute_dialog.fillStatinosBox()
        self.editRoute_dialog.fill_stations_table(self.get_stations_of_route(route_id))
        self.editRoute_dialog.exec_()
        return

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

    def tariff_field_changed(self, field: QLineEdit, route_id):
        with main_app.SignalwsBlockedWidget(field) as widget:
            try:
                new_trf = float(widget.text())
                widget.setStyleSheet("background-color : #FFFFFF")
                self._db_cursor.execute("""UPDATE routes r SET r.tariff=? WHERE route_id=?""", new_trf, route_id)
                self._db_cursor.commit()
            except Exception as exc:
                self._db_cursor.rollback()
                widget.setStyleSheet("background-color : #FFcccc")
                field.setToolTip("Введите цену в формате \'₽₽₽.₽₽\'")
        return
    #########################
    #######################
    ######################







