import pyodbc
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox

import main_app



class Trains_Manager():

    def __init__(self, user_interface, db_cursor, mainApp):
        self.editTrain_dialog = None
        self._mainApp = mainApp
        self._ui = user_interface
        self._db_cursor = db_cursor

    def update_trains_table(self):
        trains = self.get_all_trains()
        self._ui.fill_trainsManagment_table(trains)

    def get_all_trains(self):
        #####################################
        # load all trains from DB
        #####################################
        query = """SELECT * FROM trains order by number"""
        trains = self._db_cursor.execute(query).fetchall()
        return trains

    @QtCore.pyqtSlot(int)
    def delete_train(self, train_id):
        try:
            self._db_cursor.execute("""DELETE FROM trains WHERE trains.id = ?""", train_id)
            now_trains = self.get_all_trains()
            self._ui.fill_trainsManagment_table(now_trains)
        except pyodbc.Error as err:
            self._db_cursor.rollback()
            QMessageBox.critical(self.editTrain_dialog, "Error!",
                 "Can't delete train because of:\n{}".format(err.args))

    #########################
    #######################
    ######################


    @QtCore.pyqtSlot(int)
    def open_edit_train_Dialog(self, train_id):
        train_name = self._db_cursor.execute("""SELECT number FROM trains WHERE id = ?""", train_id).fetchone()[0]
        self.editTrain_dialog = main_app.EditTrainDialog(self._db_cursor, train_id, train_name, self._ui)
        self.editTrain_dialog.exec_()



