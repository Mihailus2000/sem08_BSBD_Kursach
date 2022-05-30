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


