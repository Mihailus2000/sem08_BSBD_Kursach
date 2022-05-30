import os
from copy import copy
from functools import partial

import pyodbc
import sys
from PyQt5.QtCore import Qt, QTime, QSize
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QImage

from PyQt5.QtWidgets import QWidget, QApplication, QStackedWidget, QPushButton, QTableWidget, QTableWidgetItem, \
    QStyledItemDelegate, QDialog, QLabel, QMainWindow, QInputDialog, QMessageBox, QComboBox, QCheckBox, \
    QAbstractScrollArea, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QLineEdit, QHeaderView, \
    QTimeEdit, QStatusBar, QSpinBox
from PyQt5.uic import loadUi, pyuic
from PyQt5 import QtCore, QtGui

import RoutesManager
import TimetableManager
import TrainsManager
import PurchaseManager
import regex as re


def connectToDB(driver, ser_name, db_name, username, passwd):
    return pyodbc.connect("""DRIVER={};
                        SERVER={};
                        DATABASE={};
                        UID={};
                        PWD={}""".format(driver, ser_name, db_name, username, passwd))


AUTHORIZED = False
USR_LOGIN = None


class EditRouteDialog(QDialog):
    def __init__(self, route_id, route_name, route_manager, db_cursor: pyodbc.Cursor, parent=None):
        super().__init__(parent)
        self._route_id = route_id
        self._routes_manager = route_manager
        loadUi("edit_route_dialog.ui", self)
        self.editing_route_lbl.setText(route_name)
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
        self.stationsToRoute_table.setColumnCount(2)
        self.stationsToRoute_table.setHorizontalHeaderLabels([
            "Станция", ""])
        i = 0
        for r_to_st_id, st_name, sort_order in curr_stations:
            self.stationsToRoute_table.insertRow(i)
            station_name = QTableWidgetItem(st_name)
            station_name.setFlags((station_name.flags() | QtCore.Qt.CustomizeWindowHint) &
                                  ~QtCore.Qt.ItemIsEditable)
            self.stationsToRoute_table.setItem(i, 0, station_name)

            remove_route_button = QPushButton(text="Удалить", parent=self)
            remove_route_button.clicked.connect(lambda state, data=(r_to_st_id, self._route_id):
                                                self._routes_manager.delete_station_from_route(data))
            self.stationsToRoute_table.setCellWidget(i, 1, remove_route_button)
            i += 1

    #########################################
    ######################################
    ###################################
    ##############################


