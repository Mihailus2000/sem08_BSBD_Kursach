import pyodbc
import pandas as pd
from sqlalchemy import create_engine
from IPython.display import display

def del_station(station_name, cursor : pyodbc.Cursor):
    finded = cursor.execute("SELECT station_id FROM stations WHERE station_name = '{}'".format(station_name)).fetchall()
    if len(finded) > 0:
        for st_id in finded:
            cursor.execute("CALL delete_station ('{}')".format(st_id[0]))
            cursor.commit()
            print("Deletion complete [{},id={}]".format(station_name,st_id[0]))
    else:
        print("ERR: Station not founded")

def add_station(station_name, cursor):
    cursor.execute("CALL add_station ('{}')".format(station_name))
    cursor.commit()
    print("Insertion complete [{}]".format(station_name))

def del_route(route_num, cursor):
    finded = cursor.execute("SELECT route_id FROM routes WHERE number = '{}'".format(route_num)).fetchall()
    if len(finded) > 0:
        for route_id in finded:
            cursor.execute("CALL delete_route ({})".format(route_id[0]))
            cursor.commit()
            print("Deletion complete [{},id={}]".format(route_num,route_id[0]))
    else:
        print("ERR: Route not founded")

def add_route(train_name, train_num, cursor):
    cursor.execute("CALL add_route ('{}','{}')".format(train_name, train_num))
    cursor.commit()

def del_seatT(type_name, cursor):
    finded = cursor.execute("SELECT seat_type_id FROM seat_types WHERE type_name = '{}'".format(type_name)).fetchall()
    if len(finded) > 0:
        for seatT_id in finded:
            cursor.execute("CALL delete_seatT ({})".format(seatT_id[0]))
            cursor.commit()
            print("Deletion complete [{},id={}]".format(type_name,seatT_id[0]))
    else:
        print("ERR: seatT not founded")

def add_seatTypes(type, cursor):
    cursor.execute("CALL add_seatTypes ('{}')".format(type))
    cursor.commit()

def authentication(login, password, cursor):
    is_valid = cursor.execute("SELECT tickets_on_train.authentication('{}','{}')".format(login,
                                                                    password)).fetchall()[0][0]
    if is_valid == 1:
        print("Success")
        return True # TODO Return client ID or smth unique
    else:
        print("Errrorororo of authentication!")
        return False

def del_carriage(carr_id, cursor):
    finded = cursor.execute("SELECT carriage_id FROM carriages WHERE carriage_id = {}".format(carr_id)).fetchall()
    if len(finded) > 0:
        cursor.execute("CALL delete_carriages ({})".format(carr_id))
        cursor.commit()
        print("Delete of carriage complete [id={}]".format(carr_id))
    else:
        print("ERR: Carriage not founded")

def add_carriage(name, seatT_name, cursor):
    seatTs = cursor.execute("SELECT seat_type_id FROM seat_types WHERE type_name = '{}'".format(seatT_name)).fetchall()
    if len(seatTs) == 1:
        cursor.execute("CALL add_carriages ('{}',{})".format(name,seatTs[0][0]))
        cursor.commit()
        print("Insertion of carriage complete [{},{}]".format(name,seatT_name))
    else:
        print("Insertion error")

def registration(login, cursor : pyodbc.Cursor):
    # all_ok = False
    login_cnt = cursor.execute("""SELECT COUNT(login) FROM customers
                    WHERE login='{}'""".format(login)).fetchall()[0][0]
    if login_cnt == 1:
        print("Login is busy")
        return False
    elif login_cnt == 0:
        print("Login is OK")
        print("Please enter the password:\n")
        passwd = input()    # TODO Add check of password
        print("Enter your first Name")
        f_name = input()
        print("Enter your second Name")
        s_name = input()
        cursor.execute("""INSERT INTO customers(first_name, second_name, login, passwd)
                        VALUES('{}', '{}', '{}', MD5('{}'))""".format(f_name,s_name,login,passwd))
        cursor.commit()
        print("Registration complete!")
        return True
    else:
        print("WTF?? > 1 user with the same login!") # TODO print EXCEPTION only on server
        return False


def display_table(all_tables_list,db_connection, cursor, table_name, *columns):
    if table_name not in all_tables_list:
        print("ERR: unknown table! ")
        return
    if len(columns) == 0:
        df = pd.read_sql_query("SELECT * FROM {}".format(table_name), con=db_connection)
        display("--------------------------[{}]--------------------------\n".format(table_name),df)
    else:
        df =pd.read_sql_query("SELECT {} FROM {}".format(columns, table_name), con=db_connection)
        display("--------------------------[{}]--------------------------\n".format(table_name),df)

