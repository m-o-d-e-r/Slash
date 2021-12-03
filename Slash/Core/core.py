from typing import Coroutine, Counter
import psycopg2
import string




class SlashTypeError(Exception):
    def __init__(self, text): ...

class SlashRulesError(Exception):
    def __init__(self, text): ...

class SlashBadColumnNameError(Exception):
    def __init__(self, text): ...



class Connection:
    def __init__(self, dbname =  " ", user = " ", password = " ", host = " ", port = 0):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.__connection = psycopg2.connect(
            dbname = self.dbname,
            user = self.user, 
            password = self.password,
            host = self.host,
            port = self.port    
        )
        self.cursor = self.__connection.cursor()
    
    def execute(self, request):
        self.cursor.execute(request)
        self.__connection.commit()

    def close(self):
        self.__connection.close()
    
    def create_table(self, table):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS {} ({})".format(
                table.get_name(),
                ", ".join([f"{col.column_name} {col.column_sql_type}" for col in table.columns])
                )
        )
        self.__connection.commit()



class Create():
    def __init__(self, table, types_list, conn):
        self.connection: Connection = conn
        self.table = table
        if (self.__validate(types_list)):
            self.__create(table)

    def __validate (self, types_list):
        CheckDatas.checkStr(self.table.get_name())

        for column in self.table.columns:
            if column.column_type not in types_list:
                raise SlashTypeError(f"{type(column.column_type)} is not available type for data base")

        for column in self.table.columns:
            CheckDatas.checkStr(column.column_name)

        return True

    def __create(self, table):
        self.connection.create_table(table)


class Insert():
    def __init__(self, conn: Connection, table_name, names, values, rules="*"):
        responce = self.__validate(table_name, names, values, rules)
        #conn.execute(responce)

    def __validate(self, table_name, names, values, rules):
        CheckDatas.checkStr(table_name)

        for name in names:
            CheckDatas.checkStr(name)

        for value in values:
            if value.type_name == "type_text":
                CheckDatas.checkStr(value.value)

            valid_responce = value._is_valid_datas(rules)
            if not valid_responce[0]:
                raise SlashRulesError(f"\n\n\nRule: {valid_responce[1]}")

        r = f"""INSERT INTO {table_name} {str(names).replace("'", "")} VALUES ("""

        for index, v in enumerate(values):
            if v.type_name == "type_int":
                r += str(v.value)
                if (index + 1) != len(values):
                    r += ", "
            elif v.type_name == "type_text":
                r += ("'" + v.value + "'")
                if (index + 1) != len(values):
                    r += ","
        r += ")"

        return r


class Update(): ...

class Delete(): ...

class Operations():
    def __init__(self, connection):
        self.__connection = connection

    def insert(self, connection, table_name, names, values, *, rules="*"):
        if rules == "*":
            Insert(connection, table_name, names, values)
        else:
            Insert(connection, table_name, names, values, rules)

    def update(self):
        Update()

    def delete(self):
        Delete()


class CheckDatas:
    @staticmethod
    def checkStr(str_):
        for char_ in str_:
            if char_ in string.punctuation:
                raise SlashBadColumnNameError(
                    f"Error:\n\nBad name for column of data base\nName: {str_}\nSymbol: {char_}"
                )
        return True