class MyCheckBox(QCheckBox):
    def __init__(self, *args):
        super(MyCheckBox, self).__init__(*args)  # will fail if passing **kwargs
        self._readOnly = False

    def isReadOnly(self):
        return self._readOnly

    def mousePressEvent(self, event):
        if (self.isReadOnly()):
            event.accept()
        else:
            super(MyCheckBox, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (self.isReadOnly()):
            event.accept()
        else:
            super(MyCheckBox, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if (self.isReadOnly()):
            event.accept()
        else:
            super(MyCheckBox, self).mouseReleaseEvent(event)

    # Handle event in which the widget has focus and the spacebar is pressed.
    def keyPressEvent(self, event):
        if (self.isReadOnly()):
            event.accept()
        else:
            super(MyCheckBox, self).keyPressEvent(event)

    @QtCore.pyqtSlot(bool)
    def setReadOnly(self, state):
        self._readOnly = state

    readOnly = QtCore.pyqtProperty(bool, isReadOnly, setReadOnly)

class AuthorizationModule:
    def __init__(self, ui, db_cursor: pyodbc.Cursor):
        self.__ui = ui
        self.__db_cursor = db_cursor
        self.__current_user = None
        self.__usr_id = None
        self.__user_priv_level = None
        self.__ui.authorize_btn.clicked.connect(self.__authorize)
        self.__ui.register_btn.clicked.connect(self.__register)
        self.__salt = "V^&fV%V&8v67356~$%^"
        self.__ui.back_button_on_registration_Page.clicked.connect(lambda: self.__ui.stackedWidget.setCurrentIndex(0))
        self.__ui.back_button_on_authrization_Page.clicked.connect(lambda: self.__ui.stackedWidget.setCurrentIndex(0))
        self.__ui.show_pass_registration.stateChanged.connect(self.__reg_show_pass)
        self.__ui.show_pass_on_authorization.stateChanged.connect(self.__auth_show_pass)
        self.__ui.account_exit_btn.clicked.connect(self.__account_exit_procedure)
        self.__ui.backup_DB_btn.clicked.connect(self.__do_backup_DB)
        self.__start_app_config()


    def __start_app_config(self):
        self.__ui.edit_routes_menu_btn.setEnabled(False)  # normal user
        self.__ui.edit_routes_menu_btn.setVisible(False)
        self.__ui.edit_trains_menu_btn.setEnabled(False)
        self.__ui.edit_trains_menu_btn.setVisible(False)
        self.__ui.edit_timetable_menu_btn.setEnabled(False)
        self.__ui.edit_timetable_menu_btn.setVisible(False)
        self.__ui.account_exit_btn.setEnabled(False)
        self.__ui.account_exit_btn.setVisible(False)
        self.__ui.backup_DB_btn.setEnabled(False)
        self.__ui.backup_DB_btn.setVisible(False)
        self.__ui.registerPage_errorInformation.setVisible(False)
        self.__ui.authorizePage_errorInformation.setVisible(False)


    def __reg_show_pass(self, new_state):
        if new_state == Qt.Checked:
            self.__ui.registerPage_password_input_field1.setEchoMode(QLineEdit.EchoMode.Password)
            self.__ui.registerPage_password_input_field2.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.__ui.registerPage_password_input_field1.setEchoMode(QLineEdit.EchoMode.Normal)
            self.__ui.registerPage_password_input_field2.setEchoMode(QLineEdit.EchoMode.Normal)

    def __auth_show_pass(self, new_state):
        if new_state == Qt.Checked:
            self.__ui.authPage_password_input_field.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.__ui.authPage_password_input_field.setEchoMode(QLineEdit.EchoMode.Normal)

    def __do_backup_DB(self):
        os.system("mysqldump -u root -pQwerty123! kursach > kursach_backup.sql")
        QMessageBox.information(self.__ui, "Dump DB", "Dump complited!")

    def __authorize(self):
        login = self.__ui.authPage_login_input_field.text()
        passwd = self.__ui.authPage_password_input_field.text()
        check_query = """SELECT u.user_id, u.privelegy_level FROM users u WHERE login = ? AND password = MD5(?)"""
        with PurchaseManager.MysqlConMen(self.__db_cursor, self.__ui) as cursor:
            usr_info = cursor.execute(check_query, login, passwd+self.__salt).fetchone()
            if usr_info is not None:
                self.__current_user = login
                del passwd
                self.__usr_id = usr_info[0]
                self.__user_priv_level = usr_info[1]
                self.__ui.authorizePage_errorInformation.setVisible(False)
                self.__ui.authorizePage_errorInformation.clear()
                self.__ui.authPage_password_input_field.clear()
                self.__ui.authPage_login_input_field.clear()
                self.__confirm_user_privilegies()
                self.__ui.stackedWidget.setCurrentIndex(0)

            else:
                self.__ui.authorizePage_errorInformation.setText("Ошибка аутентификации: неправильный логин или пароль") # Вывести сообщение об ошибке
                self.__ui.authorizePage_errorInformation.setVisible(True)
                self.__ui.authPage_password_input_field.clear()

    def __confirm_user_privilegies(self):
        match self.__user_priv_level:
            case 10:
                self.__ui.edit_routes_menu_btn.setEnabled(False) # normal user
                self.__ui.edit_routes_menu_btn.setVisible(False)
                self.__ui.edit_trains_menu_btn.setEnabled(False)
                self.__ui.edit_trains_menu_btn.setVisible(False)
                self.__ui.edit_timetable_menu_btn.setEnabled(False)
                self.__ui.edit_timetable_menu_btn.setVisible(False)
                self.__ui.backup_DB_btn.setEnabled(False)
                self.__ui.backup_DB_btn.setVisible(False)
            case 0:
                self.__ui.edit_routes_menu_btn.setEnabled(True) #full admin
                self.__ui.edit_routes_menu_btn.setVisible(True)
                self.__ui.edit_trains_menu_btn.setEnabled(True)
                self.__ui.edit_trains_menu_btn.setVisible(True)
                self.__ui.edit_timetable_menu_btn.setEnabled(True)
                self.__ui.edit_timetable_menu_btn.setVisible(True)
                self.__ui.backup_DB_btn.setEnabled(True)
                self.__ui.backup_DB_btn.setVisible(True)
        self.__ui.account_exit_btn.setEnabled(True)
        self.__ui.account_exit_btn.setVisible(True)

    def __account_exit_procedure(self):
        self.__user_priv_level = 10
        self.__usr_id = None
        self.__current_user = None
        self.__ui.edit_routes_menu_btn.setEnabled(False)  # normal user
        self.__ui.edit_routes_menu_btn.setVisible(False)
        self.__ui.edit_trains_menu_btn.setEnabled(False)
        self.__ui.edit_trains_menu_btn.setVisible(False)
        self.__ui.edit_timetable_menu_btn.setEnabled(False)
        self.__ui.edit_timetable_menu_btn.setVisible(False)
        self.__ui.account_exit_btn.setEnabled(False)
        self.__ui.account_exit_btn.setVisible(False)
        self.__ui.backup_DB_btn.setEnabled(False)
        self.__ui.backup_DB_btn.setVisible(False)

    def __register(self):
        login = self.__ui.registerPage_login_input_field.text()
        passwd1 = self.__ui.registerPage_password_input_field1.text()
        passwd2 = self.__ui.registerPage_password_input_field2.text()
        if passwd1 == passwd2:
            check_existence_query = """SELECT user_id FROM users u WHERE login = ?"""
            register_query = """INSERT INTO users (login, password) 
                                VALUES (?,MD5(?))"""
            with PurchaseManager.MysqlConMen(self.__db_cursor, self.__ui) as cursor:
                # priv_lvl = cursor.execute(check_query, login, passwd + self.__salt).fetchone()
                is_exist = cursor.execute(check_existence_query, login).fetchone()
                if is_exist is None:
                    self.__ui.registerPage_errorInformation.setVisible(False)
                    self.__ui.registerPage_errorInformation.clear()
                    cursor.execute(register_query, login, passwd1+self.__salt)
                    self.__ui.registerPage_errorInformation.clear()
                    self.__ui.registerPage_login_input_field.clear()
                    self.__ui.registerPage_password_input_field1.clear()
                    self.__ui.registerPage_password_input_field2.clear()
                    self.__ui.stackedWidget.setCurrentIndex(6)
                    pass# Активировать сеанс
                else:
                    self.__ui.registerPage_errorInformation.setText(
                        "Ошибка регистрации: пользователь уже существует")  # Вывести сообщение об ошибке
                    self.__ui.registerPage_errorInformation.setVisible(True)
                    self.__ui.registerPage_password_input_field1.clear()
                    self.__ui.registerPage_password_input_field2.clear()
        else:
            self.__ui.registerPage_errorInformation.setText(
                "Ошибка регистрации: пароли не совпадают")  # Вывести сообщение об ошибке

class SignalwsBlockedWidget(object):
    def __init__(self, widget):
        self.__w = widget

    def __enter__(self):
        self.__w.blockSignals(True)
        return self.__w

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is not None:
            print("ERROR: {}".format(exc_tb.args))
        self.__w.blockSignals(False)
        return True


class EditTimetableDialog(QDialog):
    def __init__(self, db_cursor: pyodbc.Cursor, parent=None):
        super().__init__(parent)
        loadUi("editPassagesDialog.ui", self)
        self._db_cursor = db_cursor
        self.fill_routes_box()
        self.fill_trains_box()
        self.trains_comboBox.currentIndexChanged.connect(self.table_update)
        self.routes_comboBox.currentIndexChanged.connect(self.table_update)
        self.route_id = None
        self.train_id = None
        self.table_update()
        self.monday_checkBox.stateChanged.connect(
            lambda state, day=self.monday_checkBox.text(): self.work_days_changed(state, self.monday_checkBox, day))
        self.tuesday_checkBox.stateChanged.connect(
            lambda state, day=self.tuesday_checkBox.text(): self.work_days_changed(state, self.tuesday_checkBox, day))
        self.wednesday_checkBox.stateChanged.connect(
            lambda state, day=self.wednesday_checkBox.text(): self.work_days_changed(state, self.wednesday_checkBox, day))
        self.thirsday_checkBox.stateChanged.connect(
            lambda state, day=self.thirsday_checkBox.text(): self.work_days_changed(state, self.thirsday_checkBox, day))
        self.friday_checkBox.stateChanged.connect(
            lambda state, day=self.friday_checkBox.text(): self.work_days_changed(state, self.friday_checkBox, day))
        self.saturday_checkBox.stateChanged.connect(
            lambda state, day=self.saturday_checkBox.text(): self.work_days_changed(state, self.saturday_checkBox, day))
        self.sunday_checkBox.stateChanged.connect(
            lambda state, day=self.sunday_checkBox.text(): self.work_days_changed(state, self.sunday_checkBox, day))

    def set_route_and_train_manual(self, route_id, train_id):
        self.route_id = route_id
        self.train_id = train_id
        with SignalwsBlockedWidget(self.trains_comboBox) as t_cbox1:
            index = t_cbox1.findData(train_id)
            t_cbox1.setCurrentIndex(index)
        with SignalwsBlockedWidget(self.routes_comboBox) as r_cbox1:
            index = r_cbox1.findData(route_id)
            r_cbox1.setCurrentIndex(index)
        self.table_update(route_id,train_id)


    def update_timetable_by_dayschanges(self, state, day): # TODO ДОДЕЛАТЬ
        if state == Qt.Checked:
            # TODO Надо пройтись по ВСЕМ записям в str и заново сделать insert для нового дня)
            # TODO Или надо считать все записи в timetables по роуту + поезду (SELECT DISTINCT) и вставить ещё один набор
            pass

    def work_days_changed(self, state, checkbox: QCheckBox, day):
        self.route_id = self.routes_comboBox.itemData(self.routes_comboBox.currentIndex())


        insert_day_in_passages = """INSERT INTO passages (day_of_week, train_id, passage_first_station_to_route_id)
                        VALUES (?,?,(SELECT str.id FROM stations_to_routes str WHERE route_id = ? AND sort_order = 1))"""
        first_delete_day_in_passages = """DELETE FROM passages WHERE day_of_week=? AND train_id = ?
            AND passage_first_station_to_route_id = (SELECT str.id FROM stations_to_routes str  WHERE route_id = ? AND sort_order = 1
            LIMIT 1 )"""
        check_order_is_empy = """SELECT COUNT(o.order_id) FROM `order` o WHERE o.train_id = ? AND route_id = ?"""
        check_is_empty = """SELECT COUNT(p.passage_id) FROM passages p WHERE train_id = ? AND passage_first_station_to_route_id = 
            (SELECT str.id FROM stations_to_routes str  WHERE route_id = ? AND sort_order = 1 LIMIT 1 )"""
        delete_in_timetable = """DELETE FROM timetable tt WHERE route_id=? AND train_id=?"""
        if state == Qt.Checked:
            match day:
                case "Понедельник":
                    self._db_cursor.execute(insert_day_in_passages, 0, self.train_id, self.route_id)
                case "Вторник":
                    self._db_cursor.execute(insert_day_in_passages, 1, self.train_id, self.route_id)
                case "Среда":
                    self._db_cursor.execute(insert_day_in_passages, 2, self.train_id, self.route_id)
                case "Четверг":
                    self._db_cursor.execute(insert_day_in_passages, 3, self.train_id, self.route_id)
                case "Пятница":
                    self._db_cursor.execute(insert_day_in_passages, 4, self.train_id, self.route_id)
                case "Суббота":
                    self._db_cursor.execute(insert_day_in_passages, 5, self.train_id, self.route_id)
                case "Воскресенье":
                    self._db_cursor.execute(insert_day_in_passages, 6, self.train_id, self.route_id)
        else:
            cnt_orders = self._db_cursor.execute(check_order_is_empy, self.train_id, self.route_id).fetchone()[0]
            if cnt_orders != 0:
                with SignalwsBlockedWidget(checkbox) as cb:
                    cb.setChecked(True)
                QMessageBox.information(self, "Attention Please!", "You can't remove already using passage!!\n"
                                                                   "Please remove dependencies first!")
                return
            match day:
                case "Понедельник":
                    self._db_cursor.execute(first_delete_day_in_passages, 0, self.train_id, self.route_id)
                case "Вторник":
                    self._db_cursor.execute(first_delete_day_in_passages, 1, self.train_id, self.route_id)
                case "Среда":
                    self._db_cursor.execute(first_delete_day_in_passages, 2, self.train_id, self.route_id)
                case "Четверг":
                    self._db_cursor.execute(first_delete_day_in_passages, 3, self.train_id, self.route_id)
                case "Пятница":
                    self._db_cursor.execute(first_delete_day_in_passages, 4, self.train_id, self.route_id)
                case "Суббота":
                    self._db_cursor.execute(first_delete_day_in_passages, 5, self.train_id, self.route_id)
                case "Воскресенье":
                    self._db_cursor.execute(first_delete_day_in_passages, 6, self.train_id, self.route_id)

        cnt = self._db_cursor.execute(check_is_empty, self.train_id, self.route_id).fetchone()[0]
        if state == Qt.Unchecked:
            if cnt == 0:
                self._db_cursor.execute(delete_in_timetable, self.route_id, self.train_id)
            else:
                with SignalwsBlockedWidget(checkbox) as cb:
                    cb.setChecked(True)
                QMessageBox.information(self, "Attention Please!", "You can't remove already using passage!!\n"
                                                                   "Please remove dependencies first!")
                return

        self._db_cursor.commit()
        self.table_update()

    def table_update(self, r_id = None, t_id = None):
        self.route_id = self.routes_comboBox.itemData(self.routes_comboBox.currentIndex())
        self.train_id = self.trains_comboBox.itemData(self.trains_comboBox.currentIndex())
        checkBoxes_Notenabled = False
        self.passage_stations_tbl.setRowCount(0)
        self.passage_stations_tbl.setColumnCount(6)
        self.passage_stations_tbl.setHorizontalHeaderLabels([
            "Станция", "Время отправления", "Стоянка", "Минут до след. станции", "Ценовой коэффициент",  "Используется"])
        header = self.passage_stations_tbl.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setCascadingSectionResizes(True)
        header.setDefaultSectionSize(140)
        header.setHighlightSections(False)
        header.setMinimumSectionSize(100)
        header.setSortIndicatorShown(False)
        header.setStretchLastSection(False)

        if r_id is None or t_id is None:
            route_id = self.routes_comboBox.itemData(self.routes_comboBox.currentIndex())
            train_id = self.trains_comboBox.itemData(self.trains_comboBox.currentIndex())
        else:
            route_id = r_id
            train_id = t_id

        checkboxes = self.checkboxes_widget.findChildren(QCheckBox)
        for checkbox in checkboxes:
            with SignalwsBlockedWidget(checkbox) as cb:
                cb.setChecked(False)


        # Проверка существования рейса
        get_passages = """SELECT day_of_week FROM passages p
            INNER JOIN stations_to_routes str ON p.passage_first_station_to_route_id = str.id
            INNER JOIN routes r on str.route_id = r.route_id
            WHERE r.route_id = ? AND train_id = ?
            ORDER BY day_of_week"""
        # TODO Добавить случай, когда нет сразу ничего в БД по этой ПАРЕ
        passages = self._db_cursor.execute(get_passages, route_id, train_id).fetchall()
        if len(passages) == 0:
            checkBoxes_Notenabled = True  # Запрет на включение боксов, пока не вабран хотябы один день недели
            # TODO Добавить информирующее окно, что не найдено по паре ничего
            pass
        else:
            for dof in passages:
                match dof[0]:
                    case 0:
                        self.monday_checkBox.blockSignals(True)
                        self.monday_checkBox.setChecked(True)
                        self.monday_checkBox.blockSignals(False)
                    case 1:
                        self.tuesday_checkBox.blockSignals(True)
                        self.tuesday_checkBox.setChecked(True)
                        self.tuesday_checkBox.blockSignals(False)

                    case 2:
                        self.wednesday_checkBox.blockSignals(True)
                        self.wednesday_checkBox.setChecked(True)
                        self.wednesday_checkBox.blockSignals(False)
                    case 3:
                        self.thirsday_checkBox.blockSignals(True)
                        self.thirsday_checkBox.setChecked(True)
                        self.thirsday_checkBox.blockSignals(False)
                    case 4:
                        self.friday_checkBox.blockSignals(True)
                        self.friday_checkBox.setChecked(True)
                        self.friday_checkBox.blockSignals(False)
                    case 5:
                        self.saturday_checkBox.blockSignals(True)
                        self.saturday_checkBox.setChecked(True)
                        self.saturday_checkBox.blockSignals(False)
                    case 6:
                        self.sunday_checkBox.blockSignals(True)
                        self.sunday_checkBox.setChecked(True)
                        self.sunday_checkBox.blockSignals(False)


        # Получение списка станций для заполнения таблицы
        passage_stations = """SELECT s.station_id, s.station_name, str.sort_order FROM stations_to_routes str
            INNER JOIN stations s ON s.station_id = str.station_id
            # INNER JOIN routes r on str.route_id = r.route_id
            WHERE str.route_id = ?
            ORDER BY sort_order"""
        stations = self._db_cursor.execute(passage_stations, route_id).fetchall()

        i = 0
        self.passage_stations_tbl.setRowCount(len(stations))
        for st_id, st_name, order in stations:
            # self.passage_stations_tbl.insertRow(self.passage_stations_tbl.rowCount())
            station_name = QTableWidgetItem(st_name)
            station_name.setFlags((station_name.flags() | QtCore.Qt.CustomizeWindowHint) &
                                  ~QtCore.Qt.ItemIsEditable)
            self.passage_stations_tbl.setItem(i, 0, station_name)

            time = QTableWidgetItem("")
            time.setFlags((time.flags() | QtCore.Qt.CustomizeWindowHint) &
                          ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsEditable)
            self.passage_stations_tbl.setItem(i, 1, time)

            delta = QTableWidgetItem("")
            delta.setFlags((delta.flags() | QtCore.Qt.CustomizeWindowHint) &
                           ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsEditable)
            self.passage_stations_tbl.setItem(i, 2, delta)

            min_delta = QTableWidgetItem("")
            min_delta.setFlags((min_delta.flags() | QtCore.Qt.CustomizeWindowHint) &
                           ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsEditable)
            self.passage_stations_tbl.setItem(i, 3, min_delta)

            price_coeff = QTableWidgetItem("")
            price_coeff.setFlags((price_coeff.flags() | QtCore.Qt.CustomizeWindowHint) &
                           ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsEditable)
            self.passage_stations_tbl.setItem(i, 4, price_coeff)


            enabledBox = MyCheckBox(self)
            enabledBox.setReadOnly(checkBoxes_Notenabled)
            enabledBox.stateChanged.connect(lambda state, cb=enabledBox, tbl_row=i,
                                                   r_id=route_id, t_id=train_id,
                                                   st_id=st_id: self.change_row_usingState(state, cb, tbl_row, r_id, t_id,
                                                                                           st_id))
            self.passage_stations_tbl.setCellWidget(i, 5, enabledBox)
            i += 1

        # Получение существующих данных из расписания по данной паре
        query_passage_timetable_info = """SELECT tt.station_id, str.sort_order, TIME_FORMAT(tt.arrival_time, '%H:%i'), 
                                                                tt.delay, tt.minutes_to_next_station, tt.price_coeff
            FROM timetable tt INNER JOIN stations_to_routes str ON 
            tt.route_id=? AND tt.train_id=? AND tt.route_id=str.route_id AND tt.station_id=str.station_id"""
        passage_timetable_info = self._db_cursor.execute(query_passage_timetable_info, route_id, train_id).fetchall()

        # Перебираем данные и заполняем некоторые строки
        for st_id, sort_order, arr_time, delay, minutes, price_coeff in passage_timetable_info:
            hour, minute = arr_time.split(':')
            qtime_edit = QTimeEdit(QTime(int(hour), int(minute)), self)
            qtime_edit.setKeyboardTracking(False)
            qtime_edit.setDisplayFormat("HH:mm")
            qtime_edit.timeChanged.connect(lambda time, st_id=st_id, r_id=route_id, t_id=train_id, sort=sort_order - 1
                                           : self.change_time(time, st_id, r_id, t_id, sort))
            self.passage_stations_tbl.setCellWidget(sort_order-1, 1, qtime_edit)

            delta = QLineEdit(str(delay))
            delta.editingFinished.connect(lambda item=delta, st_id=st_id, r_id=route_id, t_id=train_id, sort=sort_order - 1
                                     : self.changed_delay(item, st_id, r_id, t_id, sort))
            self.passage_stations_tbl.setCellWidget(sort_order-1, 2, delta)

            mins = QLineEdit(str(minutes))
            mins.editingFinished.connect(
                lambda item=mins, st_id=st_id, r_id=route_id, t_id=train_id, sort=sort_order - 1
                : self.changed_minutes(item, st_id, r_id, t_id, sort))
            self.passage_stations_tbl.setCellWidget(sort_order - 1, 3, mins)

            price_coeff = QLineEdit(str(price_coeff))
            price_coeff.editingFinished.connect(
                lambda widget=price_coeff, st_id=st_id, r_id=route_id, t_id=train_id, sort=sort_order - 1
                : self.price_coeff_changed(widget, st_id, r_id, t_id, sort))
            self.passage_stations_tbl.setCellWidget(sort_order - 1, 4, price_coeff)

            mycheckBox: MyCheckBox = self.passage_stations_tbl.cellWidget(sort_order - 1, 5)
            with SignalwsBlockedWidget(mycheckBox) as checkbox:
                checkbox.setCheckState(Qt.Checked)



    def change_row_usingState(self, state, checkbox, tbl_row, route_id, train_id, st_id):
        if state == Qt.Checked:
            print("Change row state (INSERT) ({},{})".format(True, st_id))
            insert_query = """INSERT INTO timetable (route_id, train_id, station_id, arrival_time, delay, 
                                                                    minutes_to_next_station, price_coeff)
            VALUES (?,?,?,TIME(?),?,?,?)"""

            selected_time: QTime = QTime(0, 0)
            db_time = selected_time.toString("HH:mm")
            time_w = QTimeEdit(selected_time, self)
            time_w.setKeyboardTracking(False)
            time_w.setDisplayFormat("HH:mm")
            time_w.timeChanged.connect(lambda time, st_id=st_id, r_id=route_id, t_id=train_id, sort=tbl_row
                                       : self.change_time(time, st_id, r_id, t_id, sort))
            self.passage_stations_tbl.setCellWidget(tbl_row, 1, time_w)


            delta = QLineEdit("0", self)
            db_delta = int(delta.text())
            delta.textEdited.connect(lambda item=delta, st_id=st_id, r_id=route_id, t_id=train_id, sort=tbl_row
                                     : self.changed_delay(item, st_id, r_id, t_id, sort))
            self.passage_stations_tbl.setCellWidget(tbl_row, 2, delta)

            min = QLineEdit(str(0))
            db_min = int(min.text())
            min.editingFinished.connect(
                lambda item=min, st_id=st_id, r_id=route_id, t_id=train_id, sort=tbl_row
                : self.changed_minutes(item, st_id, r_id, t_id, sort))
            self.passage_stations_tbl.setCellWidget(tbl_row, 3, min)

            price_coeff = QLineEdit(str(0.0))
            db_price_coeff = float(price_coeff.text())
            price_coeff.editingFinished.connect(
                lambda widget=price_coeff, st_id=st_id, r_id=route_id, t_id=train_id, sort=tbl_row
                : self.price_coeff_changed(widget, st_id, r_id, t_id, sort))
            self.passage_stations_tbl.setCellWidget(tbl_row, 4, price_coeff)

            self._db_cursor.execute(insert_query, route_id, train_id, st_id, db_time, db_delta, db_min, db_price_coeff)  # TODO try: catch
        else:
            # 0 Проверка использования записей в БД
            check_order_is_empy = """SELECT COUNT(o.order_id) FROM `order` o WHERE o.train_id = ? AND route_id = ?"""
            cnt_orders = self._db_cursor.execute(check_order_is_empy, train_id, route_id).fetchone()[0]

            if cnt_orders != 0:
                with SignalwsBlockedWidget(checkbox) as cb:
                    cb.setChecked(True)
                QMessageBox.information(self, "Attention Please!", "You can't remove already using passage!!\n"
                                                                   "Please remove dependencies first!")
                return
            # 1 - Удаление из расписания данный день
            del_query1 = """DELETE FROM timetable tt WHERE route_id=? AND train_id=? AND station_id=?"""
            self._db_cursor.execute(del_query1, route_id, train_id, st_id)
            # 2 - Удаление из Passages, если пусто в расписании TODO Пропуск мб этого пункта? Т.к. юзеру это не надо
            self.passage_stations_tbl.removeCellWidget(tbl_row, 1)
            self.passage_stations_tbl.removeCellWidget(tbl_row, 2)
            self.passage_stations_tbl.removeCellWidget(tbl_row, 3)
            self.passage_stations_tbl.removeCellWidget(tbl_row, 4 )
        self._db_cursor.commit()

    def change_time(self, new_time: QTime, st_id, r_id, t_id, sort_ord):  # time, station, route, train
        query = """UPDATE timetable SET arrival_time = ? WHERE route_id = ? AND train_id = ? AND station_id = ?"""
        self._db_cursor.execute(query, new_time.toString("HH:mm"), r_id, t_id, st_id)
        self._db_cursor.commit()

    def changed_delay(self, item : QLineEdit, st_id, r_id, t_id, sort_ord):
        number = item
        if type(number) is not str:
            number = number.text()
        reg = re.compile(r"^\d+$")
        all_matches = re.fullmatch(reg, number)
        if all_matches is not None:
            query = """UPDATE timetable SET delay = ? WHERE route_id = ? AND train_id = ? AND station_id = ?"""
            self._db_cursor.execute(query, int(number), r_id, t_id, st_id)
            self._db_cursor.commit()
            widget = self.passage_stations_tbl.cellWidget(sort_ord, 2)
            widget.setStyleSheet("background-color : #FFFFFF")
        else:
            widget = self.passage_stations_tbl.cellWidget(sort_ord, 2)
            widget.setStyleSheet("background-color : #FFCCCC")

    def changed_minutes(self, item : QLineEdit, st_id, r_id, t_id, sort_ord):
        number = item
        if type(number) is not str:
            number = number.text()
        reg = re.compile(r"^\d+$")
        all_matches = re.fullmatch(reg, number)
        if all_matches is not None:
            query = """UPDATE timetable SET minutes_to_next_station = ? WHERE route_id = ? AND train_id = ? AND station_id = ?"""
            self._db_cursor.execute(query, int(number), r_id, t_id, st_id)
            self._db_cursor.commit()
            widget = self.passage_stations_tbl.cellWidget(sort_ord, 3)
            widget.setStyleSheet("background-color : #FFFFFF")
        else:
            widget = self.passage_stations_tbl.cellWidget(sort_ord, 3)
            widget.setStyleSheet("background-color : #FFCCCC")

    def price_coeff_changed(self, widget : QLineEdit, st_id, r_id, t_id, sort_ord):
        with SignalwsBlockedWidget(widget) as widget:
            try:
                new_price_coeff = float(widget.text())
                widget.setStyleSheet("background-color : #FFFFFF")
                query = """UPDATE timetable SET price_coeff = ? WHERE route_id = ? AND train_id = ? AND station_id = ?"""
                self._db_cursor.execute(query, new_price_coeff, r_id, t_id, st_id)
                self._db_cursor.commit()
            except Exception as exc:
                self._db_cursor.rollback()
                widget.setStyleSheet("background-color : #FFcccc")
            widget.setToolTip("Введите коэффициент в формате числа с плавающей точкой")
        return

    def fill_trains_box(self):
        trains = self._db_cursor.execute("""SELECT id, number FROM trains t ORDER BY number""").fetchall()
        self.trains_comboBox.addItem("не выбрано", userData=None)
        for train_id, train_num in trains:
            self.trains_comboBox.addItem(train_num, userData=train_id)
        self.trains_comboBox.setCurrentIndex(0)
    def fill_routes_box(self):
        routes = self._db_cursor.execute("""SELECT route_id, name FROM routes r ORDER BY name""").fetchall()
        self.routes_comboBox.addItem("не выбрано", userData=None)
        for r_id, r_name in routes:
            self.routes_comboBox.addItem(r_name, userData=r_id)
        self.routes_comboBox.setCurrentIndex(0)

    ##################################
    ##################################
    ##################################
    ##################################
    ##################################


class EditTrainDialog(QDialog):
    def __init__(self, db_cursor: pyodbc.Cursor, train_id, train_number, parent=None):
        super().__init__(parent)
        loadUi("edit_train_dialog.ui", self)
        self.train_number.setText(train_number)
        self.statusBar = QStatusBar(self)
        self.verticalLayout_3.addWidget(self.statusBar)
        self._db_cursor = db_cursor
        self._train_id = train_id
        self._train_num = train_number
        self.__update_comboBox()
        self.__fill_table_of_carriages()
        self.update_table_btn.clicked.connect(self.__fill_table_of_carriages)
        self.addNewCarriageBtn.clicked.connect(self.__add_carriage)
        self.update_carriages_btn.clicked.connect(self.__update_comboBox)
        self.save_changes_btn.clicked.connect(self.close)

    def __update_comboBox(self):
        self.comboBox_carriages.clear()
        query_carriages = """SELECT c.carriage_id, c.carriage_name, ct.type_name FROM carriages_to_train ctt 
            RIGHT JOIN carriages c on ctt.carriage_id = c.carriage_id
            INNER JOIN carriage_types ct on c.carriage_type = ct.id
            WHERE ctt.id IS NULL"""
        carriages = self._db_cursor.execute(query_carriages).fetchall()
        for carriage_id, name, type in carriages:
            self.comboBox_carriages.addItem("{}({})".format(name,type), int(carriage_id))
        self.statusBar.showMessage("Выпадающий список обновился",3000)



    def __fill_table_of_carriages(self):
        self.carriages_of_train.setRowCount(0)
        self.carriages_of_train.setColumnCount(3)
        self.carriages_of_train.setHorizontalHeaderLabels([
            "Вагон №", "Тип вагона", ""])
        header = self.carriages_of_train.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setCascadingSectionResizes(True)
        header.setDefaultSectionSize(140)
        header.setHighlightSections(False)
        header.setMinimumSectionSize(100)
        header.setSortIndicatorShown(False)
        header.setStretchLastSection(False)

        current_carriages = self._db_cursor.execute("""SELECT ctt.carriage_id, c.carriage_name, ct.type_name FROM carriages_to_train ctt
            INNER JOIN carriages c ON ctt.carriage_id = c.carriage_id
            INNER JOIN carriage_types ct ON c.carriage_type = ct.id WHERE train_id = ? ORDER BY order_num""",
        self._train_id).fetchall()

        i = 0
        self.carriages_of_train.setRowCount(len(current_carriages))
        for carr_id, carr_name, carr_type in current_carriages:
            carriage_name = QTableWidgetItem(carr_name)
            carriage_name.setFlags((carriage_name.flags() | QtCore.Qt.CustomizeWindowHint) &
                                  ~QtCore.Qt.ItemIsEditable)
            self.carriages_of_train.setItem(i, 0, carriage_name)

            type = QTableWidgetItem(carr_type)
            type.setFlags((type.flags() | QtCore.Qt.CustomizeWindowHint) &
                          ~QtCore.Qt.ItemIsEditable)
            self.carriages_of_train.setItem(i, 1, type)

            del_btn = QPushButton("Удалить",self)
            del_btn.clicked.connect(lambda checked, carr_id=carr_id, tbl_row=i: self.__delete_carriage(carr_id, tbl_row))

            self.carriages_of_train.setCellWidget(i, 2, del_btn)
            i += 1
        self.statusBar.showMessage("Таблица обновилась", 3000)

    def __delete_carriage(self, carriage_id, tbl_row):
        query_delete_carr = """DELETE FROM carriages_to_train ctt WHERE carriage_id=? AND train_id=?"""
        query_update_order = """UPDATE carriages_to_train ctt SET ctt.order_num=(
               SELECT (@row_number:=@row_number + 1) AS num FROM (SELECT @row_number:=0 as tmp ) as rn)
               where ctt.train_id=?"""
        self._db_cursor.execute(query_delete_carr, carriage_id, self._train_id)
        self._db_cursor.execute(query_update_order, self._train_id)
        self._db_cursor.commit()
        self.carriages_of_train.removeRow(tbl_row)
        self.__update_comboBox()

    def __add_carriage(self):
        curr_row = self.carriages_of_train.rowCount()
        if self.carriages_of_train.rowCount() == 0:
            curr_row = 0
        if curr_row == -1:
            curr_row = self.carriages_of_train.rowCount()
        carriage_index = self.comboBox_carriages.currentIndex()
        carriage_name = self.comboBox_carriages.itemText(carriage_index)
        carriage_id = self.comboBox_carriages.itemData(carriage_index)
        print("Will INSERT to {} ROW this: ({},{})".format(curr_row, carriage_id,carriage_name))
        self._db_cursor.execute("""INSERT INTO carriages_to_train (order_num, train_id, carriage_id)
            VALUES (?,?,?)""", curr_row+1, self._train_id, carriage_id)
        self._db_cursor.commit()
        self.__fill_table_of_carriages()
        self.__update_comboBox()


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
        # oImage = QImage("train_background.png")
        # # sImage = oImage.scaled(QSize(self.height(), self.width()))
        # pal = self.palette()
        # pal.setBrush(QPalette.Background, QBrush(oImage))
        # self.setPalette(pal)
        self.setGeometry(100,120,1200,800)
        self.authorization_menu_btn.clicked.connect(self.open_authorization_page)
        self.registration_menu_btn.clicked.connect(self.open_registration_page)
        self.buy_tickets_menu_btn.clicked.connect(self.open_ticket_purchase_page)
        self.edit_routes_menu_btn.clicked.connect(self.open_routes_managment_page)
        self.edit_trains_menu_btn.clicked.connect(self.open_trains_managment_page)
        self.edit_timetable_menu_btn.clicked.connect(self.open_timetable_managment_page)

        self.__main_app: ApplicationBack = None
        self.back_button_on_routePage.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.back_button_on_timetable_Page.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.back_button_on_trains_Page.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.back_button_on_routePage.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.back_button_on_purchase_Page.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        ##########################
        # TODO PAGE : Route Managment
        ##########################

    def init2(self, mainApp):
        self.__main_app = mainApp

        self.update_routesForm.clicked.connect(self.__main_app.route_manager.update_routes)
        self.add_routes_btn.clicked.connect(self.__add_route)

        self.add_new_train_btn.clicked.connect(self.__add_train)
        self.update_trains_table_btn.clicked.connect(self.__main_app.trains_manager.update_trains_table)

        self.add_passage_btn.clicked.connect(self.__add_passage)
        self.update_passages_btn.clicked.connect(self.__main_app.timetable_manager.update_timetable_table)

    #########################################
    ######################################
    # TODO СТАРТОВАЯ СТРАНИЦА
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
        index = self.stackedWidget.indexOf(self.buy_tickets_page)
        self.stackedWidget.setCurrentIndex(index)

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
    # TODO СТРАНИЦА МАРШРУТОВ
    ###################################

    @QtCore.pyqtSlot()
    def fill_routeManagment_table(self, routes):
        self.routes_table.setRowCount(0)
        self.routes_table.setColumnCount(5)
        self.routes_table.setHorizontalHeaderLabels([
            "Номер", "Название", "Тариф в Руб", "", ""])
        header = self.routes_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setCascadingSectionResizes(True)
        header.setDefaultSectionSize(140)
        header.setHighlightSections(False)
        header.setMinimumSectionSize(100)
        header.setSortIndicatorShown(False)
        header.setStretchLastSection(False)
        i = 0
        for route_id, name, num, tariff in routes:
            self.routes_table.insertRow(i)
            name_w = QTableWidgetItem(str(name))
            name_w.setFlags((name_w.flags() | QtCore.Qt.CustomizeWindowHint) &
                                ~QtCore.Qt.ItemIsEditable)
            self.routes_table.setItem(i, 0, name_w)

            num_w = QTableWidgetItem(str(num))
            num_w.setFlags((num_w.flags() | QtCore.Qt.CustomizeWindowHint) &
                          ~QtCore.Qt.ItemIsEditable)
            self.routes_table.setItem(i, 1, QTableWidgetItem(num_w))

            # tariff_edit_field.clicked.connect()
            tariff_edit_field = QLineEdit(str(tariff), self)
            tariff_edit_field.editingFinished.connect(lambda widget=tariff_edit_field, r_id=route_id:
                                                      self.__main_app.route_manager.tariff_field_changed(widget, r_id))
            self.routes_table.setCellWidget(i, 2, tariff_edit_field)

            edit_route_button = QPushButton(text="Ред.", parent=self)
            edit_route_button.clicked.connect(
                lambda state, r_id=route_id, r_nm=name: self.__main_app.route_manager.open_edit_route_Dialog(r_id, r_nm))

            remove_route_button = QPushButton(text="Удалить", parent=self)
            remove_route_button.clicked.connect(
                lambda state, r_id=route_id: self.__main_app.route_manager.delete_route(r_id))

            self.routes_table.setCellWidget(i, 3, edit_route_button)
            self.routes_table.setCellWidget(i, 4, remove_route_button)
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
            print("...Ничего не делаем")  # TODO

    #########################################
    ######################################
    # TODO СТРАНИЦА РЕЙСОВ
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
    # TODO СТРАНИЦА ПОЕЗДОВ
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
                                    WHERE number = ?""", new_number).fetchone()[0]
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
                print("...Ничего не делаем")  # TODO
                return

    def fill_trainsManagment_table(self, trains):
        self.trains_table.setRowCount(0)
        self.trains_table.setColumnCount(3)
        self.trains_table.setHorizontalHeaderLabels([
            "Номер", "", ""])
        header = self.trains_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setCascadingSectionResizes(True)
        header.setDefaultSectionSize(140)
        header.setHighlightSections(False)
        header.setMinimumSectionSize(100)
        header.setSortIndicatorShown(False)
        header.setStretchLastSection(False)

        i = 0
        for train_id, number in trains:
            self.trains_table.insertRow(i)
            self.trains_table.setItem(i, 0, QTableWidgetItem(number))
            edit_train_button = QPushButton(text="Ред.", parent=self)
            edit_train_button.clicked.connect(
                lambda state, train_id=train_id: self.__main_app.trains_manager.open_edit_train_Dialog(train_id))

            remove_train_button = QPushButton(text="Удалить", parent=self)
            remove_train_button.clicked.connect(
                lambda state, train_id=train_id: self.__main_app.trains_manager.delete_train(train_id))

            self.trains_table.setCellWidget(i, 1, edit_train_button)
            self.trains_table.setCellWidget(i, 2, remove_train_button)
            i += 1

    #########################################
    ######################################
    # TODO СТРАНИЦА РЕДАКТИРОВАНИЯ РАСПИСАНИЯ
    ###################################\

    @QtCore.pyqtSlot()
    def __add_passage(self):  # TODO: Перенести в BackEnd
        add_passage_dialog = EditTimetableDialog(cursor, self)
        if add_passage_dialog.exec_():
            new_number: str = add_passage_dialog.new_train_number
            self.__main_app.trains_manager.update_admin_timetable()
        else:
            print("...Ничего не делаем")  # TODO
            return

    def fill_TimetableManagment_table(self, passages):
        self.admin_timetable.setRowCount(0)
        self.admin_timetable.setColumnCount(4)
        self.admin_timetable.setHorizontalHeaderLabels([
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
        for train_id, train_name, route_id, route_name in passages:
            self.admin_timetable.insertRow(i)
            self.admin_timetable.setItem(i, 0, QTableWidgetItem(train_name))
            self.admin_timetable.setItem(i, 1, QTableWidgetItem(route_name))

            edit_passage_button = QPushButton(text="Ред.", parent=self)
            edit_passage_button.clicked.connect(
                lambda state, t_id=train_id, r_id=route_id:
                self.__main_app.timetable_manager.open_edit_passage_Dialog(t_id, r_id))

            remove_passage_button = QPushButton(text="Удалить", parent=self)
            remove_passage_button.clicked.connect(
                lambda state, t_id=train_id, r_id=route_id:
                self.__main_app.timetable_manager.delete_passage(t_id, r_id))

            self.admin_timetable.setCellWidget(i, 2, edit_passage_button)
            self.admin_timetable.setCellWidget(i, 3, remove_passage_button)
            i += 1

    #########################################
    ######################################
    # TODO СТРАНИЦА ПОКУПКИ БИЛЕТОВ
    ###################################\





    #########################################
    ######################################
    ###################################\


class ApplicationBack():
    def __init__(self, user_interface: MainWindowUI):
        self._ui = user_interface  # MAIN APPLICATION INTERFACE
        self._ui.__main_app = self
        self.route_manager = RoutesManager.Routes_Manager(self._ui, cursor, self)
        self.trains_manager = TrainsManager.Trains_Manager(self._ui, cursor, self)
        self.timetable_manager = TimetableManager.Timetable_Manager(self._ui, cursor, self)
        self.purchase_manager = PurchaseManager.Purchase_Manager(self._ui, cursor, self)
        self._ui.init2(self)
        self.authrization_module = AuthorizationModule(self._ui, cursor)

        self.__current_user = None

    def start_route_managment(self):
        self.route_manager.update_routes()

    def start_trains_managment(self):
        self.trains_manager.update_trains_table()

    def start_timetable_managment(self):
        self.timetable_manager.update_timetable_table()


if __name__ == "__main__":
    driver = "MySQL ODBC 8.0 Unicode Driver"
    server_name = "localhost"
    database = "kursach"
    username = "root"
    passwd = "Qwerty123!"

    new_conn = connectToDB(driver, server_name, database, username, passwd)
    cursor = new_conn.cursor()

    ############################################
    # Start QT Applocation
    #############################################
    app = QApplication(sys.argv)
    main_window = MainWindowUI()
    mainApp = ApplicationBack(main_window)
    main_window.show()
    sys.exit(app.exec())