def display_all_tables(db_con, all_tables_list, cursor):
    for tabl in all_tables_list:
        display_table(all_tables_list, db_con, cursor, tabl)
        print("-----------------------------------------------------------------\n")

def row_SQL_query(query,cursor:pyodbc.Cursor):
    try:
        cursor.execute(query)
        cursor.commit()
    except Exception as ex:
        print("ERR: SQL query failed: {}".format(ex.args))

def simple_parser(all_tables, db_con, cursor : pyodbc.Cursor):
    end_of_work = False
    all_commands = ["auth","registr","new_table","new_route","new_carr","new_seatT","new_station","disp_table","exit","quit",
                    "del_route","del_carr","del_seatT","del_station","row_sql"]
    print("All available commands: [{}]".format(all_commands))
    while not end_of_work:
        try:
            print("> ",end='')
            new_request = input()
            tokens = new_request.split(sep=" ")
            cmd = tokens[0]
            if cmd not in all_commands:
                print("ERR: Unknown command!")
                continue
            match cmd:
                case "row_sql":
                    query = new_request[7:]
                    print("Correct query?:\n\t {}".format(query))
                    print("Print 1 or 0")
                    answ = input()
                    if answ == '1':
                        row_SQL_query(query,cursor)
                    else:
                        print("ERR: !\n>? row_sql <SQL query>")

                case "exit":
                    if len(tokens) > 1:
                        print("WRN: Exit command has no params")
                    end_of_work = True
                    break
                case "auth":
                    if len(tokens) == 3:
                        is_auth = authentication(tokens[1],tokens[2],cursor)
                        if is_auth:
                            AUTHORIZED = True
                            USR_LOGIN = tokens[1]
                            pass #TODO Start Application
                        else:
                            continue
                    else:
                        print("ERR: Syntax error!\n>? auth <login> <password>")
                        continue
                case "registr":
                    if len(tokens) == 2:
                        is_registered = registration(tokens[1], cursor)
                        if is_registered:
                            pass  # TODO Start Application
                        else:
                            continue
                    else:
                        print("ERR: Syntax error!\n>? registr <new login>")
                        continue
                case "quit":
                    if len(tokens) > 1:
                        print("WRN: Quit command has no params")
                        # TODO Algorithm
                        AUTHORIZED = False
                        USR_LOGIN = None
                        continue
                case "disp_table":
                    if len(tokens) == 2:
                        display_table(all_tables, db_con, cursor, tokens[1])
                    elif len(tokens) > 2:
                        display_table(all_tables, db_con, cursor, tokens[1], tokens[2:])
                    else:
                        print("ERR: Syntax error!\n>? disp_table <table name> [*columns] ")
                        continue
                case "new_station":
                    if len(tokens) == 2:
                        add_station(tokens[1],cursor)
                    else:
                        print("ERR: Syntax error!\n>? new_station <station name>")
                        continue
                case "del_station":
                    if len(tokens) == 2:
                        del_station(tokens[1], cursor)
                    else:
                        print("ERR: Syntax error!\n>? del_station <station name>")
                        continue
                case "new_route":
                    if len(tokens) == 3:
                        add_route(tokens[1], tokens[2], cursor)
                    else:
                        print("ERR: Syntax error!\n>? new_route <train name> <route number>")
                        continue
                case "del_route":
                    if len(tokens) == 2:
                        del_route(tokens[1], cursor)
                    else:
                        print("ERR: Syntax error!\n>? del_route <route number>")
                        continue
                case "new_carr":
                    if len(tokens) == 3:
                        add_carriage(tokens[1],tokens[2], cursor)
                    else:
                        print("ERR: Syntax error!\n>? new_carr <carriage name > <seats type name>")
                        continue
                case "del_carr":
                    if len(tokens) == 2:
                        del_carriage(tokens[1], cursor)
                    else:
                        print("ERR: Syntax error!\n>? del_carr <carriage id>")
                        continue
                case "new_seatT":
                    if len(tokens) == 2:
                        add_seatTypes(tokens[1],cursor)
                    else:
                        print("ERR: Syntax error!\n>? new_seatT <type name>")
                        continue
                case "del_seatT":
                    if len(tokens) == 2:
                        del_seatT(tokens[1], cursor)
                    else:
                        print("ERR: Syntax error!\n>? del_seatT <type name>")
                        continue
                case "new_station":
                    if len(tokens) == 2:
                        add_station(tokens[1],cursor)
                    else:
                        print("ERR: Syntax error!\n>? new_station <station name>")
                        continue
                case "del_station":
                    if len(tokens) == 2:
                        del_station(tokens[1], cursor)
                    else:
                        print("ERR: Syntax error!\n>? del_station <station name>")
                        continue
        except Exception as excp:
            print("ERR:", excp.args)

    print("Program stopped")