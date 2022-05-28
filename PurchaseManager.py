# from copy import copy
# from functools import partial
#
import numpy as np
import pyodbc
# from pyodbc import Cursor
#
# from PyQt5.QtWidgets import *
# from PyQt5.uic import loadUi, pyuic
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMessageBox, QHeaderView

import main_app
from prettytable import PrettyTable


class MysqlConMen:
    def __init__(self, cursor: pyodbc.Cursor, ui):
        self.__cursor: pyodbc.Cursor = cursor
        self.__ui = ui
        self._is_ok = True

    def __enter__(self):
        return self.__cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self._is_ok = False
            self.__cursor.rollback()
            QMessageBox.critical(self.__ui, "MySQL Exception!",
                                 "What's happend:\n{}".format(exc_val.args))
            return True
        return True

    @property
    def is_ok(self):
        return self._is_ok


class TrainInfo:
    class CarriageInfo:
        def __init__(self, id, id_name, ord_num, type_id, type_name):
            self.id = id
            self.id_name = id_name
            self.ord_num = ord_num
            self.type_id = type_id
            self.type_name = type_name
            self.seat_types = {}  # key = typename_id, data = [typename, total_seats, buzy_seats]

        def add_type(self, sTnm_ID, sT_nm, total_seats, buzy_seats):
            self.seat_types[sTnm_ID] = [sT_nm, total_seats, buzy_seats if buzy_seats is not None else 0]

    def __init__(self, new_train_id):
        self.train_id = new_train_id
        self.train_routes = {}
        # self.carriges: dict[
        #     TrainInfo.CarriageInfo] = {}  # key = ordnum, data = class TODO Определиться - ключ это п.н. или ID

    def add_route(self, r_id):
        self.train_routes[r_id] = {}

    def add_carriage(self,r_id, id, nm, ord, T_id, T_nm):
        new_carr = self.CarriageInfo(id, nm, ord, T_id, T_nm)
        self.train_routes[r_id][ord] = new_carr
        # self.carriges[ord] = new_carr
        return new_carr

    # def set_carrInfo(self, carr_ord, sTnm_ID, sT_nm, total_seats, buzy_seats):
    #     new_carr = self.carriges[carr_ord].add_type(sTnm_ID, sT_nm, total_seats, )

    #################################
    #################################
    #################################
    #################################


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

    def __check_if_input_ok(self):
        if self._ui.choose_from_station_cBox.currentData() != -1 and self._ui.choose_to_station_cBox.currentData() != -1:
            self._ui.find_availiable_passages_btn.setEnabled(True)
        else:
            self._ui.find_availiable_passages_btn.setEnabled(False)

    def __changed_station_from(self, new_index):
        self._station_from_id = self._ui.choose_from_station_cBox.currentData()
        station_from_name = self._ui.choose_from_station_cBox.currentText()
        print("Choose FROM station: id={}|Name={}".format(self._station_from_id, station_from_name))
        self.__check_if_input_ok()

    def __changed_station_to(self, new_index):
        self._station_to_id = self._ui.choose_to_station_cBox.currentData()
        station_to_name = self._ui.choose_to_station_cBox.currentText()
        print("Choose TO station: id={}|Name={}".format(self._station_to_id, station_to_name))
        self.__check_if_input_ok()

    def __changed_travel_date(self, new_date):
        self._travel_date = new_date
        print("Choose TRAVEL DATE: {}".format(self._travel_date.toString("dd.MM.yyyy")))

    def __fill_stations_cbox(self):  # TODO Учесть, что при добавлени станции в 1/2 список, из другого надо убрать
        self._ui.choose_from_station_cBox.clear()
        self._ui.choose_from_station_cBox.addItem("Не выбрано", -1)
        query_all_stations = """SELECT s.station_id, s.station_name FROM stations s"""
        stations = self._db_cursor.execute(query_all_stations).fetchall()
        for st_id, st_name in stations:
            self._ui.choose_from_station_cBox.addItem("{} ({})".format(st_name, st_id), int(st_id))
        self._ui.choose_from_station_cBox.setCurrentIndex(0)

        # self.statusBar.showMessage("Выпадающий список обновился", 3000)

        self._ui.choose_to_station_cBox.clear()
        query_all_stations = """SELECT s.station_id, s.station_name FROM stations s"""
        self._ui.choose_to_station_cBox.addItem("Не выбрано", -1)
        stations = self._db_cursor.execute(query_all_stations).fetchall()
        for st_id, st_name in stations:
            self._ui.choose_to_station_cBox.addItem("{} ({})".format(st_name, st_id), int(st_id))
        self._ui.choose_to_station_cBox.setCurrentIndex(0)
        self._ui.choose_date_travel.setDateRange(QDate.currentDate(), QDate.currentDate().addDays(30))

    def __find_passages(self):
        query1 = """select  str.station_id, str.sort_order from timetable t
            inner join routes r1 on r1.route_id = t.route_id and t.station_id = ?
            left join timetable t2 on t2.route_id = r1.route_id and t2.station_id = ? and t2.train_id = t.train_id
            left join passages p on p.train_id=t.train_id and p.day_of_week  = weekday(str_to_date(?,'%d.%m.%Y'))
            left join timetable t3 on t3.train_id=t.train_id and t3.route_id=t.route_id
            left join stations_to_routes str_F on str_F.route_id = t.route_id and  str_F.station_id=t.station_id
            left join stations_to_routes str_T on str_T.route_id = t2.route_id and  str_T.station_id=t2.station_id
            inner join stations_to_routes str on str.route_id = t.route_id and  str.station_id=t3.station_id
                                        and str.sort_order>=str_F.sort_order and str.sort_order<=str_T.sort_order
            group by str.station_id
            order by  t.route_id, t.train_id, str.sort_order"""

        selected_date = self._ui.choose_date_travel.date().toString("dd.MM.yyyy")
        mng = MysqlConMen(self._db_cursor, self._ui)
        with mng as cursor:
            res = cursor.execute(query1, self._station_from_id, self._station_to_id, selected_date).fetchall()
            output_table = PrettyTable()
            output_table.field_names = ["Station_id", "Sort_order"]
            output_table.add_rows(res)
            print(output_table)
            ids = [str(arr[0]) for arr in res]
            to_ids, from_ids = ','.join(ids[1:]), ','.join(ids[:-1])
            # print(from_ids)
            # print(to_ids)

            # for st_id, s_ord in res:
            #     print("{} | {}".format(st_id, s_ord))

            # Все места в вагонах и ЗАКАЗЫ
            query2 = """select t.id, t.number, tt.route_id, r.name, c.carriage_id, c.carriage_name, ctt.order_num, 
                            ct.id, ct.type_name, st.seat_type_id, st.type_name,  COUNT(s.id) total,
                   (select  count(o.order_id) from `order` o
                    left join seats s on s.id=o.seat_id
                     where o.date_from = (str_to_date(?,'%d.%m.%Y'))
                        and (o.station_from_id in ({}) or o.station_to_id in({}))
                    and t.id=train_id and tt.train_id=ctt.train_id and tt.route_id=o.route_id and c.carriage_id=carriage_id and st.seat_type_id=seat_type
                    group by train_id, route_id, carriage_id, seat_type) busy
                       from trains t
                    left join (select route_id, train_id FROM timetable tt group by train_id, route_id) tt on tt.train_id = t.id
                    left join routes r on tt.route_id = r.route_id
                    left join carriages_to_train ctt on t.id = ctt.train_id
                    left join carriages c on ctt.carriage_id = c.carriage_id
                    left join carriage_types ct on ct.id = c.carriage_type
                    left join seats s on s.carriage_type = ct.id
                    left join seat_types st on s.seat_type = st.seat_type_id
                    group by t.id, c.carriage_id, s.carriage_type, s.seat_type, tt.route_id;""".format(from_ids, to_ids)

            res2 = cursor.execute(query2, selected_date).fetchall()
            output_table = PrettyTable()
            output_table.field_names = ["Train_ID", "Train_num", "Route_ID", "Route_nm", "Carr_ID", "Carr_name", "Carr_ordnum",
                                        "CarrT_ID", "CarrT_name", "SeatT_ID", "SeatT_name", "Total_seats", "Buzy_seats"]
            output_table.add_rows(res2)
            parse_tr_ID, parse_route_ID, parse_carr_ID, parse_sT_ID = None, None, None, None
            parse_carr, parse_train = None, None
            all_trains = []
            for train_ID, train_num, route_ID, route_nm, carr_ID, carr_name, carr_ordnum, carrT_ID, carrT_name, \
                                                    seatT_ID, seatT_name, total_seats, buzy_seats in res2:
                # if parse_tr_ID is None or parse_carr_ID is None or parse_sT_ID is None:
                #     parse_tr_ID = train_ID
                #     parse_carr_ID = carr_ID
                #     parse_sT_ID = seatT_ID
                if parse_tr_ID == train_ID:
                    if parse_route_ID == route_ID:
                        if parse_carr_ID == carr_ID:
                            parse_carr.add_type(seatT_ID, seatT_name, total_seats, buzy_seats)
                        else:
                            parse_carr_ID = carr_ID  # 3
                            parse_carr = parse_train.add_carriage(route_ID,carr_ID, carr_name, carr_ordnum, carrT_ID, carrT_name)
                            parse_carr.add_type(seatT_ID, seatT_name, total_seats, buzy_seats)
                    else:
                        parse_route_ID = route_ID # 2
                        parse_train.add_route(route_ID)
                        parse_carr = parse_train.add_carriage(route_ID, carr_ID, carr_name, carr_ordnum, carrT_ID,
                                                              carrT_name)
                else:
                    parse_tr_ID = train_ID  # 1
                    parse_route_ID = route_ID # 2
                    parse_carr_ID = carr_ID  # 3
                    parse_train = TrainInfo(train_ID)
                    all_trains.append(parse_train)
                    parse_train.add_route(route_ID)
                    parse_carr = parse_train.add_carriage(route_ID, carr_ID, carr_name, carr_ordnum, carrT_ID, carrT_name)
                    parse_carr.add_type(seatT_ID, seatT_name, total_seats, buzy_seats)

            print(output_table)

        if mng.is_ok:
            self._ui.AllRoutesForBuy_tbl.setRowCount(0)
            self._ui.AllRoutesForBuy_tbl.setColumnCount(5)
            self._ui.AllRoutesForBuy_tbl.setHorizontalHeaderLabels([
                "Поезд №", "Отправление", "Прибытие", "Свободно"])
            header = self._ui.AllRoutesForBuy_tbl.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            header.setCascadingSectionResizes(True)
            header.setDefaultSectionSize(140)
            header.setHighlightSections(False)
            header.setMinimumSectionSize(100)
            header.setSortIndicatorShown(False)
            header.setStretchLastSection(False)

            for train in all_trains:
                tr_id = train.train_id


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
